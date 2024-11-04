import secrets
import string
import json
import os
import re
import textwrap

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

    # Validate URL format
    url_regex = r'^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
    while True:
        url = input("URL: ")
        if re.match(url_regex, url):
            break
        else:
            print("Invalid URL. Example: https://example.com")

    uname = input("Username: ")

    # Check for password generation option
    passw_choice = input("Generate a strong password? (y/n): ")
    if passw_choice.lower() == 'y':
        passw = passgen()
        print(f"Generated Password: {passw}")
    else:
        while True:
            passw = input("Password: ")
            if len(passw) >= 8:
                break
            else:
                print("Password must be at least 8 characters long.")

    # Add notes or tags
    notes = input("Notes (optional): ")
    
    # Save the credentials
    if url not in cred:
        cred[url] = {}
    cred[url][uname] = {"password": passw, "notes": notes}

    with open("creds.json", "w") as f:
        json.dump(cred, f)

    print(f"Credentials for {uname} added successfully for {url}!")

   


def viewcred():
    # Check if the credentials file exists
    if not os.path.exists("creds.json"):
        print("No credentials file found.")
        return

    # Load credentials from the JSON file
    try:
        with open("creds.json", "r") as f:
            cred = json.load(f)
        
        # Check if there are any credentials stored
        if not cred:
            print("No credentials stored.")
            return

        # Ask if the user wants to search for specific credentials
        search_option = input("Do you want to search for specific credentials? (y/enter): ").strip().lower()
        
        if search_option == "y":
            search_term = input("Enter URL or username to search for: ").strip().lower()
            search_results = {}
            
            # Search through credentials for matching URLs or usernames with partial matching
            for url, accounts in cred.items():
                if search_term in url.lower():  # Partial match for URL
                    search_results[url] = accounts
                else:
                    # Partial match for usernames
                    for uname in accounts:
                        if search_term in uname.lower():
                            if url not in search_results:
                                search_results[url] = {}
                            search_results[url][uname] = accounts[uname]
            
            # Sort the results by URL
            sorted_results = dict(sorted(search_results.items()))

            # Display the search results
            if sorted_results:
                print("\nSearch Results:")
                for url, accounts in sorted_results.items():
                    print(f"\nURL: {url}")
                    for uname, details in accounts.items():
                        print(textwrap.indent(f"Username: {uname}", "    "))
                        print(textwrap.indent(f"Password: {details['password']}", "    "))
                        notes = details.get("notes", "None")
                        print(textwrap.indent(f"Notes: {notes}", "    "))
            else:
                print("No matching credentials found.")
        else:
            # Sort all credentials by URL for a complete view
            sorted_cred = dict(sorted(cred.items()))
            print("\nStored Credentials:")
            for url, accounts in sorted_cred.items():
                print(f"\nURL: {url}")
                for uname, details in accounts.items():
                    print(textwrap.indent(f"Username: {uname}", "    "))
                    print(textwrap.indent(f"Password: {details['password']}", "    "))
                    notes = details.get("notes", "None")
                    print(textwrap.indent(f"Notes: {notes}", "    "))

    except json.JSONDecodeError:
        print("Error: Unable to load credentials. The file may be corrupted.")


def passgen():
    
    # Define the character pool for password generation
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(12))
    print(f"Generated Password: {password}")
    return password  # Return the generated password for use in addcred


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
