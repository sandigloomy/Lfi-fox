import sys
from time import sleep
import random
from colorama import Fore, Style


class Colors:
    OKBLUE = Fore.BLUE
    WARNING = Fore.YELLOW
    FAIL = Fore.RED
    ENDC = Style.RESET_ALL
    BOLD = Style.BRIGHT
    UNDERLINE = '\033[4m'
    CBLACK = Fore.BLACK
    CRED = Fore.RED
    CGREEN = Fore.GREEN
    CYELLOW = Fore.YELLOW
    CBLUE = Fore.BLUE
    CVIOLET = Fore.MAGENTA
    CBEIGE = Fore.CYAN
    CWHITE = Fore.WHITE

COLORS_RANDOM = [Colors.CBLUE, Colors.CVIOLET, Colors.CWHITE, Colors.OKBLUE, Colors.CGREEN, Colors.WARNING,
                Colors.CRED, Colors.CBEIGE]
random.shuffle(COLORS_RANDOM)

foxx = """The LFI scanner is a tool 
designed to identify potential Local File Inclusion
vulnerabilities in web applications.\n""" 

ASCII_ART = """
                                      
 ___   __           
 |__  /  \\ \\_/ LFI 🦊     
 |    \\__/ / \\     
 
 By Purple Fox
                                                           
"""
def fxpurple(text, color):
    print(f"{color}{text}{Colors.ENDC}")

def fox():
    fxpurple(ASCII_ART, random.choice(COLORS_RANDOM))
    print(foxx)


