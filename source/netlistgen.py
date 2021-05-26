######################################################################
######################################################################
# Description
######################################################################
######################################################################
""" Creates a netlist based from the Key Class JSON file """

######################################################################
######################################################################
# Imports
######################################################################
######################################################################

import sys
import argparse
import json
import os
import datetime
import pcbnew

from skidl import *

######################################################################
######################################################################
# Global Definitions and Variables
######################################################################
######################################################################

PROG_VERSION_NUMBER = 0.1
args = []

######################################################################
######################################################################
# Functions
######################################################################
######################################################################

def selectSupportedDiodes(diodeType):
    """ Returns footprint name of the supported diode, returns an error if not supported 
    
        Returned object will have this form:
            {
                "lib_dir":"",
                "footprint_ref": "",
            }
    """

    def selectTHTDiode():
        """ select parts for a through hole diode """
        print ("Using through-hole diode...")

        partName = {
            "lib_dir" : "Diode_THT",
            "footprint_ref": "D_DO-35_SOD27_P7.62mm_Horizontal"
        }
        return partName

    def selectSMDDiode():
       """ select parts for a surface mount diode """
       print ("Using surface mount diode...")

       partName = {
           "lib_dir" : "Diode_SMD",
           "footprint_ref": "D_SOD-123"
       }
       return partName

    def unsupportedDiode():
        """ For invalid options """
        print("Unsupported diode detected. Reverting to through-hole diodes")
        return selectTHTDiode()

    # Dictionary mapping
    diodeDict = {
        "smd" : selectSMDDiode,
        "tht" : selectTHTDiode
    }

    return diodeDict.get(diodeType, unsupportedDiode)()

def selectSupportedKeyswitch(switchType):
    """ Returns footprint name of the supported switch, returns an error if not supported 
    
        Returned object will have this form:
            {
                "lib_dir":"",
                "footprint_ref": "",
            }
    """

    def selectMXParts():
        """ select parts for a Cherry MX circuit """
        print ("Using MX-Style switches...")

        partName = {
            "lib_dir" : "Switch_Keyboard_Cherry_MX",
            "footprint_ref": "SW_Cherry_MX_PCB_1.00u"
        }
        return partName

    def selectALPSParts():
        print ("Using ALPS switches...")
        """ select parts for an ALPS/Matias circuit """

        partName = {
            "lib_dir" : "Switch_Keyboard_Alps_Matias",
            "footprint_ref": "SW_Alps_Matias_1.00u"
        }
        return partName

    def selectMXALPSParts():
        print ("Using MX/ALPS hybrid switches...")
        """ select parts for a hybrid MX/Alps circuit """
        partName = {
            "lib_dir" : "Switch_Keyboard_Hybrid",
            "footprint_ref": "SW_Hybrid_Cherry_MX_Alps_1.00u"
        }
        return partName

    def selectKailhChocParts():
        print ("Using Kailh Choc switches...")
        """ select parts for a Kailh Choc circuit """
        partName = {
            "lib_dir" : "Switch_Keyboard_Kailh",
            "footprint_ref": "SW_Kailh_Choc_V1_1.00u"
        }
        return partName

    def selectMXHotSwapParts():
        print ("Using MX-style hotswap switches...")
        """ select parts for a MX hot-swap circuit """
        partName = {
            "lib_dir" : "Switch_Keyboard_Kailh",
            "footprint_ref": "SW_Hotswap_Kailh_1.00u"
        }
        return partName

    def unsupportedSwitch():
        """ For invalid options """
        print("Switch is currently unsupported. Reverting to MX switches...")
        return selectMXParts()

    # Dictionary Mapping
    keySwitchDict = {
        "mx" : selectMXParts,
        "alps" : selectALPSParts,
        "mxalps" : selectMXALPSParts,
        "choc" : selectKailhChocParts,
        "mxhotswap" : selectMXHotSwapParts
    }

    if not isinstance(switchType, str):
        print("Error processing the required footprint.")
        return False

    switchFootprint = keySwitchDict.get(switchType, unsupportedSwitch)()
    return switchFootprint

def parseCmdArgs():
    """ Parses the incoming command-line arguments """

    parser = argparse.ArgumentParser(
        prog="netlistgen",
        description="Create a Skidl netlist using a key layout file generated by jsongen.py"
    )
    parser.add_argument(
        "layout_file",
        help='The JSON file denoted as .kle_json'
    )
    parser.add_argument(
        "config_file",
        help='The JSON file containing keyswitch settings, denoted as .config_json'
    )
    parser.add_argument(
        "-v", "--version", action="version", version="Version " + str(PROG_VERSION_NUMBER),
        help='Displays version number of program'
    )
    parser.add_argument(
        "output_name",
        help='The base name of all output files'
    )
    args = parser.parse_args()

    if not (args.layout_file):
        parser.error(
            "\nLayout file missing. Use '-h' for more information"
        )

    if not (args.config_file):
        parser.error(
            "\nConfig file missing. Use '-h' for more information"
        ) 

    return args

