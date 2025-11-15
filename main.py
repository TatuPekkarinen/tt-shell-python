import sys
import shutil
import subprocess

commands = {"exit", "echo", "type"}

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

#echo command
def echo_cmd(cmdSpl):
    print(* cmdSpl[1:])

#exit command
def exit_cmd(cmdSpl):
    match cmdSpl[0]:
        case "exit":
            sys.exit(0)
        case _:
            error(cmdSpl) 

#type command
def type_cmd(cmdSpl, cmd):
    if cmd == "type":
        error(cmdSpl, cmd)
        return
    
    file_find = shutil.which(cmdSpl[1])
    if cmdSpl[1] in commands:
        print(cmdSpl[1], "is a shell builtin")
        return  
    elif cmdSpl[1] != commands and not file_find:
        error(cmd, cmdSpl)            
    else: print(cmdSpl[1],"is", file_find)

#executing commands
def cmdexec():
    sys.stdout.write("$ ")
    cmd = input()
    cmdSpl = cmd.split(" ")
    execSpl = cmd.split(".")
    cmdSpl = cmd.split(" ")

    match cmdSpl[0]:
        case "echo":
            echo_cmd(cmdSpl)
        case "exit":
            exit_cmd(cmdSpl)
        case "type":
            type_cmd(cmdSpl, cmd)
        case _:
            if  cmd == "." + execSpl[1]:
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