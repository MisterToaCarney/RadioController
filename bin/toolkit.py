import sys
def stat(message): # Structured printing
    name = sys._getframe().f_back.f_code.co_name
    if name == "<module>":
        name = "ROOT"
        print("[" + name + "] " + str(message))
    else:
        print("  [" + name + "] " + str(message))
