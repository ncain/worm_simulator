#!/usr/bin/python3
"""Generate a CSV file representing a graph."""
from optparse import OptionParser
from networkx import connected_watts_strogatz_graph
from networkx import barabasi_albert_graph
from networkx import fast_gnp_random_graph
from networkx import draw as draw_nx
from matplotlib.pyplot import draw, show
from csv import writer


def main():
    """Generate a CSV file according to command-line options."""
    parser = OptionParser(description="Generate a random graph, and save it "
                                      "as a CSV file containing its edges.",
                          epilog="The program is unable to generate more "
                                 "than one graph at a time, and so cannot "
                                 "run when any pair of -e, -b, and -w "
                                 "(or all three) are specified.")

    parser.add_option("-o", "--out", metavar="FILE", type="string",
                      dest="filename", default="graph.csv",
                      help="Write the output graph in CSV format to FILE. "
                           "Defaults to 'graph.csv' inside the current "
                           "working directory.")

    parser.add_option("-v", "--vertices", type="int", dest="vertices",
                      default=1000, metavar="COUNT",
                      help="Size (vertex count) of the output graph")

    parser.add_option("-p", "--probability", metavar="VALUE", type="float",
                      dest="probability", default=0.5,
                      help="This argument is used to "
                           "specify a probability for use with either the -e "
                           "or -w option. VALUE must be between 0 and 1.")

    parser.add_option("-n", "--num-edges", "--number-of-edges",
                      "--num-neighbors", "--number-of-neighbors",
                      metavar="NUM", type="int", dest="num", default=2,
                      help="This argument is used to specify a number of "
                           "edges for use when generating a Barabási-Albert "
                           "network with the -b option, or to specify the "
                           "number of neighbors when generating a "
                           "Watts-Strogatz network with the -w option.")

    parser.add_option("-e", "--erdos", "--erdos-renyi",
                      action="store_true", dest="erdos", default=False,
                      help="Generate an Erdös-Rényi output graph, with the "
                           "specified probability of edge creation. "
                           "A value of 0.015 produces fairly sparse but "
                           "typically connected graphs, while 0.5 chooses "
                           "from graphs uniformly among those of degree "
                           "equal to that specified by the -v parameter. "
                           "Probability is specified with -p <value>.")

    parser.add_option("-b", "--barabasi", "--barabasi-albert",
                      action="store_true", dest="barabasi", default=False,
                      help="Generate a Barabási-Albert output graph, "
                           "with the specified number of edges per new node. "
                           "Number of edges is specified with -n <value>.")

    parser.add_option("-w", "--watts", "--watts-strogatz",
                      action="store_true", dest="watts", default=False,
                      help="Generate a Watts-Strogatz graph, with the "
                           "specified probability of random swaps as well "
                           "as the specified number of (initially) "
                           "short-circuited neighbors. Number of neighbors "
                           "is specified with -n <value>, and probability "
                           "is specified with -p <value>.")
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
    elif options.probability < 0 or options.probability > 1:
        parser.error("Probability must be between 0 and 1, "
                     "written as a floating-point number.")
    elif options.num < 0:
        parser.error("-n option can only specify a positive integer.")
    elif options.erdos:
        graph = fast_gnp_random_graph(options.vertices, options.probability)
    elif options.barabasi:
        if options.num < 1 or options.vertices <= options.num:
            parser.error("The number of edges per new node must be "
                         "between 1 and the total number of vertices.")
        else:
            graph = barabasi_albert_graph(options.vertices, options.num)
    elif options.watts:
        if options.num >= options.vertices or options.num < 2:
            parser.error("Number of neighbors must be less than "
                         "the total number of vertices, and is "
                         "ideally much less. Number of neighbors"
                         "must also be equal or greater than 2.")
        else:
            try:
                graph = connected_watts_strogatz_graph(options.vertices,
                                                       options.num,
                                                       options.probability)
            except Exception:
                print("Unable to build a connected Watts-Strogatz "
                      "graph with the given pksum in under 100 tries. "
                      "I'm giving up, but you're free to ask me to try again.")
                exit(2)
    else:
        parser.error("Unable to make sense of the given arguments. Exiting.")
    try:
        with open(options.filename, 'w', newline='') as outfile:
            # write to the file with outfile.write
            csvwriter = writer(outfile)
            draw_nx(graph)
            draw()
            show()
            for edge in graph.edges:
                csvwriter.writerow(edge)
    except IOError as e:
        parser.error("Unable to open or write " + options.filename +
                     " due to IOError: " + e.strerror)


if __name__ == "__main__":
    main()