######################################################################
######################################################################
# Classes
######################################################################
######################################################################

class Key:
    """ Contains all information about a given keyswitch

        Attributes:
            layoutInfo          dict        Keyboard info from the .kle_json file
            switchType          string      Describes the switch type used for this keyboard
            backlightSupport    bool        Indicates whether backlighting is supported with this keyswitch
            pcbStabSupport      bool        Indicates whether or not to add stabilizer holes for this keyswitch 
    """

    def __init__(self):
        self.layoutInfo = []
        self.switchType = ""
        self.backlightSupport = ""
        self.pcbStabSupport = ""

class KeyUnit(Key):
    """ Contains the basic unit of a keyswitch matrix

    Attributes:
        diode       Skidl       Skidl object describing the keyswitch diode used in the keyswitch matrix
    """

    def __init__(self):
        Key.__init__(self)
        self.switch = ""
        self.diode = ""

class LightUnit:
    """ TODO: Contains a lighting unit for each keyswitch.  """
    pass

class ControlUnit:
    """ TODO: Contains the control unit for the keyboard """
    pass

class CustomUnit:
    """ TODO: Any custom circuit"""
    pass


class Keyboard:
    """ Contains all parts needed to describe the keyboard.
    
        Possible order of operations
            - Create the control circuit first. This takes the guesswork out of the available number of pins for the control unit
            - Create the keyswitch matrix. This will spawn the required keyswitches and diodes for a basic keyboard matrix
            - Create the lighting circuit. The lighting units will be 
            - Create the custom circuit
            - Connect all circuits together
    
    """

    def __init__(self):
        self.keyUnits = []
        self.lightUnits = []
        self.controlUnits = []
        self.customUnits = []

    def createKeyMatrix(self, switchType, diodeType):
        """ TODO: Create the keyswitch matrix. Currently creates the closest square matrix based on number of keys """

        # Generate nets
        cols = math.ceil(math.sqrt(len(self.keyUnits)))     # Uses the closest square root of the number of keys to generate the matrix
        rows = math.floor(math.sqrt(len(self.keyUnits)))

        if (cols*rows) >= len(self.keyUnits):
            print("Cols: {}, Rows: {}".format(cols, rows))

        # Generate the circuit
        switchFootprint = selectSupportedKeyswitch(switchType)
        diodeFootprint = selectSupportedDiodes(diodeType)
        print(str(switchFootprint) + " , " + str(diodeFootprint))

        

        for item in self.keyUnits:

            # Keyswitch
            item.switch = Part('Switch', 'SW_SPST')
            item.switch.ref = "K" + str(item.layoutInfo["num"])
            item.switch.footprint = switchFootprint['lib_dir'] + ":" + switchFootprint["footprint_ref"]
            
            # Diode
            item.diode = Part('Device', 'D')
            item.diode.ref = "D" + str(item.layoutInfo['num'])
            item.diode.footprint = diodeFootprint['lib_dir'] + ":" + diodeFootprint["footprint_ref"]


            # print(str(item.switch) + str(item.switch.footprint) + "," + str(item.diode) + str(item.diode.footprint))

    def createLightingCircuit(self):
        """ TODO: Create the lighting circuit based on the parts provided.  Diodes and lighting circuits are generated on a 1-1 basis with each key"""
        pass

    def createControlCircuit(self):
        """ TODO: Generate the required control circuit for the keyboard """
        pass

    def createCustomCircuit(self):
        """ TODO: Connect the components together """
        pass

    def connectAllSubcircuits(self):
        """ TODO: Connects all the subcircuits together """
        pass


######################################################################
######################################################################
# Main Program Entry (if needed)
######################################################################
######################################################################

def main(argv):
    """ Main entry for the program """

    mainKeeb = Keyboard()

    try:
        configFile = open(args.config_file, "r")
        layoutFile = open(args.layout_file, "r")

        layout = json.load(layoutFile)
        for key, item in enumerate(layout):
            tmpKey = KeyUnit()
            tmpKey.layoutInfo = json.loads(item)
            mainKeeb.keyUnits.append(tmpKey)
            # print(mainKeeb.keyUnits[key].layoutInfo)
        
        config = json.load(configFile)
        print(config)
        
    except ValueError as err:
        print(err + ": Failed to process JSON files. Exiting...")
        exit()
    except OSError as err:
        print(err + ": Failed to open input files. Exiting...")
        exit()

    # TODO: Assemble the circuit
    mainKeeb.createKeyMatrix(config["switch_schema"]["type"], config["switch_schema"]["diodeMount"])

    # Generate the final netlist
    generate_netlist()
    return 0

if __name__ == "__main__":
    args = parseCmdArgs()
    main(args)