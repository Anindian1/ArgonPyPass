import secrets
import string
import json
import os

cred={}


def menuchoice():
    print("Choose an Option : \n 1. View Creds \n 2. Manage Creds \n 3. Generate Password \n 4. Exit")
    menu = int(input("Enter Choice: "))
    return menu  # Return the menu choice for further action


def addcred():
    # Functionality to add credentials will be implemented here
    print("Add Credentials functionality not yet implemented.")


def delcred():
    # Functionality to delete credentials will be implemented here
    print("Delete Credentials functionality not yet implemented.")


def editcred():
    # Functionality to edit credentials will be implemented here
    print("Edit Credentials functionality not yet implemented.")


def credman():
    cmchoice = int(input(" 1. Add Credentials \n 2. Edit Credentials\n 3. Delete Credentials\n Enter Your Choice: "))

    if cmchoice == 1:
        addcred()
    elif cmchoice == 2:
        editcred()
    elif cmchoice == 3:
        delcred()
    else:
        print("Invalid Choice. Please try again.")

def addcred() :
    
    
    print("Enter Credentials:\n")
    uname = input("Username: ")
    passw = input("Password: ")
    url = input("URL: ")

    # Add to the `cred` dictionary with URL as the key
    cred[url] = {"username": uname, "password": passw}

    # Save `cred` to a JSON file for persistence
    with open("creds.json", "w") as f:
        json.dump(cred, f)
    
    print(f"Credentials for {url} added successfully!")



def viewcred():
    print("View Credentials functionality not yet implemented.")


def passgen():
    print("Generate Password functionality not yet implemented.")


def main():
    choice = menuchoice()

    if choice == 1:
        viewcred()
    elif choice == 2:
        credman()
    elif choice == 3:
        passgen()
    elif choice == 4:
        print("Exiting the program.")
    else:
        print("Invalid Choice. Please try again.")


# Call the main function to start the program
main()
