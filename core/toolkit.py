import sys
import globals
def stat(message): # Structured printing
    name = sys._getframe().f_back.f_code.co_name
    if name == "<module>":
        name = "ROOT"
        print("[" + name + "] " + str(message))
    else:
        print("  [" + name + "] " + str(message))

def verbo(message): # Structured printing for verbose
    if (globals.args.verbose):
        name = sys._getframe().f_back.f_code.co_name
        if name == "<module>":
            name = "ROOT"
            print("[" + name + "] " + str(message))
        else:
            print("  [" + name + "] " + str(message))

def debug(message): # Structured printing for verbose
    if (globals.args.debug):
        name = sys._getframe().f_back.f_code.co_name
        if name == "<module>":
            name = "ROOT"
            print("DEBUG [" + name + "] " + str(message))
        else:
            print("DEBUG  [" + name + "] " + str(message))
