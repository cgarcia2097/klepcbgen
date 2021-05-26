# KLE PCB Generator

This repo is a fork of the [original KLE PCB Generator by Jeroen Bowens](https://github.com/jeroen94704/klepcbgen). The goal is to address some of the future work described by the original repo, which is:

- Modify the types of switches used
- Add backlighting
- Key rotation
- Vertical keys

## State of the project

The current state of the project is in alpha, and is currently trying to implement the features of the original KLE PCB Generator. Work is being done to better abstract sections of the original project.

## Dependecies

The dependencies are as follows:
- A working KiCAD installation: [KiCAD page](https://www.kicad.org/)
- A KiCAD footprint library containing a variety of switches: [Here's the one I use](https://github.com/perigoso/keyswitch-kicad-library)
- Skidl, a Python tool for generating KiCAD netlists: [Skidl page](https://xess.com/skidl/docs/_site/)

## Philosophy of use

For the time being, these scripts are to be treated more as a plugin and less of a one-click solution. The steps are broken down as follows

- Create the coordinate map of all the keyswitches on the PCB using the existing Key Class found in the original `klepcbgen.py`, plus the JSON file from Keyboard Layout Editor

- Create the KiCAD netlist for the keyboard matrix and control circuit, and optionally, any lighting, encoder and custom circuits using information from the coordinate map and a configuration file

- Import netlist into a KiCAD pcb file

- Automate the placement of the PCB file using the coordinate map and the config file

## Credits

Jeroen Bowens @jeroen94704: [Link](https://github.com/jeroen94704)
Charles Garcia @cgarcia2097:
