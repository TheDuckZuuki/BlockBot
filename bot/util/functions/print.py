from colorama import Fore, init
from datetime import datetime

init(convert=True)

def pint(message, type):
    now = datetime.now()
    curr_time = now.strftime("%H:%M:%S")
    timeformat = "[" + curr_time + " " + type + "]: "
    if type == "WARN":
        print(Fore.YELLOW + timeformat + message + Fore.RESET)
    elif type == "INFO":
        print(Fore.RESET + timeformat + message + Fore.RESET)
    elif type == "ERROR":
        print(Fore.RED + timeformat + message + Fore.RESET)
