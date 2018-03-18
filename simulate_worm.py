#!/usr/bin/python3
"""Simulate a worm traversing a network."""
from optparse import OptionParser
from csv import reader
from networkx import Graph


def main():
    """Build a network from a file, then see how long it takes to infect."""
    parser = OptionParser(description="""Load a random graph from a CSV file,
                          infect a given node,
                          and spread with a given probability.""")
    parser.add_option("-n", "--network", metavar="FILE", type="string",
                      dest="csv_file", help="""Opens the csv-formatted network
                      CSV-format file located at FILE.""")
    parser.add_option("-p", "--infection-probability", metavar="PROBABILITY",
                      type="float", dest="infection_probability", default=0.5,
                      help="The probability that an infection will spread")
    parser.add_option("-f", "--first-infected", metavar="NODE", type="int",
                      dest="patient_zero", default=0, help="""The index of the
                      initially infected node.""")
    parser.add_option("-i", "--inoculator", metavar="NODE", type="int",
                      dest="inoculator", default=None, help="""The index of the
                      first inoculator node.""")
    parser.add_option("-q", "--inoculation-probability", metavar="PROBABILTIY",
                      type="float", dest="inoculation_probability",
                      default=0.5, help="""The probability that a node will be
                      inoculated (and cured).""")
    (options, args) = parser.parse_args()
    graph = Graph()
    if any(((options.inoculation_probability > 1),
            (options.inoculation_probability < 0),
            (options.infection_probability > 1),
            (options.infection_probability < 0))):
        parser.error("Probabilities must be between 0 and 1.")
    try:
        with open(options.csv_file, 'r') as infile:
            csv = reader(infile)
            for row in csv:
                graph.add_edge(row)

    except IOError:
        parser.error("Unable to open or read from " + options.csv_file)
