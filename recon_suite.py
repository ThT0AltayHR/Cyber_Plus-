#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  RECON SUITE — Professional Security Reconnaissance Toolkit
  Eğitim ve savunma amaçlıdır. Yalnızca izinli sistemlerde kullanın.
============================================================
"""

import os
import sys
import time
import json
import socket
import random
import threading
import subprocess
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

try:
    import requests
    requests.packages.urllib3.disable_warnings()
except ImportError:
    print("[!] 'requests' modülü eksik. Kurmak için: pip install requests")
    sys.exit(1)

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print("[!] 'colorama' modülü eksik. Kurmak için: pip install colorama")
    sys.exit(1)

# ══════════════════════════════════════════════════════════════════
#  RENK PALETİ
# ══════════════════════════════════════════════════════════════════
R  = Fore.RED
G  = Fore.GREEN
Y  = Fore.YELLOW
B  = Fore.BLUE
C  = Fore.CYAN
M  = Fore.MAGENTA
W  = Fore.WHITE
BR = Fore.LIGHTRED_EX
BG = Fore.LIGHTGREEN_EX
BY = Fore.LIGHTYELLOW_EX
BB = Fore.LIGHTBLUE_EX
BC = Fore.LIGHTCYAN_EX
BM = Fore.LIGHTMAGENTA_EX
BW = Fore.LIGHTWHITE_EX
DIM = Style.DIM
BRIGHT = Style.BRIGHT
RESET = Style.RESET_ALL

# ══════════════════════════════════════════════════════════════════
#  50 ANA MENÜ ASCII TASARIMI HAVUZU
# ══════════════════════════════════════════════════════════════════
MAIN_ASCII_POOL = [
    f"""{R}
  ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
  ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝{RESET}""",

    f"""{C}
  ██████╗ ███████╗ ██████╗██╗   ██╗██████╗ ██╗████████╗██╗   ██╗
  ██╔══██╗██╔════╝██╔════╝██║   ██║██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝
  ██████╔╝███████╗██║     ██║   ██║██████╔╝██║   ██║    ╚████╔╝
  ██╔═══╝ ╚════██║██║     ╚██╗ ██╔╝██╔══██╗██║   ██║    ╚██╔╝
  ██║     ███████║╚██████╗ ╚████╔╝ ██║  ██║██║   ██║     ██║
  ╚═╝     ╚══════╝ ╚═════╝  ╚═══╝  ╚═╝  ╚═╝╚═╝   ╚═╝     ╚═╝{RESET}""",

    f"""{M}
  ██████╗ ██╗   ██╗███╗   ██╗████████╗███████╗
  ██╔══██╗██║   ██║████╗  ██║╚══██╔══╝██╔════╝
  ██████╔╝██║   ██║██╔██╗ ██║   ██║   █████╗
  ██╔══██╗██║   ██║██║╚██╗██║   ██║   ██╔══╝
  ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗
  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝{RESET}""",

    f"""{Y}
  ███████╗██╗   ██╗██╗████████╗███████╗
  ██╔════╝██║   ██║██║╚══██╔══╝██╔════╝
  ███████╗██║   ██║██║   ██║   █████╗
  ╚════██║██║   ██║██║   ██║   ██╔══╝
  ███████║╚██████╔╝██║   ██║   ███████╗
  ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝{RESET}""",

    f"""{G}
  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  ░  ██████╗░███████╗░█████╗░░█████╗░███╗  ░
  ░  ██╔══██╗██╔════╝██╔══██╗██╔══██╗████╗  ░
  ░  ██████╔╝█████╗░░██║░░╚═╝██║░░██║██╔██╗ ░
  ░  ██╔══██╗██╔══╝░░██║░░██╗██║░░██║██║╚██╗░
  ░  ██║░░██║███████╗╚█████╔╝╚█████╔╝██║░╚██╗
  ░  ╚═╝░░╚═╝╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝
  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░{RESET}""",

    f"""{BB}
  ┌─────────────────────────────────────────────┐
  │  ██████╗ ███████╗ ██████╗ ██████╗ ███╗     │
  │  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗    │
  │  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗   │
  │  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗  │
  │  ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚██╗ │
  └─────────────────────────────────────────────┘{RESET}""",

    f"""{BM}
  ╔═╗╔═╗╔═╗╔═╗╔╗╔   ╔═╗╦ ╦╦╔╦╗╔═╗
  ╠╦╝║╣ ║  ║ ║║║║   ╚═╗║ ║║ ║ ║╣
  ╩╚═╚═╝╚═╝╚═╝╝╚╝   ╚═╝╚═╝╩ ╩ ╚═╝{RESET}""",

    f"""{BR}
  ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗
  ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
  ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
  ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
  ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝{RESET}""",

    f"""{C}
  ▓█████▄ ▒█████   ███▄ ▄███▓ ▄▄▄       ██▓ ███▄    █
  ▒██▀ ██▌▒██▒  ██▒▓██▒▀█▀ ██▒▒████▄    ▓██▒ ██ ▀█   █
  ░██   █▌▒██░  ██▒▓██    ▓██░▒██  ▀█▄  ▒██▒▓██  ▀█ ██▒
  ░▓█▄   ▌▒██   ██░▒██    ▒██ ░██▄▄▄▄██ ░██░▓██▒  ▐▌██▒
  ░▒████▓ ░ ████▓▒░▒██▒   ░██▒ ▓█   ▓██▒░██░▒██░   ▓██░
   ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒░   ░  ░ ▒▒   ▓▒█░░▓  ░ ▒░   ▒ ▒{RESET}""",

    f"""{G}
  ____  ____  ____  ____  _  _     ____  __  __  ____  ____  ____
 (  _ \( ___)(  _ \(  _ \( \( )   / ___)(  )(  )(_  _)(_  _)( ___)
  )   / )__)  )___/ )   / )  (    \___ \ )(__)(   )(   _)(_   )__)
 (_)\_)(____)(__)  (_)\_)(_)\_)   (____/(______) (__) (____) (____)
{RESET}""",

    f"""{Y}
  ██▀███  ▓█████  ▄████▄   ▒█████   ███▄    █     ███████╗██╗   ██╗██╗████████╗███████╗
  ▓██ ▒ ██▒▓█   ▀ ▒██▀ ▀█  ▒██▒  ██▒ ██ ▀█   █     ██╔════╝██║   ██║██║╚══██╔══╝██╔════╝
  ▓██ ░▄█ ▒▒███   ▒▓█    ▄ ▒██░  ██▒▓██  ▀█ ██▒    ███████╗██║   ██║██║   ██║   █████╗
  ▒██▀▀█▄  ▒▓█  ▄ ▒▓▓▄ ▄██▒▒██   ██░▓██▒  ▐▌██▒    ╚════██║██║   ██║██║   ██║   ██╔══╝
  ░██▓ ▒██▒░▒████▒▒ ▓███▀ ░░ ████▓▒░▒██░   ▓██░    ███████║╚██████╔╝██║   ██║   ███████╗
  ░ ▒▓ ░▒▓░░░ ▒░ ░░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝{RESET}""",

    f"""{R}
  ██████████████████████████████████████████████████
  ██  ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗ ██
  ██  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║ ██
  ██  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ██
  ██  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██
  ██  ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║ ██
  ██████████████████████████████████████████████████{RESET}""",

    f"""{BC}
   ___  ___  ___  ___  ___  ___      ___  ___  ___  ___  ___
  | R || E || C || O || N || - |    | S || U || I || T || E |
  |___||___||___||___||___||___|    |___||___||___||___||___|
  {RESET}""",

    f"""{BG}
   _____  _____  _____  _____  _  _     _____  _  _  _  _____  _____
  | __  || __  ||     || __  || || |   |   __||  | || ||_   _||   __|
  |    -||    -||   --|| __ -|| || |__ |__   ||  | || |  | |  |   __|
  |__|__||__|__||_____||_____||_||_____|_____||_____||_|  |_|  |_____|
  {RESET}""",

    f"""{M}
  +-+-+-+-+-+ +-+-+-+-+-+
  |R|E|C|O|N| |S|U|I|T|E|
  +-+-+-+-+-+ +-+-+-+-+-+
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |P|r|o|f|e|s|s|i|o|n|a|l| |T|o|o|l|k|i|t|
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+{RESET}""",

    f"""{Y}
  ╔╦╗╦ ╦╔═╗  ╦ ╦╦ ╦╔╗╔╔╦╗╔═╗╦═╗
   ║ ╠═╣║╣   ╠═╣║ ║║║║ ║ ║╣ ╠╦╝
   ╩ ╩ ╩╚═╝  ╩ ╩╚═╝╝╚╝ ╩ ╚═╝╩╚═
  ╔═╗╔═╗╔═╗╦ ╦╦═╗╦╔╦╗╦ ╦  ╔╦╗╔═╗╔═╗╦╔═╔═╗╔╦╗
  ╚═╗║╣ ║  ║ ║╠╦╝║ ║ ╚╦╝   ║ ║ ║║ ║║╔╝║╣  ║
  ╚═╝╚═╝╚═╝╚═╝╩╚═╩ ╩  ╩    ╩ ╚═╝╚═╝╩╚╝╚═╝ ╩{RESET}""",

    f"""{C}
  ██╗      ██████╗ ██╗   ██╗███████╗██╗     ██╗  ██╗    ██╗ ██████╗
  ██║     ██╔═══██╗██║   ██║██╔════╝██║     ██║  ██║    ██║██╔═══██╗
  ██║     ██║   ██║██║   ██║█████╗  ██║     ███████║    ██║██║   ██║
  ██║     ██║   ██║╚██╗ ██╔╝██╔══╝  ██║     ██╔══██║    ██║██║   ██║
  ███████╗╚██████╔╝ ╚████╔╝ ███████╗███████╗██║  ██║    ██║╚██████╔╝
  ╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝ ╚═════╝{RESET}""",

    f"""{R}
  ░██████╗███████╗░█████╗░██╗░░░██╗██████╗░██╗████████╗██╗░░░██╗
  ██╔════╝██╔════╝██╔══██╗██║░░░██║██╔══██╗██║╚══██╔══╝╚██╗░██╔╝
  ╚█████╗░█████╗░░██║░░╚═╝██║░░░██║██████╔╝██║░░░██║░░░░╚████╔╝░
  ░╚═══██╗██╔══╝░░██║░░██╗██║░░░██║██╔══██╗██║░░░██║░░░░░╚██╔╝░░
  ██████╔╝███████╗╚█████╔╝╚██████╔╝██║░░██║██║░░░██║░░░░░░██║░░░
  ╚═════╝░╚══════╝░╚════╝░░╚═════╝░╚═╝░░╚═╝╚═╝░░░╚═╝░░░░░░╚═╝░░░{RESET}""",

    f"""{G}
  ██████  ██████████████████  ██████
  ██  ██  █                █  ██  ██
  ██████  █  RECON SUITE   █  ██████
  ██  ██  █  PROFESSIONAL  █  ██  ██
  ██████  █  SECURITY TOOL █  ██████
  ██  ██  █                █  ██  ██
  ██████  ██████████████████  ██████{RESET}""",

    f"""{BC}
   ▄▄▄       ██▓  █████   ██████  ██▓ ██████ ▓██   ██▓
  ▒████▄    ▓██▒▒██▓  ██▒▒██    ▒ ▓██▒▒██    ▒  ▒██  ██▒
  ▒██  ▀█▄  ▒██▒▒██▒  ██░░ ▓██▄   ▒██▒░ ▓██▄     ▒██ ██░
  ░██▄▄▄▄██ ░██░░██  █▀ ░  ▒   ██▒░██░  ▒   ██▒  ░ ▐██▓░
   ▓█   ▓██▒░██░░▒███▒█▄ ▒██████▒▒░██░▒██████▒▒  ░ ██▒▓░
   ▒▒   ▓▒█░░▓  ░░ ▒▒░ ▒ ▒ ▒▓▒ ▒ ░░ ▒░▒ ▒▓▒ ▒ ░   ██▒▒▒{RESET}""",

    f"""{BM}
  ┌──────────────────────────────────────────────────────┐
  │                                                      │
  │     ____  _____ ____ ___  _   _   ____  _   _ ___ │
  │    |  _ \| ____/ ___/ _ \| \ | | / ___|| | | |_ _| │
  │    | |_) |  _|| |  | | | |  \| | \___ \| | | || |  │
  │    |  _ <| |__| |__| |_| | |\  |  ___) | |_| || |  │
  │    |_| \_\_____\____\___/|_| \_| |____/ \___/|___| │
  │                                                      │
  └──────────────────────────────────────────────────────┘{RESET}""",

    f"""{Y}
  ██████╗ ██╗     ██╗   ██╗███████╗████████╗███████╗ █████╗ ███╗   ███╗
  ██╔══██╗██║     ██║   ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
  ██████╔╝██║     ██║   ██║█████╗     ██║   █████╗  ███████║██╔████╔██║
  ██╔══██╗██║     ██║   ██║██╔══╝     ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
  ██████╔╝███████╗╚██████╔╝███████╗   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
  ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝{RESET}""",

    f"""{R}
  [*]═══════════════════════════════════════════════[*]
  [*]   ____  ____ ___ _    ___   ____ _____  ___  [*]
  [*]  |  _ \| ___|_ _| |  / _ \ / ___| ____||   \ [*]
  [*]  | |_) |  _| | || | | | | |\___ \|  _|  | O | [*]
  [*]  |  _ <| |___| || |__| |_| | ___) | |___ | V | [*]
  [*]  |_| \_\____|___|_____\___/ |____/|_____|___/ [*]
  [*]═══════════════════════════════════════════════[*]{RESET}""",

    f"""{C}
  ◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼
  ◼     ██████╗ ███████╗ ██████╗ ██████╗ ███╗       ◼
  ◼     ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗      ◼
  ◼     ██████╔╝█████╗  ██║     ██║   ██║██╔██╗     ◼
  ◼     ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗    ◼
  ◼     ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚██╗   ◼
  ◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼{RESET}""",

    f"""{BG}
  ╭━━━╮╭━━━┳━━━┳━━━┳━╮╱╭┱━━━╮
  ┃╭━╮┃┃╭━━┫╭━╮┃╭━╮┃┃╰╮┃┃╭━╮┃
  ┃╰━━╮┃╰━━┫┃╱╰┫┃╱┃┃╭╮╰╯┃╰━━╮
  ╰━━╮┃┃╭━━┫┃╱╭┫┃╱┃┃┃╰╮┃┃╰━━╮
  ┃╰━╯┃┃╰━━┫╰━╯┃╰━╯┃┃╱┃┃┃╰━╯┃
  ╰━━━╯╰━━━┻━━━┻━━━┻╯╱╰━┻━━━╯{RESET}""",

    f"""{M}
  MMMMMMMM   MMMMMMMM   RRRRRRRRR   EEEEEEEEE   CCCCCCCC   OOOOOOO   NNNN   NNNN
  MM      MM MM      MM RR      RR  EE          CC         OO     OO  NN NN  NN
  MM  MM  MM MM  MM  MM RRRRRRRRR   EEEEEE      CC         OO     OO  NN  NN NN
  MM   MMMM  MM   MMMM  RR   RR     EE          CC         OO     OO  NN   NNNN
  MM         MM         RR    RR    EEEEEEEEE    CCCCCCCC    OOOOOOO   NN    NNN{RESET}""",

    f"""{BB}
  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
  █▄─▄▄▀█▄─▄▄─█─▄▄▀█─▄▄─█▄─▀█▄─▄█   █─▄▄▄▄█▄─██─▄█
  ██─▄─▀██─▄█▀█─▀─▄█─██─██─█▄▀─██─▄─█▄▄▄▄─██─██─██
  ▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▀▄▄▄▀▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▄▀▄▄▀{RESET}""",

    f"""{BR}
  ████████████████████████████████████████████████████
  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█
  █░  ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗  ░█
  █░  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║  ░█
  █░  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║  ░█
  █░  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║  ░█
  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█
  ████████████████████████████████████████████████████{RESET}""",

    f"""{G}
  ─────────────────────────────────────────────────────
    ____  _____  __  ___  _  _     ____  _  _  ____  ____  ____
   |  _ \| ____||  |/ _ \| \| |   / ___|| || ||_  _||_  _||  __|
   | |_) |  _|  |  | | | |    \  \___ \ || ||  | |   | |  |  _|
   |  _ <| |___ |  | |_| | |\  \  ___) |_   _|  | |   | |  | |___
   |_| \_|_____||___\___/|_| \_| |____/  |_|    |_|  |_|  |_____|
  ─────────────────────────────────────────────────────{RESET}""",

    f"""{Y}
    ██████████████████████████████████████
   ██                                    ██
  ██   ██████╗ ███████╗ ██████╗ ██████╗  ██
  ██   ██╔══██╗██╔════╝██╔════╝██╔═══██╗ ██
  ██   ██████╔╝█████╗  ██║     ██║   ██║ ██
  ██   ██╔══██╗██╔══╝  ██║     ██║   ██║ ██
  ██   ██║  ██║███████╗╚██████╗╚██████╔╝ ██
   ██                                    ██
    ██████████████████████████████████████{RESET}""",

    f"""{C}
  ┌─┐┌─┐┌─┐┌─┐┌┐┌   ┌─┐┬ ┬┬┌┬┐┌─┐
  ├┬┘├┤ │  │ ││││   └─┐│ ││ │ ├┤
  ┴└─└─┘└─┘└─┘┘└┘   └─┘└─┘┴ ┴ └─┘
  ┌─────────────────────────────────┐
  │  PROFESSIONAL SECURITY TOOLKIT  │
  │  Subdomain Hunter | Web Recon   │
  └─────────────────────────────────┘{RESET}""",

    f"""{M}
  ╔══╗░╔══╗░╔══╗░╔══╗░╔╗░░╔╗   ╔══╗░╔╗░░╔╗░╔══╗░╔══╗░╔══╗
  ║╔╗║░║╔╗╚╗║╔╗║░║╔╗║░║╚╗╔╝║   ║╔╗╚╗║╚╗╔╝║░║╔╗╚╗║╔╗╚╗║╔╗╚╗
  ║╚╝╚╗║╚╝╔╝║╚╝╚╗║╚╝║░║░╔╗░║   ║╚╝╔╝║░╚╝░║░║╚╝╔╝║╚╝╔╝║╚╝╔╝
  ║╔═╗║║╔═╝░║╔═╗║║╔╗║░║░║║░║   ║╔═╝░║╔╗╔╗║░║╔═╝░║╔═╝░║╔═╝░
  ║╚═╝║║╚══╗║╚═╝║║╚╝╚╗║╝╚╝░║   ║╚══╗║╝╚╝╚╝░║╚══╗║╚══╗║╚══╗
  ╚═══╝╚═══╝╚═══╝╚════╝╚════╝   ╚═══╝╚════╝░╚═══╝╚═══╝╚═══╝{RESET}""",

    f"""{R}
  ██████████████████████████████████████████████████████████
  ██ ____  ____  _____  _   _    ____  _  _  ___  _____  ██
  ██|  _ \| ___||  _  || \_/ |  / ___|| || ||_ _||_   _| ██
  ██| |_) |  _| | | | ||  _  | \___ \| || | | |   | |   ██
  ██|  _ <| |___| |_| || | | |  ___) ||_  _|| |   | |   ██
  ██|_| \_|_____|\___/ |_| |_| |____/   |_||___|  |_|   ██
  ██████████████████████████████████████████████████████████{RESET}""",

    f"""{BC}
  ╔════╗╔════╗╔════╗╔════╗╔═╗  ╔═╗
  ║╔══╝╝║╔══╝╝║╔══╗║║╔══╗║║ ╚╗╔╝ ║
  ║╚══╗ ║╚══╗ ║║  ║║║║  ║║║  ╚╝  ║
  ╠══╗║ ╠══╗║ ║║  ║║║║  ║║║ ╔╗╔╗ ║
  ║  ╚╝ ║  ╚╝ ║╚══╝║║╚══╝║║ ║║║║ ║
  ╚════╝╚════╝╚════╝╚════╝╚═╝╚╝╚╝╚═╝{RESET}""",

    f"""{G}
   _____  ______  _____  _____  _   _   _____  _   _  _____  _____  _____
  |  __ \|  ____|/ ____|/ ____|| \ | | |_   _|| | | ||_   _||_   _||  ___|
  | |__) | |__  | |    | |     |  \| |   | |  | | | |  | |    | |  | |___
  |  _  /|  __| | |    | |     | . ` |   | |  | | | |  | |    | |  |  ___|
  | | \ \| |____| |____| |____ | |\  |  _| |_ | |_| | _| |_  _| |_ | |___
  |_|  \_|______|\_____|\_____||_| \_| |_____| \___/ |_____||_____||_____|{RESET}""",

    f"""{Y}
  ▀█████████▄     ▄████████    ▄████████    ▄████████  ███▄▄▄▄
    ███    ███   ███    ███   ███    ███   ███    ███ ███▀▀▀██▄
    ███    ███   ███    █▀    ███    ███   ███    ███ ███   ███
   ▄███▄▄▄██▀  ▄███▄▄▄       ███    ███   ███    ███ ███   ███
  ▀▀███▀▀▀██▄ ▀▀███▀▀▀     ▀███████████ ▀███████████ ███   ███
    ███    ██▄   ███    █▄    ███    ███   ███    ███ ███   ███
    ███    ███   ███    ███   ███    ███   ███    ███ ███   ███
  ▄█████████▀    ██████████   ███    █▀    ███    █▀   ▀█   █▀ {RESET}""",

    f"""{M}
  ████████████████████████████████████████████████████████████████
  █ ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗   ███████╗ █████╗ █
  █ ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║   ██╔════╝██╔══██╗█
  █ ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║   ███████╗██║  ╚═╝█
  █ ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║   ╚════██║██║  ██╗█
  █ ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║   ███████║╚█████╔╝█
  ████████████████████████████████████████████████████████████████{RESET}""",

    f"""{BR}
  :'######:::'##::::'##::'####:'########:'########::
  '##... ##::. ##::'##::. ##::... ##..:: ##.....:::
   ##:::..::::. ##'##::::: ##::::: ##:::: ##::::::::
  . ######:::::. ###:::::: ##::::: ##:::: ######::::
  :..... ##::::: ##::::::: ##::::: ##:::: ##...::::
  '##::: ##::::: ##::::::: ##::::: ##:::: ##::::::::
  . ######:::::: ##:::::'####:::: ##:::: ########::
  :......:::::::..::::::.....::::..:::::........::::{RESET}""",

    f"""{C}
  ╔═══╦═══╦═══╦═══╦═╗░╔╦═══╦═══╦═══╦╦══╦══╗
  ╚╗╔╗╠╗╔╗║╔═╗║╔══╩╗╚╗║║╔═╗║╔═╗║╔═╗╠╣╔╗║╔╗║
  ░║║╚╣║║║║╚══╣║╔══╝╔╝╚╝║║░║║╚══╣╚═╝║║╚╝║║║╝
  ░║╔╗╣║║║║╔══╣║╚══╦╝╔╗╔╣║░║╠══╗║╔╗╔╣║╔╗║║║╗
  ╔╝╚╝╠╝╚╝║╚═╗║╚═══╩═╝╚╝║╚═╝║╚═╝║║╚╝║╚╝╚╩╩╝╚╗
  ╚═══╩═══╩═══╩════════════════╩═══╩═╝░░╚════╝{RESET}""",

    f"""{BG}
  ·····················································
  ·  ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗  ·
  ·  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║  ·
  ·  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║  ·
  ·  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║  ·
  ·····················································{RESET}""",

    f"""{R}
   __    ___    __    __  __  ___    ____  _  _  ____  ____  ____
  |__\  | __| /  \  /  \|  \| __\  / ___|| || ||_  _||_  _||  __|
  |   \ | |_  | () | () ||   | |_   \___ \| || | | |   | |  |  _|
  |__/_/ |___| \__/ \__/ |_|\|__|   |____/|_||_| |_|  |_|  |_____|{RESET}""",

    f"""{Y}
  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  ░ ___  ___  ___  ___  ___       ___  _ _ _  ___  ░
  ░|   \| __|| __|| __||   \     / __|| | | ||_ _| ░
  ░| |) | _| | _| | _| | |) |    \__ \| | | | | |  ░
  ░|___/|___||___||___||___/     |___/|_____||___|  ░
  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░{RESET}""",

    f"""{BC}
   ____ ____ ____ ____ __ _    ____ _  _ _ ___ ____
   |--< |=== |___ [__] | \|    ==== |__| | |==  |===
   {RESET}""",

    f"""{M}
  ╭╮╭╮╭╮╭━━━╮╭━━━╮╭━━╮╭━━━╮╭╮  ╭╮
  ┃┃┃┃┃┃┃╭━╮┃┃╭━━╝┃╭╮┃┃╭━╮┃┃╰╮╭╯┃
  ┃┃┃┃┃┃┃┃ ┃┃┃╰━━╮┃╰╯╚╮┃┃ ┃┃┃╭╯╰╮┃
  ┃┃┃┃┃┃┃┃ ┃┃┃╭━━╝┃╭━╮┃┃┃ ┃┃┃┃  ┃┃
  ┃╰╯╰╯┃┃╰━╯┃┃╰━━╮┃╰━╯┃┃╰━╯┃┃╰╮╭╯┃
  ╰━━━━━╯╰━━━╯╰━━━╯╰━━━╯╰━━━╯╰━╯╰━╯{RESET}""",

    f"""{G}
  ██╗  ██╗ █████╗ ██╗  ██╗███████╗██████╗     ██████╗ ██╗   ██╗███╗   ██╗████████╗███████╗██████╗
  ██║  ██║██╔══██╗██║ ██╔╝██╔════╝██╔══██╗    ██╔══██╗██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
  ███████║███████║█████╔╝ █████╗  ██████╔╝    ██████╔╝██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
  ██╔══██║██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗    ██╔══██╗██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
  ██║  ██║██║  ██║██║  ██╗███████╗██║  ██║    ██████╔╝╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝{RESET}""",

    f"""{R}
  ╔══════════════════════════════════════════════════╗
  ║  ___  ___  ___  ___  ___     ___  _  _  _  ___ ║
  ║ | _ \| __|| __||  _|| _ \   / __|/ \| || ||_ _|║
  ║ |   /| _| | _| | |  |   /   \___ | _ | \/ | | | ║
  ║ |_|_\|___||___||___|_|_\_\  |___||_|_|\__/ |___|║
  ╚══════════════════════════════════════════════════╝{RESET}""",

    f"""{C}
  .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
  |  ____  ____ ____ ___  _  _     ___ _  _ ___ _|
  | |  _ \| ___|  _ \  _ \| \| |   / __| || |_ _|_ _||
  | | |_) |  _| | |_) | | | |    | (__| __ | | | | | |
  | |  _ <| |___| _ <| |_| | |\  |  \___| || |_| | | | |
  | |_| \_|_____|_| \_|___/|_| \_|  \___|_||_|___| |_||
  .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-{RESET}""",

    f"""{BM}
  ██████████████████████████████████████████████████████
  ██                                                  ██
  ██   ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗   ██
  ██   ╚════██╗╚════██║██╔════╝╚════██╗████╗  ██║   ██
  ██    █████╔╝    ██╔╝╚█████╗  █████╔╝██╔██╗ ██║   ██
  ██   ██╔═══╝    ██╔╝  ╚═══██╗██╔═══╝ ██║╚██╗██║   ██
  ██   ███████╗   ██║  ██████╔╝███████╗██║ ╚████║   ██
  ██   ╚══════╝   ╚═╝  ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ██
  ██                                                  ██
  ██████████████████████████████████████████████████████{RESET}""",

    f"""{G}
  ▐▓█▀▀▀▀▀▀▀▀▀█▓▌░▄▄▄▄░░░░░░░░░░░░░░░░░░░░░░░░░░░
  ▐▓█░░░░░░░░░░░█▓▌░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  ▐▓█░░░██████░░░█▓▌░██████╗ ███████╗ ██████╗ ██╗░░
  ▐▓█░░░██████░░░█▓▌░██╔══██╗██╔════╝██╔════╝██╗░░
  ▐▓█░░░██████░░░█▓▌░██████╔╝█████╗  ██║     ███╗░
  ▐▓█░░░░░░░░░░░█▓▌░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  ▐▓█▄▄▄▄▄▄▄▄▄█▓▌░▀▀▀▀▀▀░░░░░░░░░░░░░░░░░░░░░░░░░{RESET}""",

    f"""{Y}
  ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗     ██████╗  ██████╗
  ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗   ██╔══██╗██╔════╝
  ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝   ██████╔╝██║
  ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗   ██╔═══╝ ██║
  ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║██╗██║     ╚██████╗
  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝╚═╝      ╚═════╝{RESET}""",

    f"""{C}
   ╔═╗╔═╗═╗ ╦   ╦  ╦╔═╗╔╗╔╔╦╗╔═╗╦═╗  ╦  ╔═╗╔═╗╦╔═╗
   ╚═╗╠═ ╔╩╦╝   ╠═╣║ ║║║║ ║ ║╣ ╠╦╝  ║  ║ ║║ ╦║║
   ╚═╝╚═╝╩ ╚═   ╩ ╩╚═╝╝╚╝ ╩ ╚═╝╩╚═  ╩═╝╚═╝╚═╝╩╚═╝{RESET}""",

    f"""{G}
  ▀▀█▀▀ █──█ █▀▀   █──█ █──█ █▄─█ ▀▀█▀▀ █▀▀ █▀▀█
  ──█── █▀▀█ █▀▀   █▀▀█ █──█ █─▀█ ──█── █▀▀ █▄▄▀
  ──▀── ▀──▀ ▀▀▀   ▀──▀ ─▀▀▀ ▀──▀ ──▀── ▀▀▀ ▀─▀▀{RESET}""",

    f"""{M}
  ┌─────────────────────────────────────────────────────────┐
  │  ████████╗██╗  ██╗███████╗    ██╗  ██╗██╗   ██╗███╗   │
  │  ╚══██╔══╝██║  ██║██╔════╝    ██║  ██║██║   ██║████╗  │
  │     ██║   ███████║█████╗      ███████║██║   ██║██╔██╗ │
  │     ██║   ██╔══██║██╔══╝      ██╔══██║██║   ██║██║╚██╗│
  │     ██║   ██║  ██║███████╗    ██║  ██║╚██████╔╝██║ ╚██│
  └─────────────────────────────────────────────────────────┘{RESET}""",
]

# ══════════════════════════════════════════════════════════════════
#  20 MODÜL ASCII TASARIMI HAVUZU
# ══════════════════════════════════════════════════════════════════
MODULE_ASCII_POOL = [
    f"""{C}
  ╔═══════════════════════════════════╗
  ║   [MODULE ACTIVE] >>> RUNNING    ║
  ╚═══════════════════════════════════╝{RESET}""",

    f"""{G}
  ┌─────────────────────────────────┐
  │ ▶▶▶  SCANNING IN PROGRESS  ◀◀◀ │
  └─────────────────────────────────┘{RESET}""",

    f"""{Y}
  ╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
  ┃  ⚡  RECON ENGINE ACTIVATED  ⚡  ┃
  ╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯{RESET}""",

    f"""{M}
  ████████  ███  ████  ████████  ███████
  ██    ██  ███  ████  ██    ██  ██
  ████████  ███  ████  ████████  ███████{RESET}""",

    f"""{R}
  [!]═══════════════════════════════[!]
  [!]   DEEP SCAN MODULE ONLINE    [!]
  [!]═══════════════════════════════[!]{RESET}""",

    f"""{BC}
  ◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
  ◈   INTELLIGENCE GATHERING ACTIVE   ◈
  ◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈{RESET}""",

    f"""{BG}
  ╔════╗╔════╗╔══╗╔═══╗╔════╗
  ║╔══╝╝║╔══╝╝║╔╗║║╔══╝╝║╔══╝╝
  ║╚══╗ ║║    ║║║║║╚══╗ ║╚══╗
  ╚══╗║ ║║    ║║║║╠══╗║ ╠══╗║
  ╔══╝║ ║╚══╗ ║╚╝║║╔══╝╝║╔══╝╝
  ╚════╝╚════╝╚══╝╚═══╝╚════╝{RESET}""",

    f"""{Y}
  ──────────────────────────────────────
  >>> TARGET ACQUIRED — INITIATING <<<
  ──────────────────────────────────────{RESET}""",

    f"""{M}
  ·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·
  ·   PROFESSIONAL RECON TOOLKIT    ·
  ·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·{RESET}""",

    f"""{C}
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ~   NETWORK ANALYSIS UNDERWAY   ~
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{RESET}""",

    f"""{R}
  ╔╗╔╗╔╗╔╗╔╗╔╗╔╗╔╗╔╗╔╗╔╗╔╗╔╗╔╗╔╗╔╗╔╗
  ║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║
  ╠╣╠╣    SCAN ENGINE ONLINE    ╠╣╠╣
  ║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║
  ╚╝╚╝╚╝╚╝╚╝╚╝╚╝╚╝╚╝╚╝╚╝╚╝╚╝╚╝╚╝╚╝╚╝{RESET}""",

    f"""{BM}
  ╔══════════════════════════════════╗
  ║ ██████╗  ██████╗  ███╗   ██╗   ║
  ║ ██╔══██╗██╔═══██╗ ████╗  ██║   ║
  ║ ██████╔╝██║   ██║ ██╔██╗ ██║   ║
  ╚══════════════════════════════════╝{RESET}""",

    f"""{G}
  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  ░  ♦ DEEP INTELLIGENCE MODULE ♦  ░
  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░{RESET}""",

    f"""{Y}
  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
  █ >>> SECURITY SCANNER v9.1 <<< █
  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{RESET}""",

    f"""{C}
  ┌────────────────────────────────┐
  │ ▓▓▓  PAYLOAD GENERATOR ▓▓▓   │
  └────────────────────────────────┘{RESET}""",

    f"""{BR}
  ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
    BLUE TEAM DEFENSE MODULE LIVE
  ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡{RESET}""",

    f"""{M}
  ╔═╗╔═╗╔╗╔  ╔═╗╔═╗╔═╗╔╗╔  ╔═╗╦═╗╔═╗╦ ╦╔═╗╦
  ╚═╗║  ╠╩╗  ╚═╗║  ╠═╣║║║  ╠═╣╠╦╝║╣ ╚╦╝║╣ ║
  ╚═╝╚═╝╩ ╩  ╚═╝╚═╝╩ ╩╝╚╝  ╩ ╩╩╚═╚═╝ ╩ ╚═╝╩═╝{RESET}""",

    f"""{G}
  ╔╦╗╔═╗╦═╗╔═╗╔═╗╔╦╗  ╦  ╔═╗╔═╗╦╔═╔═╗╦═╗
   ║ ╠═╣╠╦╝║ ╦║╣  ║   ║  ║ ║║  ╠╩╗║╣ ╠╦╝
   ╩ ╩ ╩╩╚═╚═╝╚═╝ ╩   ╩═╝╚═╝╚═╝╩ ╩╚═╝╩╚═{RESET}""",

    f"""{BC}
  ╭──────────────────────────────────────╮
  │  ╔═╗╔╦╗╔═╗╦═╗╔╦╗   ╔═╗╔═╗╔═╗╔╗╔   │
  │  ╚═╗ ║ ╠═╣╠╦╝ ║    ╚═╗║  ╠═╣║║║   │
  │  ╚═╝ ╩ ╩ ╩╩╚═ ╩    ╚═╝╚═╝╩ ╩╝╚╝   │
  ╰──────────────────────────────────────╯{RESET}""",

    f"""{Y}
  ████████████████████████████████████████
  ██                                    ██
  ██   RECON SUITE — TARGET LOCKED      ██
  ██                                    ██
  ████████████████████████████████████████{RESET}""",
]

# ══════════════════════════════════════════════════════════════════
#  YARDIMCI FONKSİYONLAR
# ══════════════════════════════════════════════════════════════════
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner_main():
    clear()
    print(random.choice(MAIN_ASCII_POOL))

def banner_module():
    print(random.choice(MODULE_ASCII_POOL))

def header(title):
    w = 60
    print(f"\n{C}{'═'*w}")
    print(f"{BRIGHT}{C}{'  ' + title.upper():^{w}}")
    print(f"{C}{'═'*w}{RESET}\n")

def info(msg):    print(f"  {BC}[i]{RESET} {msg}")
def success(msg): print(f"  {BG}[✓]{RESET} {BG}{msg}{RESET}")
def warn(msg):    print(f"  {BY}[!]{RESET} {BY}{msg}{RESET}")
def error(msg):   print(f"  {BR}[✗]{RESET} {BR}{msg}{RESET}")
def found(msg):   print(f"  {BM}[+]{RESET} {BM}{msg}{RESET}")

def separator(char="─", color=C):
    print(f"{color}{'─'*60}{RESET}")

def pause():
    print(f"\n  {DIM}[ENTER'a basın...]{RESET}", end="")
    input()

def get_target(prompt="Hedef domain (örn: example.com)"):
    print(f"\n  {BC}[?]{RESET} {prompt}: ", end="")
    return input().strip()

def spinner_start(msg):
    chars = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    stop_flag = threading.Event()
    def _spin():
        i = 0
        while not stop_flag.is_set():
            sys.stdout.write(f"\r  {C}{chars[i % len(chars)]}{RESET} {msg}  ")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write(f"\r  {BG}[✓]{RESET} {msg} - Tamamlandı.\n")
        sys.stdout.flush()
    t = threading.Thread(target=_spin, daemon=True)
    t.start()
    return stop_flag, t

def spinner_stop(stop_flag, thread):
    stop_flag.set()
    thread.join()

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def resolve_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

# ══════════════════════════════════════════════════════════════════
#  MENÜ 1 — BU ARAÇ NE İŞE YARIYOR
# ══════════════════════════════════════════════════════════════════
def menu_about():
    banner_module()
    header("Bu Araç Ne İşe Yarıyor?")
    print(f"""
  {BW}RECON SUITE{RESET} — Profesyonel Güvenlik Keşif Araç Seti

  {C}▸  Subdomain Hunter (Alt Alan Adı Keşfi){RESET}
     ├── Pasif Keşif: crt.sh Certificate Transparency logları
     ├── Aktif DNS Çözümleme: A, AAAA, CNAME kayıt sorgulaması
     └── Paralel thread desteği ile hız optimizasyonu

  {G}▸  Web-Recon (Web Zafiyet/Yapı Keşfi){RESET}
     ├── HTTP durum kodu analizi (200/301/302/403/404/500)
     ├── Content-Length temelli custom-404 tespiti
     ├── Server/X-Powered-By başlık analizi
     └── Teknoloji parmak izi (fingerprinting)

  {Y}▸  İstihbari Modüller{RESET}
     ├── WHOIS sorgulama
     ├── DNS kayıt haritalaması (A/MX/NS/TXT/SOA)
     ├── Banner Grabbing (port/servis tespiti)
     └── IP geolocation ve ASN analizi

  {M}▸  Savunma Araçları (Blue Team){RESET}
     ├── WAF tespit algoritması
     ├── Rate-limit güvenlik analizi
     ├── Security başlık kontrolü
     └── SSL/TLS güvenlik denetimi

  {R}▸  Uluslararası Araçlar{RESET}
     ├── Shodan-benzeri banner grabbing
     ├── VirusTotal benzeri hash sorgulama
     └── OSINT kaynak analizi

  {DIM}Not: Tüm araçlar yalnızca yetkili sistemlerde kullanılmalıdır.{RESET}
    """)
    pause()

# ══════════════════════════════════════════════════════════════════
#  MENÜ 2 — NASIL KULLANILIR
# ══════════════════════════════════════════════════════════════════
def menu_howto():
    banner_module()
    header("Bu Araç Nasıl Kullanılır?")
    print(f"""
  {BY}KULLANIM REHBERİ{RESET}

  {BW}1. Gereksinimler:{RESET}
     {G}pip install requests colorama{RESET}
     Python 3.7+ gereklidir.

  {BW}2. Temel Kullanım Akışı:{RESET}
     {BC}a){RESET} Ana menüden modül seçin (1-9 arası)
     {BC}b){RESET} Hedef domain/IP girin
     {BC}c){RESET} Tarama parametrelerini ayarlayın
     {BC}d){RESET} Sonuçları ekranda veya dosyada görüntüleyin

  {BW}3. Subdomain Hunter Kullanımı:{RESET}
     ┌─────────────────────────────────────────────┐
     │ Hedef: example.com                         │
     │ Yöntem: Pasif (crt.sh) veya Aktif (brute)  │
     │ Thread Sayısı: 50 (önerilen)               │
     │ Çıktı: Ekran + isteğe bağlı .txt dosyası   │
     └─────────────────────────────────────────────┘

  {BW}4. Web-Recon Kullanımı:{RESET}
     ┌─────────────────────────────────────────────┐
     │ Hedef: https://example.com                 │
     │ Wordlist: Dahili (built-in) liste           │
     │ Thread: 20 (önerilen, dikkatli kullanın)    │
     │ Timeout: 5 saniye (önerilen)               │
     └─────────────────────────────────────────────┘

  {BW}5. Sonuç Kaydetme:{RESET}
     Her modülde {G}[S]{RESET} tuşu ile sonuçları .txt olarak kaydedin
     Dosyalar: {BY}recon_output_YYYY-MM-DD.txt{RESET}

  {BW}6. Hız Ayarı:{RESET}
     {G}Düşük{RESET}: 5-10 thread  (dikkatli/stealth mod)
     {Y}Orta{RESET}:  20-50 thread (standart)
     {R}Yüksek{RESET}: 100+ thread (agresif, dikkat!)
    """)
    pause()

# ══════════════════════════════════════════════════════════════════
#  MENÜ 3 — ÖNEMLİ KURALLAR
# ══════════════════════════════════════════════════════════════════
def menu_rules():
    banner_module()
    header("Önemli Kurallar — Yasal Uyarı")
    print(f"""
  {BR}╔═════════════════════════════════════════════════════════╗
  ║          !!!  YASAL UYARI — OKUMAK ZORUNLUDUR  !!!      ║
  ╚═════════════════════════════════════════════════════════╝{RESET}

  {BW}Bu araç yalnızca:{RESET}
  {G}  ✔  Kendi sistemlerinizde{RESET}
  {G}  ✔  Yazılı izin aldığınız sistemlerde (pentest sözleşmesi){RESET}
  {G}  ✔  Eğitim ortamlarında (CTF, lab, sanal makine){RESET}
  {G}  ✔  Bug Bounty programlarına katılan sistemlerde{RESET}
  kullanılmalıdır.

  {BR}  ✗  İzinsiz sistemlerde kullanmak YASA DIŞIDIR.{RESET}
  {BR}  ✗  Türk Ceza Kanunu 243-245. maddeler uygulanabilir.{RESET}
  {BR}  ✗  GDPR, KVKK ve uluslararası siber suç yasaları geçerlidir.{RESET}

  {BW}Etik Kurallar:{RESET}
  {C}  1. Hedefi asla aşırı yükleyin (DoS etkisi yaratmayın){RESET}
  {C}  2. Bulguları sorumlu ifşa (Responsible Disclosure) ile bildirin{RESET}
  {C}  3. Elde edilen verileri üçüncü kişilerle paylaşmayın{RESET}
  {C}  4. Rate limiting kurallarına uyun{RESET}
  {C}  5. Aracı otomatize saldırı için kullanmayın{RESET}

  {BW}Geliştirici Sorumluluk Reddi:{RESET}
  {DIM}Bu araç eğitim ve savunma (Blue Team) amaçlı geliştirilmiştir.
  Kötüye kullanımdan kaynaklanan tüm hukuki sorumluluk kullanıcıya aittir.{RESET}

  {BY}[Devam etmek için ENTER'a basın]{RESET}
    """)
    pause()

# ══════════════════════════════════════════════════════════════════
#  SUBDOMAIN HUNTER — CORE ENGINE
# ══════════════════════════════════════════════════════════════════
def crtsh_lookup(domain):
    """crt.sh Certificate Transparency pasif keşfi"""
    results = set()
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        r = requests.get(url, timeout=15, verify=False)
        if r.status_code == 200:
            data = r.json()
            for entry in data:
                names = entry.get("name_value", "")
                for name in names.split("\n"):
                    name = name.strip().lower()
                    if name.endswith(f".{domain}") or name == domain:
                        if "*" not in name:
                            results.add(name)
    except Exception as e:
        error(f"crt.sh hatası: {e}")
    return results

def dns_resolve(hostname):
    """Tek bir hostname için DNS çözümleme"""
    try:
        ip = socket.gethostbyname(hostname)
        return hostname, ip
    except:
        return hostname, None

def subdomain_bruteforce(domain, wordlist, threads=30):
    """Aktif DNS brute-force"""
    found_subs = []
    targets = [f"{word}.{domain}" for word in wordlist]

    def check(host):
        h, ip = dns_resolve(host)
        if ip:
            return h, ip
        return None

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check, t): t for t in targets}
        for future in as_completed(futures):
            result = future.result()
            if result:
                found_subs.append(result)
                found(f"{result[0]}  →  {result[1]}")
    return found_subs

# Geniş built-in wordlist
SUBDOMAIN_WORDLIST = [
    "www","mail","ftp","smtp","pop","ns1","ns2","webmail","admin","vpn",
    "api","dev","test","staging","beta","prod","app","cdn","static","img",
    "media","assets","upload","login","auth","portal","dashboard","panel",
    "ssh","rdp","remote","support","help","forum","blog","shop","store",
    "payment","checkout","account","secure","ssl","mx","mx1","mx2","pop3",
    "imap","autodiscover","autoconfig","relay","smtp2","email","newsletter",
    "lists","internal","intranet","corp","extranet","db","database","sql",
    "mysql","postgres","redis","cache","memcache","elasticsearch","kibana",
    "grafana","prometheus","jenkins","gitlab","git","svn","jira","confluence",
    "wiki","docs","documentation","files","backup","archive","old","legacy",
    "new","mobile","m","wap","pda","ios","android","api2","v1","v2","v3",
    "api-v1","api-v2","rest","graphql","ws","websocket","socket","chat",
    "crm","erp","hr","finance","marketing","sales","ops","monitoring","log",
    "logs","syslog","nagios","zabbix","splunk","graylog","kibana2","elastic",
    "uat","qa","dev2","staging2","demo","sandbox","poc","preview","pre-prod",
    "load-balancer","lb","lb1","lb2","proxy","reverse-proxy","gateway",
    "firewall","vpn2","citrix","f5","haproxy","nginx","apache","iis",
    "cloud","aws","azure","gcp","k8s","kubernetes","docker","container",
    "registry","hub","repo","repository","packages","pkg","npm","pypi",
    "cdn1","cdn2","origin","edge","network","net","connect","connectivity",
    "analytics","tracker","tracking","pixel","tag","gtm","metrics","stats",
]

def run_subdomain_hunter():
    banner_module()
    header("Subdomain Hunter — Alt Alan Adı Keşfi")
    print(f"""
  {C}Tarama Modları:{RESET}
  {G}[1]{RESET} Pasif Keşif (crt.sh — hedeften gizli)
  {G}[2]{RESET} Aktif DNS Brute-Force
  {G}[3]{RESET} Kombine (Pasif + Aktif)
    """)
    domain = get_target("Hedef domain (örn: google.com)")
    if not domain:
        error("Domain boş olamaz!")
        pause()
        return

    mod = input(f"  {BC}[?]{RESET} Mod seçin [1/2/3]: ").strip()

    print(f"\n  {DIM}Başlangıç: {timestamp()}{RESET}")
    all_found = set()
    results_log = []

    # Pasif
    if mod in ["1", "3"]:
        separator()
        info(f"crt.sh Certificate Transparency sorgulanıyor...")
        sf, st = spinner_start("Pasif keşif çalışıyor")
        passive = crtsh_lookup(domain)
        spinner_stop(sf, st)
        separator()
        if passive:
            info(f"{len(passive)} subdomain bulundu (pasif):")
            for sub in sorted(passive):
                ip = resolve_ip(sub)
                ip_str = f" → {ip}" if ip else " → [çözümlenemedi]"
                found(f"{sub}{ip_str}")
                all_found.add(sub)
                results_log.append(f"{sub}{ip_str}")
        else:
            warn("Pasif keşifte sonuç bulunamadı.")

    # Aktif
    if mod in ["2", "3"]:
        separator()
        thread_count = 30
        try:
            tc = input(f"  {BC}[?]{RESET} Thread sayısı [{thread_count}]: ").strip()
            if tc.isdigit():
                thread_count = int(tc)
        except:
            pass
        info(f"Aktif DNS brute-force başlatılıyor ({thread_count} thread)...")
        separator()
        active = subdomain_bruteforce(domain, SUBDOMAIN_WORDLIST, thread_count)
        for sub, ip in active:
            all_found.add(sub)
            results_log.append(f"{sub} → {ip}")

    separator()
    success(f"Toplam {len(all_found)} benzersiz subdomain bulundu.")

    # Kaydet?
    save = input(f"\n  {BC}[?]{RESET} Sonuçları kaydet? [e/h]: ").strip().lower()
    if save == "e":
        fn = f"subdomain_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(fn, "w") as f:
            f.write(f"# Subdomain Hunter — {domain}\n")
            f.write(f"# Tarih: {timestamp()}\n\n")
            for line in sorted(results_log):
                f.write(line + "\n")
        success(f"Kayıt: {fn}")

    pause()

# ══════════════════════════════════════════════════════════════════
#  WEB-RECON — CORE ENGINE
# ══════════════════════════════════════════════════════════════════
# Kapsamlı web path wordlist
WEB_WORDLIST = [
    "admin","administrator","admin/login","login","logout","signin","signout",
    "register","signup","dashboard","panel","controlpanel","cpanel","wp-admin",
    "wp-login.php","wp-config.php","config.php","configuration.php","settings.php",
    ".env",".htaccess",".htpasswd","robots.txt","sitemap.xml","sitemap_index.xml",
    "backup","backup.zip","backup.tar.gz","backup.sql","db.sql","database.sql",
    "dump.sql","site.zip","www.zip","old","old.zip","tmp","temp","test","testing",
    "dev","development","staging","beta","api","api/v1","api/v2","api/v1/docs",
    "swagger","swagger-ui.html","swagger.json","openapi.json","redoc","docs",
    "documentation","readme","readme.txt","readme.md","changelog","install",
    "install.php","phpinfo.php","info.php","server-status","server-info",
    ".git/HEAD",".git/config","/.git","/.svn","/.hg","/.bzr","composer.json",
    "package.json","requirements.txt","Dockerfile","docker-compose.yml",
    "Makefile","Vagrantfile","Jenkinsfile",".travis.yml","appveyor.yml",
    "web.config","app.config","appsettings.json","application.properties",
    "index.php","index.html","index.htm","default.asp","default.aspx",
    "home","home.php","main","main.php","portal","search","search.php",
    "user","users","account","accounts","profile","profiles","member","members",
    "shop","store","cart","checkout","payment","order","orders","product","products",
    "upload","uploads","files","file","download","downloads","media","images",
    "static","assets","css","js","javascript","vendor","lib","library","third-party",
    "ajax","xhr","api/users","api/admin","api/login","api/register","api/config",
    "api/v1/users","api/v1/admin","api/v2/users","graphql","rest","rpc",
    "health","healthz","health-check","ping","pong","status","metrics","prometheus",
    "actuator","actuator/health","actuator/env","actuator/beans","actuator/mappings",
    "trace","debug","logging","logs","log","error","errors","exception",
    "cgi-bin","cgi-bin/test.cgi","scripts","shell","cmd","exec","command",
    "phpmyadmin","pma","adminer","db-admin","dbadmin","mssql","oracle","mysql",
    "mailman","webmail","roundcube","squirrelmail","horde","owa","exchange",
    "jenkins","gitlab","sonar","sonarqube","nexus","artifactory","harbor",
    "kibana","grafana","elasticsearch","redis","memcached","mongodb",
    "jira","confluence","bitbucket","bamboo","octopus","teamcity",
    "vpn","remote","rdp","ssh","telnet","ftp","sftp","smb","nfs",
    "nagios","zabbix","cacti","prtg","observium","librenms","checkmk",
    "forum","community","blog","news","events","calendar","feed","rss",
    "newsletter","subscribe","unsubscribe","contact","about","team","careers",
    "privacy","terms","cookie","gdpr","legal","support","helpdesk","ticket",
    "crm","erp","hr","payroll","finance","accounting","billing","invoice",
    "report","reports","analytics","stats","statistics","kpi","dashboard",
    "admin/index.php","admin/login.php","admin/dashboard","admin/users",
]

STATUS_COLORS = {
    200: BG,   201: BG,   301: BC,   302: BC,
    400: BY,   401: BY,   403: Y,    404: DIM,
    405: BY,   500: BR,   503: BR,
}

def analyze_headers(headers):
    """Sunucu teknoloji parmak izi"""
    findings = []
    tech_headers = {
        "Server": "Web Sunucusu",
        "X-Powered-By": "Çerçeve/Dil",
        "X-AspNet-Version": "ASP.NET Sürümü",
        "X-AspNetMvc-Version": "MVC Sürümü",
        "X-Generator": "CMS/Generator",
        "X-Drupal-Cache": "Drupal CMS",
        "X-WordPress": "WordPress",
        "X-Joomla": "Joomla CMS",
        "X-CF-Cache-Status": "Cloudflare CDN",
        "X-Cache": "Cache Layer",
        "Via": "Proxy/CDN",
        "X-Varnish": "Varnish Cache",
        "X-Amzn-Trace-Id": "AWS ALB",
        "X-Azure-Ref": "Azure Front Door",
    }
    for h, label in tech_headers.items():
        val = headers.get(h, headers.get(h.lower()))
        if val:
            findings.append((label, val))
    return findings

def web_scan_path(base_url, path, timeout=5, baseline_len=0):
    """Tek URL yolunu tara"""
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    try:
        r = requests.get(url, timeout=timeout, allow_redirects=False,
                         verify=False, headers={"User-Agent": "Mozilla/5.0 (Security-Audit/9.1)"})
        status = r.status_code
        clen = len(r.content)
        color = STATUS_COLORS.get(status, W)
        # Custom 404 tespiti
        custom404 = False
        if status == 200 and baseline_len > 0:
            if abs(clen - baseline_len) < 50:
                custom404 = True
        return {"url": url, "status": status, "length": clen,
                "headers": dict(r.headers), "custom404": custom404, "color": color}
    except requests.exceptions.Timeout:
        return None
    except Exception:
        return None

def get_baseline(base_url, timeout=5):
    """404 baseline uzunluğunu tespit et"""
    test_path = f"recon_nonexistent_{random.randint(100000,999999)}"
    url = f"{base_url.rstrip('/')}/{test_path}"
    try:
        r = requests.get(url, timeout=timeout, verify=False,
                         headers={"User-Agent": "Mozilla/5.0 (Security-Audit/9.1)"})
        return len(r.content), r.status_code
    except:
        return 0, 0

def run_web_recon():
    banner_module()
    header("Web-Recon — HTTP Yapı ve Zafiyet Keşfi")

    target = get_target("Hedef URL (örn: https://example.com)")
    if not target:
        error("URL boş olamaz!")
        pause()
        return

    if not target.startswith("http"):
        target = "https://" + target

    try:
        timeout_s = int(input(f"  {BC}[?]{RESET} Timeout (saniye) [5]: ").strip() or "5")
    except:
        timeout_s = 5

    try:
        thread_s = int(input(f"  {BC}[?]{RESET} Thread sayısı [20]: ").strip() or "20")
    except:
        thread_s = 20

    print(f"\n  {DIM}Başlangıç: {timestamp()}{RESET}")
    separator()
    info("Baseline (gerçek 404) tespiti yapılıyor...")
    baseline_len, baseline_status = get_baseline(target, timeout_s)
    info(f"Baseline: durum={baseline_status}, boyut={baseline_len} byte")
    separator()

    # Header analizi (ana URL)
    info("Ana URL başlık analizi...")
    try:
        r = requests.get(target, timeout=timeout_s, verify=False,
                         headers={"User-Agent": "Mozilla/5.0 (Security-Audit/9.1)"})
        techs = analyze_headers(r.headers)
        if techs:
            print(f"\n  {BY}[Teknoloji Tespiti]{RESET}")
            for label, val in techs:
                print(f"    {BM}{label}{RESET}: {val}")
        print()
    except Exception as e:
        warn(f"Ana URL bağlantı hatası: {e}")

    separator()
    info(f"Dizin/dosya taraması başlatılıyor ({thread_s} thread)...")
    separator()

    results = []
    done = 0
    total = len(WEB_WORDLIST)

    def worker(path):
        return web_scan_path(target, path, timeout_s, baseline_len)

    with ThreadPoolExecutor(max_workers=thread_s) as executor:
        futures = {executor.submit(worker, p): p for p in WEB_WORDLIST}
        for future in as_completed(futures):
            res = future.result()
            done += 1
            if res:
                status = res["status"]
                if status in [200, 201, 301, 302, 403, 401, 500]:
                    if not res["custom404"]:
                        color = res["color"]
                        flag = " [CUSTOM-404?]" if res["custom404"] else ""
                        flag2 = " ★" if status == 200 else ""
                        flag3 = " [FORBIDDEN]" if status == 403 else ""
                        print(f"  {color}[{status}]{RESET} {res['url']:<55} {DIM}{res['length']} B{RESET}{BG}{flag2}{RESET}{BY}{flag3}{RESET}{flag}")
                        results.append(res)
            # Progress
            sys.stdout.write(f"\r  {DIM}İlerleme: {done}/{total} ({100*done//total}%){RESET}  ")
            sys.stdout.flush()

    print()
    separator()
    success(f"{len(results)} bulgu tespit edildi.")

    # Başlık güvenlik analizi
    print(f"\n  {C}[Güvenlik Başlıkları Analizi]{RESET}")
    try:
        r = requests.get(target, timeout=timeout_s, verify=False)
        sec_headers = {
            "Strict-Transport-Security": "HSTS",
            "Content-Security-Policy": "CSP",
            "X-Frame-Options": "Clickjacking Koruması",
            "X-XSS-Protection": "XSS Koruması",
            "X-Content-Type-Options": "MIME Koruması",
            "Referrer-Policy": "Referrer Politikası",
            "Permissions-Policy": "İzin Politikası",
        }
        for header_name, label in sec_headers.items():
            val = r.headers.get(header_name)
            if val:
                success(f"{label}: {val}")
            else:
                warn(f"{label}: EKSİK ← Güvenlik açığı!")
    except:
        pass

    # Kaydet
    save = input(f"\n  {BC}[?]{RESET} Sonuçları kaydet? [e/h]: ").strip().lower()
    if save == "e":
        fn = f"webrecon_{urlparse(target).netloc}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(fn, "w") as f:
            f.write(f"# Web-Recon — {target}\n# {timestamp()}\n\n")
            for r2 in results:
                f.write(f"[{r2['status']}] {r2['url']} | {r2['length']} B\n")
        success(f"Kayıt: {fn}")

    pause()

# ══════════════════════════════════════════════════════════════════
#  MENÜ 4 — GİZLİ MENÜ ÖZEL ARAÇLAR
# ══════════════════════════════════════════════════════════════════
def banner_grab(host, port, timeout=5):
    """Port banner grabbing"""
    try:
        with socket.socket() as s:
            s.settimeout(timeout)
            s.connect((host, port))
            s.send(b"HEAD / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
            return s.recv(1024).decode(errors="ignore")
    except:
        return None

def run_banner_grabber():
    banner_module()
    header("Banner Grabbing — Servis Tespiti")
    host = get_target("Hedef host/IP")
    if not host:
        error("Host boş!")
        pause()
        return
    common_ports = [21,22,23,25,53,80,110,111,135,139,143,443,445,
                    3306,3389,5432,5900,6379,8080,8443,8888,9200,27017]
    info(f"Yaygın portlar taranıyor: {host}")
    separator()
    open_ports = []
    for port in common_ports:
        try:
            with socket.socket() as s:
                s.settimeout(1.5)
                result = s.connect_ex((host, port))
                if result == 0:
                    banner = banner_grab(host, port, timeout=2)
                    banner_snippet = banner.split("\n")[0][:50] if banner else "-"
                    found(f"Port {port:5d}/tcp  AÇIK  |  {banner_snippet}")
                    open_ports.append((port, banner_snippet))
        except:
            pass
    separator()
    success(f"{len(open_ports)} açık port tespit edildi.")
    pause()

def run_whois_lookup():
    banner_module()
    header("WHOIS — Domain Kayıt Sorgulama")
    domain = get_target("Domain (örn: example.com)")
    if not domain:
        error("Domain boş!")
        pause()
        return
    info(f"WHOIS sorgusu: {domain}")
    try:
        result = subprocess.run(["whois", domain], capture_output=True, text=True, timeout=15)
        output = result.stdout or result.stderr
        lines = [l for l in output.split("\n") if any(
            k in l.lower() for k in ["registrar","created","expires","updated",
                                      "name server","status","registrant","tech","admin"])]
        if lines:
            for line in lines[:30]:
                print(f"  {G}{line}{RESET}")
        else:
            print(f"  {DIM}{output[:1500]}{RESET}")
    except FileNotFoundError:
        warn("'whois' komutu bulunamadı. Sisteminize yükleyin.")
    except Exception as e:
        error(f"Hata: {e}")
    pause()

def run_dns_map():
    banner_module()
    header("DNS Kayıt Haritalaması")
    domain = get_target("Domain (örn: example.com)")
    if not domain:
        error("Domain boş!")
        pause()
        return

    record_types = ["A","AAAA","MX","NS","TXT","SOA","CNAME","CAA"]
    info(f"DNS kayıtları sorgulanıyor: {domain}")
    separator()
    for rtype in record_types:
        try:
            result = subprocess.run(
                ["nslookup", "-type=" + rtype, domain],
                capture_output=True, text=True, timeout=10
            )
            lines = result.stdout.strip().split("\n")
            relevant = [l for l in lines if domain in l or "=" in l or "answer" in l.lower()]
            if relevant:
                print(f"  {BC}[{rtype}]{RESET}")
                for r in relevant[:5]:
                    print(f"       {G}{r.strip()}{RESET}")
        except:
            try:
                ip = socket.gethostbyname(domain)
                if rtype == "A":
                    print(f"  {BC}[A]{RESET} {domain} → {G}{ip}{RESET}")
            except:
                pass
    separator()
    pause()

def menu_hidden():
    while True:
        banner_module()
        header("Gizli Menü — Özel Araçlar")
        print(f"""
  {R}[ ÖZEL ARAÇLAR ]{RESET}

  {G}[1]{RESET} Banner Grabbing — Port/Servis Tespiti
  {G}[2]{RESET} WHOIS — Domain Kayıt Sorgulama
  {G}[3]{RESET} DNS Haritalaması (A/MX/NS/TXT/SOA)
  {G}[4]{RESET} IP Geolocation (socket tabanlı)
  {G}[5]{RESET} SSL Sertifika Analizi
  {G}[0]{RESET} Ana Menüye Dön
        """)
        c = input(f"  {BC}[?]{RESET} Seçim: ").strip()
        if c == "1": run_banner_grabber()
        elif c == "2": run_whois_lookup()
        elif c == "3": run_dns_map()
        elif c == "4": run_geo_lookup()
        elif c == "5": run_ssl_audit()
        elif c == "0": break

def run_geo_lookup():
    banner_module()
    header("IP Geolocation Analizi")
    target = get_target("Domain veya IP")
    if not target:
        error("Boş!")
        pause()
        return
    try:
        ip = socket.gethostbyname(target)
        info(f"Çözümlenen IP: {ip}")
        r = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10)
        if r.status_code == 200:
            data = r.json()
            print(f"\n  {C}{'─'*40}{RESET}")
            fields = [("IP","ip"),("Ülke","country_name"),("Bölge","region"),
                      ("Şehir","city"),("ISP","org"),("ASN","asn"),
                      ("Zaman Dilimi","timezone"),("Enlem","latitude"),("Boylam","longitude")]
            for label, key in fields:
                val = data.get(key, "-")
                if val and val != "-":
                    print(f"  {BC}{label:<15}{RESET}: {G}{val}{RESET}")
    except Exception as e:
        error(f"Hata: {e}")
    pause()

def run_ssl_audit():
    banner_module()
    header("SSL/TLS Sertifika Analizi")
    host = get_target("Domain (örn: example.com)")
    if not host:
        error("Boş!")
        pause()
        return
    info(f"SSL sertifikası kontrol ediliyor: {host}")
    try:
        import ssl, socket
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.settimeout(10)
            s.connect((host, 443))
            cert = s.getpeercert()
            separator()
            subject = dict(x[0] for x in cert.get("subject", []))
            issuer = dict(x[0] for x in cert.get("issuer", []))
            print(f"  {BC}Konu CN       {RESET}: {G}{subject.get('commonName', '-')}{RESET}")
            print(f"  {BC}Kuruluş       {RESET}: {G}{subject.get('organizationName', '-')}{RESET}")
            print(f"  {BC}Yayıncı       {RESET}: {G}{issuer.get('commonName', '-')}{RESET}")
            print(f"  {BC}Geçerlilik Başı{RESET}: {Y}{cert.get('notBefore', '-')}{RESET}")
            print(f"  {BC}Geçerlilik Sonu{RESET}: {Y}{cert.get('notAfter', '-')}{RESET}")
            sans = []
            for t, v in cert.get("subjectAltName", []):
                if t == "DNS":
                    sans.append(v)
            if sans:
                print(f"  {BC}SAN Sayısı    {RESET}: {G}{len(sans)}{RESET}")
                for san in sans[:10]:
                    print(f"    {DIM}→ {san}{RESET}")
    except ssl.SSLError as e:
        error(f"SSL hatası: {e}")
    except Exception as e:
        error(f"Hata: {e}")
    pause()

# ══════════════════════════════════════════════════════════════════
#  MENÜ 5 — İSTİHBARİ MENÜ ÜST DÜZEY ARAÇLAR
# ══════════════════════════════════════════════════════════════════
def run_email_harvest():
    banner_module()
    header("E-posta Toplama — OSINT")
    domain = get_target("Domain (örn: example.com)")
    if not domain:
        error("Boş!")
        pause()
        return
    info(f"TXT kayıtlarında SPF/DMARC/DKIM taranıyor: {domain}")
    separator()
    txt_domains = [
        domain, f"_dmarc.{domain}", f"default._domainkey.{domain}",
        f"mail._domainkey.{domain}", f"smtp._domainkey.{domain}"
    ]
    for td in txt_domains:
        try:
            result = subprocess.run(
                ["nslookup", "-type=TXT", td],
                capture_output=True, text=True, timeout=10
            )
            lines = [l for l in result.stdout.split("\n") if "text" in l.lower() or "=" in l]
            if lines:
                found(f"{td}:")
                for l in lines[:3]:
                    print(f"       {G}{l.strip()}{RESET}")
        except:
            pass
    separator()
    info("Mail sunucuları (MX):")
    try:
        result = subprocess.run(["nslookup", "-type=MX", domain],
                                capture_output=True, text=True, timeout=10)
        for line in result.stdout.split("\n"):
            if "mail exchanger" in line.lower() or "MX" in line:
                print(f"  {BM}  {line.strip()}{RESET}")
    except:
        pass
    pause()

def run_tech_fingerprint():
    banner_module()
    header("Teknoloji Parmak İzi — Derinlemesine Analiz")
    target = get_target("Hedef URL")
    if not target:
        error("Boş!")
        pause()
        return
    if not target.startswith("http"):
        target = "https://" + target
    info("Teknoloji analizi başlatılıyor...")
    separator()
    try:
        r = requests.get(target, timeout=10, verify=False,
                         headers={"User-Agent": "Mozilla/5.0 (Security-Audit/9.1)"})
        techs = analyze_headers(r.headers)
        for label, val in techs:
            found(f"{label}: {val}")

        # İçerik analizi
        body = r.text.lower()
        cms_sigs = {
            "WordPress": ["wp-content","wp-includes","wp-json"],
            "Drupal": ["drupal.js","drupal.min","sites/default"],
            "Joomla": ["joomla","com_content","com_users"],
            "Magento": ["magento","mage/","varien/"],
            "Shopify": ["shopify.com","myshopify"],
            "Laravel": ["laravel_session","_token","csrf-token"],
            "Django": ["csrfmiddlewaretoken","django"],
            "Rails": ["rails","csrf-param"],
            "React": ["react.development","react.production","__reactFiber"],
            "Vue.js": ["vue.min","__vue__"],
            "Angular": ["ng-version","angular.min"],
            "jQuery": ["jquery.min","jquery-"],
            "Bootstrap": ["bootstrap.min","bootstrap.css"],
        }
        separator()
        info("İçerik tabanlı CMS/Framework tespiti:")
        detected = []
        for cms, sigs in cms_sigs.items():
            if any(sig in body for sig in sigs):
                success(f"Tespit: {cms}")
                detected.append(cms)
        if not detected:
            warn("Bilinen CMS/Framework imzası bulunamadı.")
    except Exception as e:
        error(f"Hata: {e}")
    pause()

def run_parameter_discover():
    banner_module()
    header("Parametre Keşfi — Hidden Input/Form Analizi")
    target = get_target("Hedef URL")
    if not target:
        error("Boş!")
        pause()
        return
    if not target.startswith("http"):
        target = "https://" + target
    info("Form ve gizli parametreler taranıyor...")
    try:
        r = requests.get(target, timeout=10, verify=False,
                         headers={"User-Agent": "Mozilla/5.0 (Security-Audit/9.1)"})
        body = r.text
        import re
        # Input alanları
        inputs = re.findall(r'<input[^>]+>', body, re.IGNORECASE)
        separator()
        info(f"{len(inputs)} input alanı bulundu:")
        for inp in inputs[:20]:
            name = re.search(r'name=["\']([^"\']+)["\']', inp, re.I)
            itype = re.search(r'type=["\']([^"\']+)["\']', inp, re.I)
            n = name.group(1) if name else "isimsiz"
            t = itype.group(1) if itype else "text"
            color = BY if t.lower() == "hidden" else G
            print(f"  {color}[{t.upper()}]{RESET} name={n}")
        # Formlar
        forms = re.findall(r'<form[^>]+>', body, re.IGNORECASE)
        separator()
        info(f"{len(forms)} form bulundu:")
        for form in forms[:5]:
            action = re.search(r'action=["\']([^"\']+)["\']', form, re.I)
            method = re.search(r'method=["\']([^"\']+)["\']', form, re.I)
            a = action.group(1) if action else "/"
            m = method.group(1).upper() if method else "GET"
            found(f"{m} → {a}")
    except Exception as e:
        error(f"Hata: {e}")
    pause()

def menu_intelligence():
    while True:
        banner_module()
        header("İstihbari Menü — Üst Düzey Araçlar")
        print(f"""
  {M}[ ÜST DÜZEY OSINT & İSTİHBARAT ]{RESET}

  {G}[1]{RESET} E-posta Toplama (SPF/DMARC/MX OSINT)
  {G}[2]{RESET} Teknoloji Parmak İzi (Derinlemesine)
  {G}[3]{RESET} Parametre Keşfi (Hidden Input/Form)
  {G}[4]{RESET} HTTP Metod Analizi (OPTIONS/TRACE/PUT)
  {G}[5]{RESET} Redirect Zinciri Analizi
  {G}[6]{RESET} Cookie Güvenlik Analizi
  {G}[0]{RESET} Ana Menüye Dön
        """)
        c = input(f"  {BC}[?]{RESET} Seçim: ").strip()
        if c == "1": run_email_harvest()
        elif c == "2": run_tech_fingerprint()
        elif c == "3": run_parameter_discover()
        elif c == "4": run_http_methods()
        elif c == "5": run_redirect_chain()
        elif c == "6": run_cookie_analysis()
        elif c == "0": break

def run_http_methods():
    banner_module()
    header("HTTP Metod Analizi")
    target = get_target("Hedef URL")
    if not target:
        error("Boş!")
        pause()
        return
    if not target.startswith("http"):
        target = "https://" + target
    methods = ["GET","POST","PUT","DELETE","PATCH","OPTIONS","HEAD","TRACE","CONNECT"]
    separator()
    info(f"HTTP metodları test ediliyor: {target}")
    separator()
    for method in methods:
        try:
            r = requests.request(method, target, timeout=5, verify=False)
            color = BG if r.status_code < 300 else (BY if r.status_code < 500 else BR)
            flag = " ← DİKKAT!" if method in ["TRACE","PUT","DELETE"] and r.status_code < 400 else ""
            print(f"  {color}[{r.status_code}]{RESET} {method:<10} {BY}{flag}{RESET}")
        except Exception as e:
            print(f"  {DIM}[ERR]{RESET} {method:<10} → {e}")
    pause()

def run_redirect_chain():
    banner_module()
    header("Redirect Zinciri Analizi")
    target = get_target("Hedef URL")
    if not target:
        error("Boş!")
        pause()
        return
    if not target.startswith("http"):
        target = "https://" + target
    info("Redirect zinciri izleniyor...")
    separator()
    try:
        r = requests.get(target, timeout=10, allow_redirects=True, verify=False)
        for i, resp in enumerate(r.history + [r]):
            color = BC if resp.is_redirect else BG
            loc = resp.headers.get("Location", resp.url)
            print(f"  {color}[{resp.status_code}]{RESET} [{i}] {loc}")
    except Exception as e:
        error(f"Hata: {e}")
    pause()

def run_cookie_analysis():
    banner_module()
    header("Cookie Güvenlik Analizi")
    target = get_target("Hedef URL")
    if not target:
        error("Boş!")
        pause()
        return
    if not target.startswith("http"):
        target = "https://" + target
    try:
        r = requests.get(target, timeout=10, verify=False)
        separator()
        info(f"{len(r.cookies)} cookie tespit edildi:")
        for cookie in r.cookies:
            issues = []
            if not cookie.secure: issues.append("Secure bayrağı EKSİK")
            if not cookie.has_nonstandard_attr("HttpOnly"): issues.append("HttpOnly EKSİK")
            if not cookie.has_nonstandard_attr("SameSite"): issues.append("SameSite EKSİK")
            issue_str = " | ".join(issues) if issues else "Güvenli"
            color = BG if not issues else BY
            print(f"  {color}[Cookie]{RESET} {cookie.name} = {cookie.value[:20]}...")
            if issues:
                for iss in issues:
                    warn(f"    → {iss}")
    except Exception as e:
        error(f"Hata: {e}")
    pause()

# ══════════════════════════════════════════════════════════════════
#  MENÜ 6 — ANA MENÜ STANDART ARAÇLAR
# ══════════════════════════════════════════════════════════════════
def menu_standard():
    while True:
        banner_module()
        header("Ana Menü — Standart Araçlar")
        print(f"""
  {C}[ TEMEL GÜVENLIK ARAÇLARI ]{RESET}

  {G}[1]{RESET} Subdomain Hunter (Pasif + Aktif)
  {G}[2]{RESET} Web-Recon (Dizin/Dosya Taraması)
  {G}[3]{RESET} Port Tarayıcı (Hızlı)
  {G}[4]{RESET} DNS Kayıt Analizi
  {G}[5]{RESET} IP/Domain Çözümleme
  {G}[0]{RESET} Ana Menüye Dön
        """)
        c = input(f"  {BC}[?]{RESET} Seçim: ").strip()
        if c == "1": run_subdomain_hunter()
        elif c == "2": run_web_recon()
        elif c == "3": run_port_scanner()
        elif c == "4": run_dns_map()
        elif c == "5": run_resolve()
        elif c == "0": break

def run_port_scanner():
    banner_module()
    header("Hızlı Port Tarayıcı")
    host = get_target("Hedef host/IP")
    if not host:
        error("Boş!")
        pause()
        return
    try:
        port_range = input(f"  {BC}[?]{RESET} Port aralığı (ör: 1-1024) [1-1024]: ").strip() or "1-1024"
        start_p, end_p = map(int, port_range.split("-"))
    except:
        start_p, end_p = 1, 1024

    try:
        threads_n = int(input(f"  {BC}[?]{RESET} Thread [100]: ").strip() or "100")
    except:
        threads_n = 100

    info(f"Port taraması: {host} ({start_p}-{end_p})")
    separator()
    open_ports = []

    def check_port(port):
        try:
            with socket.socket() as s:
                s.settimeout(0.7)
                if s.connect_ex((host, port)) == 0:
                    try:
                        svc = socket.getservbyport(port)
                    except:
                        svc = "bilinmiyor"
                    return port, svc
        except:
            pass
        return None

    with ThreadPoolExecutor(max_workers=threads_n) as executor:
        futures = [executor.submit(check_port, p) for p in range(start_p, end_p + 1)]
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                port, svc = res
                open_ports.append((port, svc))
                found(f"Port {port:5d}/tcp  →  {svc}")

    separator()
    success(f"{len(open_ports)} açık port.")
    pause()

def run_resolve():
    banner_module()
    header("IP/Domain Çözümleme")
    target = get_target("Domain veya IP")
    if not target:
        error("Boş!")
        pause()
        return
    try:
        ip = socket.gethostbyname(target)
        found(f"IP: {ip}")
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            found(f"Ters DNS: {hostname}")
        except:
            warn("Ters DNS çözümlenemedi.")
    except Exception as e:
        error(f"Hata: {e}")
    pause()

# ══════════════════════════════════════════════════════════════════
#  MENÜ 7 — KRİTİK ARAÇLAR
# ══════════════════════════════════════════════════════════════════
def menu_critical():
    while True:
        banner_module()
        header("Kritik Araçlar")
        print(f"""
  {BR}[ KRİTİK GÜVENLİK ARAÇLARI ]{RESET}

  {R}[1]{RESET} WAF Tespit Analizi
  {R}[2]{RESET} Subdomain Takeover Kontrolü
  {R}[3]{RESET} Açık Dizin İndeksleme Tespiti
  {R}[4]{RESET} Hassas Dosya Sızıntısı Kontrolü
  {R}[5]{RESET} Rate-Limit Analizi
  {G}[0]{RESET} Ana Menüye Dön
        """)
        c = input(f"  {BC}[?]{RESET} Seçim: ").strip()
        if c == "1": run_waf_detect()
        elif c == "2": run_subdomain_takeover()
        elif c == "3": run_dir_listing()
        elif c == "4": run_sensitive_files()
        elif c == "5": run_rate_limit()
        elif c == "0": break

def run_waf_detect():
    banner_module()
    header("WAF Tespit Analizi")
    target = get_target("Hedef URL")
    if not target:
        error("Boş!")
        pause()
        return
    if not target.startswith("http"):
        target = "https://" + target
    info(f"WAF tespiti yapılıyor: {target}")
    separator()

    # Kötü niyetli payload ile test
    payload_url = target + "/?q=<script>alert(1)</script>&id=1' OR 1=1--"
    waf_sigs = {
        "Cloudflare": ["cloudflare","__cfduid","cf-ray","403 Forbidden"],
        "AWS WAF": ["x-amzn-requestid","aws-waf","awselb"],
        "Akamai": ["akamai","akamaighost","akamaierror"],
        "Sucuri": ["sucuri","cloudproxy","x-sucuri-id"],
        "Incapsula": ["incapsula","visid_incap","incap_ses"],
        "ModSecurity": ["mod_security","modsec","not acceptable"],
        "F5 BIG-IP": ["bigip","f5-bigip","ts=","tu="],
        "Barracuda": ["barracuda_","barra_counter_session"],
        "Imperva": ["imperva","x-iinfo","incap_ses"],
    }

    try:
        r = requests.get(payload_url, timeout=10, verify=False,
                         headers={"User-Agent": "Mozilla/5.0 (Security-Audit)"})
        headers_str = str(r.headers).lower()
        body_str = r.text.lower()
        full = headers_str + body_str + str(r.status_code)

        detected_waf = []
        for waf, sigs in waf_sigs.items():
            if any(sig.lower() in full for sig in sigs):
                detected_waf.append(waf)
                found(f"WAF Tespit: {waf}")

        if r.status_code in [403, 406, 429, 503]:
            warn(f"Şüpheli durum kodu: {r.status_code} → WAF engeli olabilir")

        if not detected_waf:
            warn("Bilinen WAF imzası bulunamadı (WAF yok veya gizlenmiş)")

        separator()
        info(f"Response: {r.status_code} | Boyut: {len(r.content)} B")
    except Exception as e:
        error(f"Hata: {e}")
    pause()

def run_subdomain_takeover():
    banner_module()
    header("Subdomain Takeover Kontrolü")
    domain = get_target("Ana domain (örn: example.com)")
    if not domain:
        error("Boş!")
        pause()
        return
    info("Potansiyel takeover açıkları taranıyor...")

    # Yaygın servis hata mesajları
    takeover_sigs = {
        "GitHub Pages": ["there isn't a github pages site here"],
        "Heroku": ["no such app","heroku | no such app"],
        "Netlify": ["not found - request id"],
        "AWS S3": ["nosuchbucket","the specified bucket does not exist"],
        "Azure": ["404 web site not found"],
        "Shopify": ["sorry, this shop is currently unavailable"],
        "Tumblr": ["there's nothing here"],
        "Fastly": ["fastly error: unknown domain"],
        "Pantheon": ["the gods are wise, but do not know of the url"],
        "Unbounce": ["the requested url was not found on this server"],
    }

    passive = crtsh_lookup(domain)
    subs_to_check = list(passive)[:30]

    if not subs_to_check:
        warn("Kontrol edilecek subdomain bulunamadı.")
        pause()
        return

    separator()
    info(f"{len(subs_to_check)} subdomain kontrol ediliyor...")
    separator()
    vulnerable = []

    for sub in subs_to_check:
        for proto in ["https", "http"]:
            url = f"{proto}://{sub}"
            try:
                r = requests.get(url, timeout=5, verify=False)
                body = r.text.lower()
                for service, sigs in takeover_sigs.items():
                    if any(sig in body for sig in sigs):
                        print(f"  {BR}[TAKEOVER RISKI!]{RESET} {sub} → {service}")
                        vulnerable.append((sub, service))
                        break
            except:
                pass

    if not vulnerable:
        success("Subdomain takeover açığı tespit edilmedi.")
    else:
        warn(f"{len(vulnerable)} potansiyel takeover açığı!")
    pause()

def run_dir_listing():
    banner_module()
    header("Açık Dizin İndeksleme Tespiti")
    target = get_target("Hedef URL")
    if not target:
        error("Boş!")
        pause()
        return
    if not target.startswith("http"):
        target = "https://" + target
    dirs = ["uploads/","images/","files/","backup/","logs/","tmp/","assets/",
            "static/","media/","downloads/","documents/","data/","old/"]
    separator()
    info("Açık dizin indeksleme kontrol ediliyor...")
    separator()
    for d in dirs:
        url = f"{target.rstrip('/')}/{d}"
        try:
            r = requests.get(url, timeout=5, verify=False)
            if r.status_code == 200 and ("index of" in r.text.lower() or
                                          "<title>directory" in r.text.lower()):
                print(f"  {BR}[AÇIK DİZİN!]{RESET} {url}")
            elif r.status_code == 200:
                print(f"  {BG}[200]{RESET} {url}")
            elif r.status_code == 403:
                print(f"  {BY}[403]{RESET} {url} {DIM}(Mevcut ama erişim yok){RESET}")
        except:
            pass
    pause()

def run_sensitive_files():
    banner_module()
    header("Hassas Dosya Sızıntısı Kontrolü")
    target = get_target("Hedef URL")
    if not target:
        error("Boş!")
        pause()
        return
    if not target.startswith("http"):
        target = "https://" + target
    sensitive = [".env",".git/config","config.php","wp-config.php","settings.py",
                 "database.yml","secrets.yml",".aws/credentials","id_rsa",".ssh/id_rsa",
                 "backup.sql","dump.sql","db.sql","phpinfo.php","info.php",
                 ".htpasswd","passwd","shadow","web.config","appsettings.json"]
    separator()
    info("Hassas dosyalar kontrol ediliyor...")
    separator()
    for f in sensitive:
        url = f"{target.rstrip('/')}/{f}"
        try:
            r = requests.get(url, timeout=5, verify=False)
            if r.status_code == 200 and len(r.content) > 10:
                print(f"  {BR}[SIZINTI!]{RESET} {url}  {DIM}({len(r.content)} B){RESET}")
            elif r.status_code == 403:
                print(f"  {BY}[403]{RESET} {url}  {DIM}(Mevcut ama kısıtlı){RESET}")
        except:
            pass
    pause()

def run_rate_limit():
    banner_module()
    header("Rate-Limit Analizi")
    target = get_target("Hedef URL")
    if not target:
        error("Boş!")
        pause()
        return
    if not target.startswith("http"):
        target = "https://" + target
    try:
        req_count = int(input(f"  {BC}[?]{RESET} İstek sayısı [20]: ").strip() or "20")
    except:
        req_count = 20
    separator()
    info(f"{req_count} istek gönderiliyor, rate-limit analiz ediliyor...")
    separator()
    statuses = []
    times = []
    for i in range(req_count):
        try:
            start = time.time()
            r = requests.get(target, timeout=5, verify=False)
            elapsed = time.time() - start
            statuses.append(r.status_code)
            times.append(elapsed)
            rl_header = r.headers.get("X-RateLimit-Remaining","?")
            retry = r.headers.get("Retry-After","?")
            color = BG if r.status_code == 200 else (BY if r.status_code == 429 else BR)
            print(f"  {color}[{r.status_code}]{RESET} İstek #{i+1:3d} | {elapsed:.2f}s | RL-Kalan:{rl_header} | Retry:{retry}")
            if r.status_code == 429:
                warn("RATE LIMIT TETIKLENDI!")
                break
        except Exception as e:
            error(f"Hata: {e}")
            break
    separator()
    info(f"Ortalama süre: {sum(times)/max(len(times),1):.2f}s")
    pause()

# ══════════════════════════════════════════════════════════════════
#  MENÜ 8 — INTERNATIONAL ARAÇLAR
# ══════════════════════════════════════════════════════════════════
def menu_international():
    while True:
        banner_module()
        header("International Araçlar")
        print(f"""
  {BB}[ ULUSLARARASI OSINT & NETWORK ARAÇLARI ]{RESET}

  {G}[1]{RESET} Shodan-Benzeri Banner Grabbing (çoklu port)
  {G}[2]{RESET} IP Blacklist / Reputation Kontrolü
  {G}[3]{RESET} HTTP Archive (Wayback Machine) Sorgusu
  {G}[4]{RESET} Traceroute Analizi
  {G}[5]{RESET} BGP / ASN Sorgulama
  {G}[0]{RESET} Ana Menüye Dön
        """)
        c = input(f"  {BC}[?]{RESET} Seçim: ").strip()
        if c == "1": run_multi_banner()
        elif c == "2": run_reputation()
        elif c == "3": run_wayback()
        elif c == "4": run_traceroute()
        elif c == "5": run_asn()
        elif c == "0": break

def run_multi_banner():
    banner_module()
    header("Çoklu Port Banner Grabbing")
    host = get_target("Hedef host/IP")
    if not host:
        error("Boş!")
        pause()
        return
    all_ports = [21,22,23,25,53,80,110,143,443,445,3306,3389,5432,6379,8080,8443,9200,27017]
    separator()
    info(f"Banner grabbing: {host} ({len(all_ports)} port)")
    separator()
    for port in all_ports:
        banner = banner_grab(host, port, timeout=2)
        if banner:
            snippet = banner.replace("\r","").split("\n")[0][:60]
            found(f"Port {port:5d} → {snippet}")
        else:
            try:
                with socket.socket() as s:
                    s.settimeout(0.5)
                    if s.connect_ex((host, port)) == 0:
                        print(f"  {BC}[AÇIK]{RESET} Port {port:5d} → banner alınamadı")
            except:
                pass
    pause()

def run_reputation():
    banner_module()
    header("IP Reputation / Blacklist Kontrolü")
    ip = get_target("IP adresi")
    if not ip:
        error("Boş!")
        pause()
        return
    info(f"Reputation kontrol: {ip}")
    try:
        r = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10)
        if r.status_code == 200:
            data = r.json()
            print(f"\n  {BC}Ülke{RESET}: {data.get('country_name','-')}")
            print(f"  {BC}ISP{RESET}: {data.get('org','-')}")
            print(f"  {BC}ASN{RESET}: {data.get('asn','-')}")
            print(f"  {BC}Zaman Dilimi{RESET}: {data.get('timezone','-')}")
    except Exception as e:
        error(f"Hata: {e}")
    # AbuseIPDB API olmadan basit kontrol
    try:
        r2 = requests.get(f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}",
                          headers={"Accept":"application/json"}, timeout=10)
        if r2.status_code == 200:
            d = r2.json().get("data",{})
            score = d.get("abuseConfidenceScore","-")
            print(f"  {BC}Abuse Skoru{RESET}: {BR if score and int(score)>50 else BG}{score}/100{RESET}")
    except:
        warn("AbuseIPDB API anahtarı gerekli (ücretsiz: abuseipdb.com)")
    pause()

def run_wayback():
    banner_module()
    header("Wayback Machine — Geçmiş Sayfa Arşivi")
    domain = get_target("Domain (örn: example.com)")
    if not domain:
        error("Boş!")
        pause()
        return
    info("Wayback Machine API sorgulanıyor...")
    try:
        url = f"http://archive.org/wayback/available?url={domain}"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            closest = data.get("archived_snapshots",{}).get("closest",{})
            if closest:
                found(f"Son arşiv: {closest.get('timestamp','?')}")
                found(f"URL: {closest.get('url','?')}")
                found(f"Durum: {closest.get('status','?')}")
            else:
                warn("Arşiv bulunamadı.")

        # CDX API ile tüm URL'leri listele
        cdx_url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}&output=json&limit=20&fl=original,timestamp,statuscode"
        r2 = requests.get(cdx_url, timeout=20)
        if r2.status_code == 200 and r2.text.strip():
            data2 = r2.json()
            separator()
            info(f"CDX API — Son {len(data2)-1} arşiv kaydı:")
            for entry in data2[1:21]:
                if len(entry) >= 3:
                    print(f"  {DIM}[{entry[1]}]{RESET} {G}{entry[0]}{RESET} {BC}({entry[2]}){RESET}")
    except Exception as e:
        error(f"Hata: {e}")
    pause()

def run_traceroute():
    banner_module()
    header("Traceroute Analizi")
    host = get_target("Hedef host/IP")
    if not host:
        error("Boş!")
        pause()
        return
    info(f"Traceroute: {host}")
    separator()
    cmd = "tracert" if os.name == "nt" else "traceroute"
    try:
        result = subprocess.run([cmd, "-m", "20", host],
                                capture_output=True, text=True, timeout=60)
        for line in result.stdout.split("\n")[:25]:
            print(f"  {G}{line}{RESET}")
    except FileNotFoundError:
        warn(f"'{cmd}' komutu bulunamadı.")
    except Exception as e:
        error(f"Hata: {e}")
    pause()

def run_asn():
    banner_module()
    header("BGP / ASN Sorgulama")
    target = get_target("IP veya domain")
    if not target:
        error("Boş!")
        pause()
        return
    try:
        ip = socket.gethostbyname(target)
        info(f"IP: {ip}")
        r = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10)
        if r.status_code == 200:
            data = r.json()
            print(f"\n  {BC}ASN{RESET}:         {G}{data.get('asn','-')}{RESET}")
            print(f"  {BC}Organizasyon{RESET}: {G}{data.get('org','-')}{RESET}")
            print(f"  {BC}Network{RESET}:      {G}{data.get('network','-')}{RESET}")
            print(f"  {BC}Ülke{RESET}:         {G}{data.get('country_name','-')}{RESET}")
    except Exception as e:
        error(f"Hata: {e}")
    pause()

# ══════════════════════════════════════════════════════════════════
#  MENÜ 9 — SAVUNMA ARAÇLARI (BLUE TEAM)
# ══════════════════════════════════════════════════════════════════
def menu_defense():
    while True:
        banner_module()
        header("Savunma Araçları — Blue Team")
        print(f"""
  {BG}[ SAVUNMA & GÜVENLİK SERTLEŞTIRME ]{RESET}

  {G}[1]{RESET} Güvenlik Başlıkları Denetimi (Security Headers)
  {G}[2]{RESET} SSL/TLS Güvenlik Denetimi
  {G}[3]{RESET} WAF Kuralı Simülasyonu
  {G}[4]{RESET} Rate-Limit Uygulaması Analizi
  {G}[5]{RESET} CORS Güvenlik Kontrolü
  {G}[6]{RESET} CSP (Content Security Policy) Analizi
  {G}[7]{RESET} Açık Port Riski Raporu
  {G}[8]{RESET} Güvenli Yapılandırma Kontrol Listesi
  {G}[0]{RESET} Ana Menüye Dön
        """)
        c = input(f"  {BC}[?]{RESET} Seçim: ").strip()
        if c == "1": run_security_headers()
        elif c == "2": run_ssl_audit()
        elif c == "3": run_waf_simulation()
        elif c == "4": run_rate_limit()
        elif c == "5": run_cors_check()
        elif c == "6": run_csp_analysis()
        elif c == "7": run_port_risk()
        elif c == "8": run_config_checklist()
        elif c == "0": break

def run_security_headers():
    banner_module()
    header("Güvenlik Başlıkları Denetimi")
    target = get_target("Hedef URL")
    if not target:
        error("Boş!")
        pause()
        return
    if not target.startswith("http"):
        target = "https://" + target
    try:
        r = requests.get(target, timeout=10, verify=False)
        separator()
        print(f"  {BW}URL:{RESET} {target}")
        print(f"  {BW}Durum:{RESET} {r.status_code}\n")

        checks = [
            ("Strict-Transport-Security","HSTS","Kritik — MITM saldırılarını önler"),
            ("Content-Security-Policy","CSP","Kritik — XSS saldırılarını sınırlar"),
            ("X-Frame-Options","Clickjacking","Orta — iframe gömme engeller"),
            ("X-XSS-Protection","XSS Filtresi","Orta — eski tarayıcı XSS koruması"),
            ("X-Content-Type-Options","MIME Sniff","Orta — MIME tipi sahtekarlığı önler"),
            ("Referrer-Policy","Referrer","Düşük — bilgi sızıntısını azaltır"),
            ("Permissions-Policy","İzinler","Düşük — API izinlerini kısıtlar"),
            ("Cache-Control","Önbellek","Orta — hassas veri önbellekte kalmasın"),
            ("Access-Control-Allow-Origin","CORS","Kritik — çapraz köken erişimi"),
            ("Server","Server","Bilgi — sürüm bilgisi ifşası riski"),
        ]

        pass_count = 0
        fail_count = 0
        for h, label, note in checks:
            val = r.headers.get(h)
            if val:
                if h == "Server":
                    warn(f"[!] {label:<25} {BY}MEVCUT{RESET}: {val} {DIM}← sürüm gizlenebilir{RESET}")
                else:
                    success(f"[✓] {label:<25} {G}MEVCUT{RESET}: {val[:50]}")
                    pass_count += 1
            else:
                if h == "Server":
                    success(f"[✓] Server başlığı gizlenmiş")
                    pass_count += 1
                else:
                    print(f"  {BR}[✗]{RESET} {label:<25} {BR}EKSİK{RESET}   {DIM}← {note}{RESET}")
                    fail_count += 1

        separator()
        score = int(pass_count / (pass_count + fail_count) * 100) if (pass_count + fail_count) > 0 else 0
        color = BG if score >= 70 else (BY if score >= 40 else BR)
        print(f"\n  {color}Güvenlik Skoru: {score}/100{RESET}")
        print(f"  Geçen: {pass_count} | Başarısız: {fail_count}")
    except Exception as e:
        error(f"Hata: {e}")
    pause()

def run_waf_simulation():
    banner_module()
    header("WAF Kuralı Simülasyonu")
    target = get_target("Hedef URL")
    if not target:
        error("Boş!")
        pause()
        return
    if not target.startswith("http"):
        target = "https://" + target

    payloads = {
        "SQL Injection": f"{target}?id=1' OR 1=1--",
        "XSS": f"{target}?q=<script>alert(1)</script>",
        "Path Traversal": f"{target}?file=../../../etc/passwd",
        "Command Injection": f"{target}?cmd=;ls -la",
        "SSRF": f"{target}?url=http://169.254.169.254/latest/meta-data/",
        "XXE": f"{target}?xml=<!DOCTYPE>",
        "SSTI": f"{target}?name={{{{7*7}}}}",
        "Open Redirect": f"{target}?redirect=https://evil.com",
    }

    separator()
    info("WAF engelleme testleri (saldırı simülasyonu):")
    separator()
    for attack, url in payloads.items():
        try:
            r = requests.get(url, timeout=5, verify=False,
                             headers={"User-Agent": "Mozilla/5.0 (Audit)"})
            blocked = r.status_code in [403, 406, 429, 503]
            if blocked:
                success(f"[ENGELLENDI] {attack:<25} → HTTP {r.status_code}")
            else:
                warn(f"[GEÇTİ]      {attack:<25} → HTTP {r.status_code} {BR}← WAF GEREKLİ!{RESET}")
        except Exception as e:
            print(f"  {DIM}[ERR]{RESET} {attack:<25} → {e}")
    pause()

def run_cors_check():
    banner_module()
    header("CORS Güvenlik Kontrolü")
    target = get_target("Hedef URL")
    if not target:
        error("Boş!")
        pause()
        return
    if not target.startswith("http"):
        target = "https://" + target

    test_origins = [
        "https://evil.com",
        "https://attacker.com",
        "null",
        target.replace("https://","https://evil."),
    ]
    separator()
    for origin in test_origins:
        try:
            r = requests.get(target, timeout=5, verify=False,
                             headers={"Origin": origin, "User-Agent": "Mozilla/5.0"})
            acao = r.headers.get("Access-Control-Allow-Origin","")
            acac = r.headers.get("Access-Control-Allow-Credentials","")
            if acao == "*":
                warn(f"Wildcard CORS! Origin:{origin} → ACAO:*")
            elif acao == origin:
                print(f"  {BR}[RISK!]{RESET} Origin yansıtıldı: {origin}")
                if acac.lower() == "true":
                    error("  Credentials=true ile birleşik → KRITIK!")
            elif acao:
                print(f"  {BG}[OK]{RESET}   Origin:{origin} → ACAO:{acao}")
            else:
                print(f"  {G}[✓]{RESET}   CORS başlığı yok: {origin}")
        except Exception as e:
            error(f"Hata: {e}")
    pause()

def run_csp_analysis():
    banner_module()
    header("CSP — Content Security Policy Analizi")
    target = get_target("Hedef URL")
    if not target:
        error("Boş!")
        pause()
        return
    if not target.startswith("http"):
        target = "https://" + target
    try:
        r = requests.get(target, timeout=10, verify=False)
        csp = r.headers.get("Content-Security-Policy","")
        if not csp:
            warn("CSP başlığı YOK → XSS saldırılarına açık!")
            pause()
            return
        success(f"CSP mevcut:\n  {DIM}{csp[:200]}{RESET}")
        separator()
        weak_indicators = [
            ("'unsafe-inline'", "Script satır içi çalıştırma — XSS riski"),
            ("'unsafe-eval'", "eval() kullanımı — XSS riski"),
            ("*", "Wildcard kaynak — herkese izin verir"),
            ("data:", "Data URI — potansiyel XSS"),
        ]
        for indicator, desc in weak_indicators:
            if indicator in csp:
                warn(f"Zayıf direktif bulundu: {indicator} → {desc}")
            else:
                success(f"Yok: {indicator}")
    except Exception as e:
        error(f"Hata: {e}")
    pause()

def run_port_risk():
    banner_module()
    header("Açık Port Riski Raporu")
    host = get_target("Hedef host/IP")
    if not host:
        error("Boş!")
        pause()
        return

    risk_ports = {
        21: ("FTP","Yüksek","Şifresiz veri transferi, brute-force riski"),
        22: ("SSH","Orta","Brute-force saldırı hedefi, güçlü şifre gerekli"),
        23: ("Telnet","Kritik","Şifresiz bağlantı! Kapatın"),
        25: ("SMTP","Orta","Spam relay riski, açık relay kontrolü yapın"),
        53: ("DNS","Orta","DNS amplification, zone transfer kontrolü"),
        80: ("HTTP","Düşük","HTTPS'e yönlendirme yapılmalı"),
        110: ("POP3","Yüksek","Şifresiz mail — POP3S kullanın"),
        135: ("RPC","Yüksek","Windows RPC — güvenlik duvarı ile koru"),
        139: ("NetBIOS","Kritik","Bilgi sızıntısı ve exploit riski"),
        445: ("SMB","Kritik","EternalBlue gibi kritik exploit riski"),
        1433: ("MSSQL","Kritik","Doğrudan internette olmamalı!"),
        3306: ("MySQL","Kritik","Doğrudan internette olmamalı!"),
        3389: ("RDP","Kritik","Brute-force ve BlueKeep riski"),
        5432: ("PostgreSQL","Kritik","Doğrudan internette olmamalı!"),
        5900: ("VNC","Kritik","Şifresiz ekran paylaşımı!"),
        6379: ("Redis","Kritik","Kimlik doğrulamasız! Kritik veri riski"),
        8080: ("HTTP Alt","Düşük","Admin panel buraya konulmamalı"),
        8443: ("HTTPS Alt","Düşük","Kontrol edilmeli"),
        9200: ("Elasticsearch","Kritik","Kimlik doğrulamasız olabilir!"),
        27017: ("MongoDB","Kritik","Kimlik doğrulamasız olabilir!"),
    }

    info(f"Kritik port risk taraması: {host}")
    separator()
    for port, (service, risk, note) in risk_ports.items():
        try:
            with socket.socket() as s:
                s.settimeout(0.7)
                if s.connect_ex((host, port)) == 0:
                    rcolor = (BR if risk == "Kritik" else
                              (BY if risk == "Yüksek" else
                               (Y if risk == "Orta" else G)))
                    print(f"  {rcolor}[{risk}]{RESET} Port {port:5d} {service:<15} {DIM}{note}{RESET}")
        except:
            pass
    separator()
    print(f"\n  {BW}Blue Team Önerileri:{RESET}")
    print(f"  {G}→ Gereksiz portları firewall ile kapat{RESET}")
    print(f"  {G}→ Yönetim portlarını VPN arkasına al{RESET}")
    print(f"  {G}→ Fail2ban ile brute-force koruması kur{RESET}")
    print(f"  {G}→ Tüm servislerin güncel ve yamalı olduğunu doğrula{RESET}")
    pause()

def run_config_checklist():
    banner_module()
    header("Güvenli Yapılandırma Kontrol Listesi")
    print(f"""
  {BG}BLUE TEAM — Sunucu Sertleştirme Kontrol Listesi{RESET}

  {BW}HTTP / Web Sunucusu:{RESET}
  {G}□{RESET} HTTPS zorunlu, HTTP → HTTPS yönlendirme aktif
  {G}□{RESET} HSTS başlığı etkin (max-age ≥ 31536000)
  {G}□{RESET} CSP başlığı yapılandırılmış, unsafe-inline yok
  {G}□{RESET} X-Frame-Options: DENY veya SAMEORIGIN
  {G}□{RESET} X-Content-Type-Options: nosniff
  {G}□{RESET} Server başlığı sürüm bilgisi gizlenmiş

  {BW}Kimlik Doğrulama:{RESET}
  {G}□{RESET} Admin paneli varsayılan /admin yolunda değil
  {G}□{RESET} MFA (çok faktörlü) doğrulama aktif
  {G}□{RESET} Brute-force koruması (captcha/lockout)
  {G}□{RESET} Parola politikası: min 12 karakter, karmaşıklık

  {BW}Veri Tabanı:{RESET}
  {G}□{RESET} DB dışarıdan erişilemez (firewall kuralı)
  {G}□{RESET} Uygulama hesabı en az yetkiye sahip
  {G}□{RESET} Tüm sorgular parametreli (SQL injection önlemi)
  {G}□{RESET} Yedekler şifreli ve farklı lokasyonda

  {BW}Sunucu:{RESET}
  {G}□{RESET} Gereksiz portlar kapatılmış
  {G}□{RESET} SSH sadece anahtar tabanlı (parola devre dışı)
  {G}□{RESET} Fail2ban aktif
  {G}□{RESET} Güvenlik yamaları otomatik uygulanıyor
  {G}□{RESET} Log yönetimi ve izleme (SIEM) aktif

  {BW}Ağ:{RESET}
  {G}□{RESET} WAF (Web Application Firewall) aktif
  {G}□{RESET} DDoS koruması (CDN/cloudflare)
  {G}□{RESET} Rate limiting tüm API uç noktalarında aktif
  {G}□{RESET} Network segmentasyonu uygulanmış
    """)
    pause()

# ══════════════════════════════════════════════════════════════════
#  ANA MENÜ
# ══════════════════════════════════════════════════════════════════
def show_main_menu():
    banner_main()
    print(f"  {DIM}═══════════════════════════════════════════════════════{RESET}")
    print(f"  {BW}RECON SUITE{RESET} {DIM}|{RESET} {BY}Profesyonel Güvenlik Keşif Araç Seti{RESET}")
    print(f"  {DIM}Sürüm: 9.1 | Eğitim & Savunma Amaçlıdır{RESET}")
    print(f"  {DIM}═══════════════════════════════════════════════════════{RESET}\n")
    print(f"  {C}[1]{RESET}  Bu araç ne işe yarıyor?")
    print(f"  {C}[2]{RESET}  Bu araç nasıl kullanılır?")
    print(f"  {C}[3]{RESET}  Önemli kurallar / Yasal uyarı")
    print(f"  {C}[4]{RESET}  {BY}Gizli menü{RESET} — özel araçlar")
    print(f"  {C}[5]{RESET}  {BM}İstihbari menü{RESET} — üst düzey araçlar")
    print(f"  {C}[6]{RESET}  {G}Ana menü{RESET} — standart araçlar")
    print(f"  {C}[7]{RESET}  {BR}Kritik araçlar{RESET}")
    print(f"  {C}[8]{RESET}  {BB}International araçlar{RESET}")
    print(f"  {C}[9]{RESET}  {BG}Savunma araçları{RESET} (Blue Team)")
    print(f"  {DIM}[0]{RESET}  {DIM}Çıkış{RESET}")
    print(f"\n  {DIM}────────────────────────────────────────────────────{RESET}")

def main():
    # Bağımlılık kontrolü
    missing = []
    try:
        import requests
    except ImportError:
        missing.append("requests")
    try:
        from colorama import init
    except ImportError:
        missing.append("colorama")

    if missing:
        print(f"[!] Eksik modüller: {', '.join(missing)}")
        print(f"[!] Kur: pip install {' '.join(missing)}")
        sys.exit(1)

    while True:
        show_main_menu()
        choice = input(f"\n  {BC}[?]{RESET} Seçiminiz: ").strip()
        if choice == "0":
            clear()
            print(f"\n  {BG}Çıkış yapılıyor... Güvenli araştırmalar!{RESET}\n")
            sys.exit(0)
        elif choice == "1": menu_about()
        elif choice == "2": menu_howto()
        elif choice == "3": menu_rules()
        elif choice == "4": menu_hidden()
        elif choice == "5": menu_intelligence()
        elif choice == "6": menu_standard()
        elif choice == "7": menu_critical()
        elif choice == "8": menu_international()
        elif choice == "9": menu_defense()
        else:
            warn("Geçersiz seçim!")
            time.sleep(0.8)

if __name__ == "__main__":
    main()
