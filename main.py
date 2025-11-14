import sys
import shutil
import subprocess

#executing file
def exec_file(execFind):
    subprocess.Popen(execFind)
#error message
def error(cmd, cmdSpl):
    match cmdSpl[0]:
        case "type":
            print(*cmdSpl[1:],": not found",sep="")
        case _:
            print(f"{cmd}: command not found")
commands = {"exit", "exit 0", "echo", "type", "./"}
def echo_cmd(cmdSpl):
    print(* cmdSpl[1:])
#exit command
def exit_cmd(cmdSpl):
    match cmdSpl[0]:
        case "exit":
            sys.exit(0)
        case _:
            if cmdSpl[0] == "exit" and cmdSpl[1] == "0" :
                sys.exit(0)
            else :
                error(cmdSpl) 
#type command                
def type_cmd(cmdSpl, cmd):
    find = shutil.which(cmdSpl[1])
    if cmdSpl[1] in commands:
        print(cmdSpl[1], "is a shell builtin")
        return  
    elif cmdSpl[1] != commands and not find:
        error(cmd, cmdSpl)            
    else: print(cmdSpl[1],"is", find)
#executing commands
def cmdexec():
    sys.stdout.write("$ ")
    cmd = input()
    cmdSpl = cmd.split(" ")
    execSpl = cmd.split("./")
    cmdSpl = cmd.split(" ")
    cmdf = cmd.find("./",0)

    match cmdSpl[0]:
        case "echo":
            echo_cmd(cmdSpl)
        case "exit":
            exit_cmd(cmdSpl)
        case "type":
            type_cmd(cmdSpl, cmd)
        case _:
            if  cmdf == 0:
                execFind = shutil.which(execSpl[1])
                exec_file(execFind)
                return
            else:
                error(cmd, cmdSpl)
def main():
    while True:
        cmdexec()

if __name__ == "__main__":
    main()