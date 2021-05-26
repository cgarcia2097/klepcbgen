# KLE PCB Generator

This repo is a fork of the [original KLE PCB Generator by Jeroen Bowens](https://github.com/jeroen94704/klepcbgen). The goal is to address some of the future work described by the original repo, which is:

- Modify the types of switches used
- Add backlighting
- Key rotation
- Vertical keys

## State of the project

The current state of the project is in alpha, and is currently trying to implement the features of the original KLE PCB Generator.

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

## My current take on the current klepcbgen project

It's hard not to be impressed at the level of work that went into the current klepcbgen project, since looking at the source files reminded be quite a bit of how a website is rendered. The templates themselves are KiCAD schematic and PCB files, rather than your typical HTML. However, the templates are hand-modified and the project itself is unable to tap into the user's existing KiCAD install (which contains the bulk of the libraries). Unless one can regex the whole KiCAD library into a series of Jinja templates, the project cannot be properly expanded to more switch types, or even lighting types. This severely limits the potential of this project.
