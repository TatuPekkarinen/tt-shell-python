import pprint
import shlex
import time, datetime
import sys, os, shutil
import subprocess, webbrowser
from collections import deque
from pathlib import Path
import socket, json

GREEN = '\033[92m'
TITLE1 = '\033[94m'
TITLE2 = '\033[95m'
WARNING = '\033[91m'
RESET = '\033[0m'

#current directory
script_directory = Path(__file__).parent

#global deque of command history
history = deque(maxlen=25)

def scan(current_port, sock_data, status, sock):
    if status == 0:
        print(f"Port / {current_port} / {GREEN}{sock_data[str(status)]}{RESET}")
    elif status > 0: 
        print(f"Port / {current_port} / {WARNING}{sock_data[str(status)]}{RESET}")
    else: 
        print(f"Port / {current_port} / {WARNING}{sock_data[str(status)]}{RESET}")
    sock.close()
    return

#general error handler (Work in progress)
def error_handler(command, command_split):
    print(f"{WARNING}Command not found{RESET} => {command}")
    command_split.clear()
    return

#connectivity tester and port scanner
def connection_portal(command, command_split):
    def port_valid(port: int) -> bool:
        maximum_port = 65535
        return 0 <= port <= maximum_port

    if len(command_split) > 2:
        file_path = script_directory / 'socket.json'
        with file_path.open('r') as file:
            sock_data = json.load(file)

        if command_split[1] == 'range':
            if len(command_split) <= 3:
                print(f"{WARNING}invalid arguments{RESET} => 3 given / 4 expected")
                return

            print(f"{GREEN}Starting scan from {command_split[2]} to {command_split[3]}{RESET}")
            for port_iterator in range(int(command_split[2]), int(command_split[3]) + 1):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)

                LOCALHOST = '127.0.0.1'
                PORT = int(port_iterator)

                if not port_valid(PORT):
                    print(f"Port ({port_iterator}) invalid / {WARNING}Not in range{RESET}")
                    sock.close()
                    return
                
                current_port = PORT
                status = sock.connect_ex((LOCALHOST, PORT))
                scan(current_port, sock_data, status, sock)  
                return

        else:   
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)

            try: HOST = socket.gethostbyname(str(command_split[1]))
            except socket.gaierror: 
                print(f"{WARNING}exception => socket.gaierror{RESET} / Unable to open website")
                return
            
            PORT = int(command_split[2])

            if not port_valid(PORT):
                print(f"{WARNING}Port invalid{RESET} / (Not in range 0/65535)")
                sock.close()
                return
            
            print(f"{GREEN}connnecting to {HOST} from {PORT}{RESET}")
            current_port = PORT
            status = sock.connect_ex((HOST, PORT))
            if status == 0: scan(current_port, sock_data, status, sock)
            else: scan(current_port, sock_data, status, sock) 
            return

    else: 
        error_handler(command, command_split)
        return

#executing file
def execute_file(command, command_split):
    if len(command_split) < 2:
        error_handler(command, command_split)
        return
    
    execute_path = shutil.which(command_split[1])

    if execute_path is None:
        print(f"{WARNING}File not found{RESET} => {command_split[1]}")
        return
    
    if os.access(str(execute_path), os.X_OK):
        print(f"{GREEN}Opening file =>{RESET} {execute_path}")
        time.sleep(1)
        subprocess.run(execute_path, shell=False)
        return

    else: 
        error_handler(command, command_split)
        return

#website opener
def open_website(command, command_split):
    match len(command_split):
        case 2:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            try: HOST = socket.gethostbyname(str(command_split[1]))

            except socket.gaierror:
                print(f"{WARNING}exception => socket.gaierror{RESET} / Unable to open website")
                return
            
            HTTPS_PORT = 443

            print(f"CONNECTION TEST => {GREEN}Connection to {HOST} from {HTTPS_PORT}{RESET}")
            status = sock.connect_ex((HOST, HTTPS_PORT))

            if status == 0:
                print(f"CONNECTION SUCCESFUL => {GREEN}Accessing website{RESET} / {command_split[1]}")
                webbrowser.open(command_split[1])
                return

            else: 
                print(f"{WARNING}Connection failed{RESET} / Unable to open website")
                return
        case _: 
            error_handler(command, command_split)
            return
    
