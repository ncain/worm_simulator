"""Generate a CSV file representing a graph."""
from optparse import OptionParser
from math import floor
from networkx import connected_watts_strogatz_graph
from networkx import barabasi_albert_graph
from networkx import fast_gnp_random_graph
from networkx import draw as draw_nx
from matplotlib.pyplot import draw
from csv import writer


def main():
    """Generate a CSV file according to command-line options."""
    parser = OptionParser(description="""Generate a random graph, and save it as
                          a CSV file.""",
                          epilog="""The program is unable to generate more than
                          one graph at a time, and so cannot run when any pair
                          of -e, -b, and -w are specified.""")

    parser.add_option("-o", "--out", metavar="FILE", type="string",
                      dest="filename", default="graph.csv",
                      help="Write the output graph in CSV format to FILE")

    parser.add_option("-v", "--vertices", type="int", dest="vertices",
                      default=1000,
                      help="Size (vertex count) of the output graph")

    parser.add_option("-e", "--erdos", "--erdos-renyi", metavar="probability",
                      type="float", dest="erdos",
                      help="""Generate an Erdös-Rényi output graph, with the
                      specified probability of edge creation.""")

    parser.add_option("-b", "--barabasi", "--barabasi-albert", metavar="edges",
                      type="int", dest="barabasi",
                      help="""Generate a Barabási-Albert output graph,
                      with the specified number of edges per new node.""")

    parser.add_option("-w", "--watts", "--watts-strogatz", metavar="pksum",
                      type="float", dest="watts",
                      help="""Generate a Watts-Strogatz graph, where pksum is
                      p + k, with p being the probability of an edge being
                      replaced, and k being the number of neighbors
                      per sub-ring.""")
    (options, args) = parser.parse_args()
    graph = None
    if not any((options.erdos, options.barabasi, options.watts)):
        # no graph type was chosen- choose a sensible default.
        graph = fast_gnp_random_graph(1000, 0.5)
    elif any(((options.erdos and options.barabasi),
              (options.erdos and options.watts),
              (options.barabasi and options.watts))):
        # two or more graph types were chosen- print an error message.
        parser.error("Please specify only one of -e, -b, and -w.")
    elif options.erdos:
        if (options.erdos <= 0 or 1 <= options.erdos):
            # probabilities must be between 0 and 1.
            parser.error("""Probability of edge creation
                         must be between 0 and 1.""")
        else:
            graph = fast_gnp_random_graph(options.vertices, options.erdos)
    elif options.barabasi:
        if (options.barabasi < 1 or options.vertices <= options.barabasi):
            # the number of edges per new node must be between 1
            # and the total number of vertices.
            parser.error("""The number of edges per new node must be
                         between 1 and the total number of vertices.""")
        else:
            graph = barabasi_albert_graph(options.vertices, options.barabasi)
    elif options.watts:
        neighbors = floor(options.watts)
        probability = options.watts - neighbors
        if (neighbors >= options.vertices or 1 > neighbors):
            # there can't be more neighbors than total vertices in a subring.
            parser.error("""The integer part of pksum must be between 1 and
                         the number of total vertices, and is ideally much
                         less than the number of vertices.""")
        elif (probability <= 0 or 1 <= probability):
            # probabilities must be between 0 and 1.
            parser.error("""The probability of rewiring an edge
                         (the fractional part of pksum) must be
                         between 0 and 1.""")
        else:
            try:
                graph = connected_watts_strogatz_graph(options.vertices,
                                                       neighbors,
                                                       probability)
            except Exception:
                parser.error("""Unable to construct a connected Watts-Strogatz
                             graph with the given pksum in under 100 tries.""")
    else:
        parser.error("Unable to make sense of the given arguments. Exiting.")
    try:
        with open(options.filename, 'w', newline='') as outfile:
            # write to the file with outfile.write
            csvwriter = writer(outfile)
            draw_nx(graph)
            draw()
            for edge in graph.edges:
                csvwriter.writerow(edge)
    except IOError as e:
        parser.error("Unable to open or write "
                     + options.filename
                     + " due to IOError: "
                     + e.strerror)


if __name__ == "__main__":
    main()
