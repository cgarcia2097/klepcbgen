""" Keyboard netlist generator using KLE JSON files. Uses the closest square matrix for a given number of keys """

import sys
import argparse
import json
from klepcbgenmod import *

######################################################################
######################################################################
# Global Definitions
######################################################################
######################################################################

PROG_VERSION_NUMBER = 0.1
args = []

######################################################################
######################################################################
# Classes
######################################################################
######################################################################

def kle2KeyClassJSON(klepcbgen):
    """ Create a JSON file for all instances of the Key Class for the given KLE file"""
    layout = []

    for item in klepcbgen.keyboard.keys:
        tmpString = json.dumps(item.__dict__)
        layout.append(tmpString)

    with open(args.output_name + ".kle_json", "w+") as fp:
        json.dump(layout, fp)

######################################################################
######################################################################
# Functions
######################################################################
######################################################################

def parseCmdArgs():
    """ Parses the incoming command-line arguments """

    parser = argparse.ArgumentParser(
        prog="jsonen",
        description="Create a detailed coordinate layouts using a key layout defined in Keyboard Layout Editor (http://www.keyboard-layout-editor.com/)"
    )
    parser.add_argument(
        "infile",
        help='The JSON file containing the keyboard layout in the KLE JSON format'
    )
    parser.add_argument(
        "-v", "--version", action="version", version="Version " + str(PROG_VERSION_NUMBER),
        help='Displays version number'
    )
    parser.add_argument(
        "output_name",
        help='The base name of all output files'
    )
    args = parser.parse_args()

    if not args.infile:
        parser.error(
            "\nKLE layout file missing. Use '-h' for more information"
        )
    
    return args

######################################################################
######################################################################
# Main program entry
######################################################################
######################################################################

def main(argv):
    """ Main entry for the program """

    # Parse JSON through KLEPCBGen
    kleproj = KLEPCBGenerator()
    kleproj.read_kle_json(args)
    kle2KeyClassJSON(kleproj)

    return 0

if __name__ == "__main__":
    args = parseCmdArgs()
    main(args)
    
