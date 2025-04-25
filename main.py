def print_todo_header():
    print("+-------------------------------------+")
    print("|  _____  ___  ____   ___      __     |")
    print("| |_   _|/ _ \\|  _ \\ / _ \\    |  |    |")
    print("|   | | | | | | | | | | | |   |  |    |")
    print("|   | | | |_| | |_| | |_| |   |__|    |")
    print("|   |_|  \\___/|____/ \\___/    |__|    |")
    print("|                                     |")
    print("|   [A] Class 1                       |")
    print("|   [B] Class 2                       |")
    print("|   [C] Class 3                       |")
    print("|   [D] Class 4                       |")
    print("|                                     |")
    print("+-------------------------------------+")

def main():
    print_todo_header()
    
    # Get user input
    user_command = input("Enter command here: ")
    
    # Here you can add logic to handle the user's command
    if user_command.upper() == 'A':
        print("You selected Class 1")
    elif user_command.upper() == 'B':
        print("You selected Class 2")
    elif user_command.upper() == 'C':
        print("You selected Class 3")
    elif user_command.upper() == 'D':
        print("You selected Class 4")
    else:
        print("Invalid command")

# This will run when the program starts
if __name__ == "__main__":
    main()