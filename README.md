Minimal Python Shell

This project is a small command-line shell written in Python. It supports a few basic builtin commands and can also run executable files from the current directory. The goal is to provide a lightweight example of how a shell parses input and decides what to do with it.

This was a codecrafters challenge I did without AI and im planning to add my own functionalities to the shell.

LIST OF USABLE COMMANDS

            Exit - exits the program
            Type - tells if the file is in the directory or if the command is builtin
            Echo - echoes the text
            ./ - executes a given file (for example ./cmd)
            
CODECRAFTERS STARTER CODE
            
            import sys
            
            def main():
                sys.stdout.write("$ ")
            
            if __name__ == "__main__":
                main()
