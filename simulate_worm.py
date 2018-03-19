#!/usr/bin/python3
"""Simulate a worm traversing a network."""
from optparse import OptionParser
from csv import reader
from networkx import Graph
from random import choice, random


def simulate(net: Graph, patient_zero: str,
             infection_probability: float) -> int:
    """Simulate worm propagation through a given network from a given node.
       Returns the number of rounds to fully infect the network."""
    infected = list(patient_zero)
    round_count = 0
    print('Infecting ' + str(len(net.nodes())) + ' nodes, starting from '
          + patient_zero + '.')
    while len(infected) < len(net.nodes()):
        currently_infected = len(infected)
        for node in net.neighbors(choice(infected)):
            if node not in infected:
                if random() <= infection_probability:
                    infected.append(node)
        round_count += 1
        print('Round: ' + str(round_count) + ', '
              + str(len(infected) - currently_infected)
              + ' newly infected, ' + str(len(infected)) + ' total infected.')
    return round_count


def simulate_inoculation(net: Graph, patient_zero: str,
                         infection_probability: float, inoculator: str,
                         inoculation_probability: float):
    """Simulate worm and inoculation propagation through a given network,
       from two given nodes. Returns the number of rounds to either fully
       infect or fully cure the network."""
    infected = list(patient_zero)
    inoculated = list(inoculator)
    round_count = 0
    print('Infecting ' + str(len(net.nodes())) + ' nodes, starting from '
          + patient_zero + ', and inoculating from ' + inoculator + '.')
    while len(infected) > 0:
        currently_infected = len(infected)
        currently_inoculated = len(inoculated)
        for node in net.neighbors(choice(infected)):
            if node not in infected and node not in inoculated:
                if random() <= infection_probability:
                    infected.append(node)
        for node in net.neighbors(choice(inoculated)):
            if node not in inoculated:
                if random() <= inoculation_probability:
                    inoculated.append(node)
                    if node in infected:
                        infected.remove(node)
        round_count += 1
        infection_delta = str(len(infected) - currently_infected)
        inoculation_delta = str(len(inoculated) - currently_inoculated)
        print('Round: ' + str(round_count) + ', infection delta: ' +
              infection_delta + ', inoculation delta: ' + inoculation_delta +
              ', total infected: ' + str(len(infected)) +
              ', total inoculated: ' + str(len(inoculated)))
    return round_count


def main():
    """Build a network from a file, then see how long it takes to infect."""
    parser = OptionParser(description="Load a random graph from a CSV file," +
                                      "infect a given node, and spread with " +
                                      "a given probability.")
    parser.add_option("-n", "--network", metavar="FILE", type="string",
                      dest="csv_file", help="Opens the csv-formatted network" +
                                            "CSV-format file located at FILE.")
    parser.add_option("-p", "--infection-probability", metavar="PROBABILITY",
                      type="float", dest="infection_probability", default=0.5,
                      help="The probability that an infection will spread")
    parser.add_option("-f", "--first-infected", metavar="NODE", type="string",
                      dest="patient_zero", default='0',
                      help="The index of the initially infected node.")
    parser.add_option("-i", "--inoculator", metavar="NODE", type="string",
                      dest="inoculator", default=None,
                      help="The index of the first inoculator node.")
    parser.add_option("-q", "--inoculation-probability", metavar="PROBABILTIY",
                      type="float", dest="inoculation_probability",
                      default=0.5,
                      help="The probability that a node will be inoculated" +
                           "(and cured).")
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
                graph.add_edge(row[0], row[1])
            if options.patient_zero not in graph.nodes():
                parser.error("Patient zero must be in the set of nodes."
                             + "\nPatient zero: " + str(options.patient_zero)
                             + "\nNode set:\n" + str(graph.nodes()))
            elif options.inoculator is None:
                simulate(graph, options.patient_zero,
                         options.infection_probability)
            else:
                if options.inoculator in graph.nodes():
                    simulate_inoculation(graph, options.patient_zero,
                                         options.infection_probability,
                                         options.inoculator,
                                         options.inoculation_probability)
                else:
                    parser.error("The inoculator must be in the set of nodes.")

    except IOError:
        parser.error("Unable to open or read from " + options.csv_file)


if __name__ == "__main__":
    main()
