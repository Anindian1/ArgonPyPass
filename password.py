import secrets
import string
import json
import os
import re

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



# Load existing credentials from JSON file (if it exists)
if os.path.exists("creds.json"):
    try:
        with open("creds.json", "r") as f:
            content = f.read().strip()  # Read and strip whitespace
            if content:  # Check if content is not empty
                cred = json.loads(content)  # Load only if there is content
            else:
                print("Warning: creds.json is empty. Starting with empty credentials.")
    except json.JSONDecodeError:
        print("Error: creds.json is corrupted or contains invalid JSON. Starting with empty credentials.")
        cred = {}
else:
    print("creds.json not found. Starting with empty credentials.")
    
    
def addcred():
    
    print("Enter Credentials:\n")
    
    # Validate URL
    
    url_regex = r'^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'  # Basic URL regex
    while True:
        url = input("URL: ")
        if re.match(url_regex, url):
            break
        else:
            print("Invalid URL format. Please enter a valid URL (e.g., http://example.com).")

    uname = input("Username: ")
    
    # Validate Password
    
    while True:
        passw = input("Password: ")
        if len(passw) >= 8:
            break
        else:
            print("Password must be at least 8 characters long. Please try again.")

    # Check if the URL already exists in the credentials
    
    if url not in cred:
        cred[url] = {}  # Create a new entry if it doesn't exist
        

    # Check for existing username
    if uname in cred[url]:
        print(f"Username '{uname}' already exists for {url}. Please use a different username.")
    else:
        cred[url][uname] = passw  # Add the new username and password

        # Save to the JSON file
        
        with open("creds.json", "w") as f:
            json.dump(cred, f)

        print(f"Credentials for {uname} added successfully for {url}!")

   

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