#environment variables   
def environ_print(command, command_split):
    if len(command_split) == 1:
            envar = os.environ
            pprint.pprint(dict(envar), width=5, indent=5) 
            return
    else: 
        error_handler(command, command_split)
        return

#builtin checker
def type_command(command, command_split):
    def file_check() -> bool:
        if type_file is not None:
            return os.access(type_file, os.X_OK)

    match len(command_split):
        case 2:
            type_file = shutil.which(command_split[1])
            if command_split[1] in commands:
                print(f"{command_split[1]} // {commands.get(command_split[1])}")
                return  

            if file_check() == True:
                print(f"{command_split[1]} => {type_file}")
                return 
            
            else: 
                error_handler(command, command_split)
                return
        case _: 
            print(f"{WARNING}invalid arguments{RESET} => 1 given / 2 expected")
            return

#change directory
def change_directory(command, command_split):
    directory = str(command_split[1])
    if len(command_split) > 1:

        if command_split[1] == 'reset':
            os.chdir(script_directory)
            return

        if os.access(str(directory), os.X_OK):
            try: 
                os.chdir(str(directory))
                return
            except: 
                print(f"{WARNING}Exception raised{RESET} => not a directory")
                return
        else: 
            print(f"{WARNING}Unable to find the directory{RESET} => {directory}")
            return
    else: 
        error_handler(command, command_split)
        return

#history
def modify_history(command, command_split):
    if len(command_split) == 2:
        match command_split[1]:
            case 'clear':
                history.clear()
            case _: error_handler(command, command_split)

    if len(command_split) == 1:
        if command_split[0] == 'history':
            print(F"\n{GREEN}Command history{RESET}")
            for element in history: print(f"{GREEN}=>{RESET} {element}")
            return
    return

#wrappers for external tools
def wrappers(command, command_split):
    run_failure = lambda: print(f"{WARNING}Failed to run command{RESET} => {command}")
    match command_split[0]:
        case 'curl':
            try: subprocess.run(command_split)
            except: run_failure()
            return
        case 'git': 
            try: subprocess.run(command_split)
            except: run_failure()
            return
        case _: 
            error_handler(command, command_split)
            return

#all usable commands
commands = {
    "exit": lambda command, command_split: sys.exit(0),
    "python": lambda command, command_split: print(sys.version),
    "echo": lambda command, command_split: print(*command_split[1:]),
    "com": lambda command, command_split: pprint.pprint(dict(commands), width = 5),
    "git": wrappers,
    "curl": wrappers,
    "type": type_command,
    "web": open_website,
    "env": environ_print,
    "file": execute_file,
    "change": change_directory,
    "con": connection_portal,
    "history": modify_history
}

#executing commands
def command_execute(current_directory):
    sys.stdout.write(f"[{current_directory}]{GREEN} => {RESET}")

    try:
        command = input()
        history.append(command)
        if command == '': return
        try:command_split = shlex.split(command) 

        except ValueError: 
            print(f"{WARNING}Invalid input{RESET} => {command}")
            return
        
        for element in range(len(command_split)):
            if len(command_split[element]) >= 63:
                print(f"{WARNING}Command too long{RESET} => 63 (limit)")
                return
    
        if command_split[0] in commands:
            execute = commands.get(command_split[0], error_handler)
            execute(command, command_split)
        
        else: error_handler(command, command_split)

    except KeyboardInterrupt: 
        print(f"\n{WARNING}Keyboard interrupt{RESET}")
        return

def main():
    date = datetime.datetime.now()
    print(f"{TITLE1}tt-shell [{sys.argv[0]}]{RESET} / {TITLE2}{date}{RESET}")
    while True:
        current_directory = os.getcwd()
        command_execute(current_directory)

if __name__ == "__main__":
    main()