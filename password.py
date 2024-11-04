import secrets
import string
import json
import os
import re
import textwrap

# Global variable to store credentials
cred = {}

# Load existing credentials from JSON file (if it exists)
def load_credentials():
    global cred
    if os.path.exists("creds.json"):
        try:
            with open("creds.json", "r") as f:
                content = f.read().strip()
                if content:
                    cred = json.loads(content)
                else:
                    print("Warning: creds.json is empty. Starting with empty credentials.")
        except json.JSONDecodeError:
            print("Error: creds.json is corrupted or contains invalid JSON. Starting with empty credentials.")
            cred = {}
    else:
        print("creds.json not found. Starting with empty credentials.")

# Menu option selection
def menuchoice():
    print("Choose an Option: \n 1. View Creds \n 2. Manage Creds \n 3. Generate Password \n 4. Exit")
    return int(input("Enter Choice: "))

# Function to generate a strong password
def passgen():
    # User input for password length
    while True:
        try:
            length = int(input("Enter the desired password length (minimum 8): "))
            if length < 8:
                print("Password length must be at least 8.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")

    # Ensuring password contains at least one character from each category
    upper = secrets.choice(string.ascii_uppercase)
    lower = secrets.choice(string.ascii_lowercase)
    digit = secrets.choice(string.digits)
    punctuation = secrets.choice(string.punctuation)

    # Ensure the remaining characters are randomly chosen from all categories
    remaining_length = length - 4  # We've already chosen 4 characters

    if remaining_length > 0:
        characters = string.ascii_letters + string.digits + string.punctuation
        password = upper + lower + digit + punctuation + ''.join(secrets.choice(characters) for _ in range(remaining_length))
    else:
        password = upper + lower + digit + punctuation  # Just return the minimum characters if length is exactly 4

    # Shuffle the password to avoid any predictable sequences
    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    final_password = ''.join(password_list)

    print(f"Generated Password: {final_password}")
    return final_password

# Function to add new credentials
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
    passw = passgen() if passw_choice.lower() == 'y' else input("Password (8+ chars): ")

    notes = input("Notes (optional): ")
    if url not in cred:
        cred[url] = {}
    cred[url][uname] = {"password": passw, "notes": notes}

    with open("creds.json", "w") as f:
        json.dump(cred, f)

    print(f"Credentials for {uname} added successfully for {url}!")

# Function to delete credentials
def delcred():
    if not os.path.exists("creds.json"):
        print("No credentials file found.")
        return

    try:
        with open("creds.json", "r") as f:
            current_cred = json.load(f)
        if not current_cred:
            print("No credentials stored.")
            return

        url_search = input("Enter part of the URL of the credential to delete: ").strip().lower()
        matching_urls = {url: current_cred[url] for url in current_cred if url_search in url.lower()}
        
        if not matching_urls:
            print("No matching URLs found.")
            return

        # User selects URL to delete from
        url_choice = int(input("Select the URL by entering the corresponding number: "))
        selected_url = list(matching_urls.keys())[url_choice - 1]
        uname = select_username(current_cred, selected_url)
        if uname:
            del current_cred[selected_url][uname]  
            if not current_cred[selected_url]:
                del current_cred[selected_url]

            with open("creds.json", "w") as f:
                json.dump(current_cred, f)
            print(f"Credentials for {uname} at {selected_url} have been deleted successfully.")
    except json.JSONDecodeError:
        print("Error: Unable to load credentials. The file may be corrupted.")

# Helper function to select username based on URL
def select_username(cred_dict, url):
    usernames = list(cred_dict[url].keys())
    if not usernames:
        print(f"No usernames found under {url}.")
        return None
    print(f"Usernames under {url}:")
    for idx, uname in enumerate(usernames, 1):
        print(f"{idx}. {uname}")
    uname_choice = int(input("Select the username by entering the corresponding number: "))
    return usernames[uname_choice - 1] if 1 <= uname_choice <= len(usernames) else None

# Function to edit credentials
def editcred():
    if not os.path.exists("creds.json"):
        print("No credentials file found.")
        return

    try:
        with open("creds.json", "r") as f:
            current_cred = json.load(f)
        if not current_cred:
            print("No credentials stored.")
            return

        url_search = input("Enter part of the URL of the credential to edit: ").strip().lower()
        matching_urls = {url: current_cred[url] for url in current_cred if url_search in url.lower()}
        
        if not matching_urls:
            print("No matching URLs found.")
            return

        url_choice = int(input("Select the URL by entering the corresponding number: "))
        selected_url = list(matching_urls.keys())[url_choice - 1]
        uname = select_username(current_cred, selected_url)

        if uname:
            selected_cred = current_cred[selected_url][uname]
            print(f"Current Password: {selected_cred.get('password', 'Not Set')}")
            print(f"Current Notes: {selected_cred.get('notes', 'Not Set')}")

            field_choice = input("What would you like to edit? (1. Password / 2. Notes): ")

            if field_choice == "1":
                passw_choice = input("Generate a new strong password? (y/n): ")
                new_password = passgen() if passw_choice.lower() == 'y' else input("Enter new password: ")
                selected_cred["password"] = new_password
            elif field_choice == "2":
                selected_cred["notes"] = input("Enter new notes: ")

            with open("creds.json", "w") as f:
                json.dump(current_cred, f)
            print(f"Credentials for {uname} at {selected_url} have been updated successfully.")
    except json.JSONDecodeError:
        print("Error: Unable to load credentials. The file may be corrupted.")

# Function to manage credentials
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

# Function to view stored credentials
def viewcred():
    if not os.path.exists("creds.json"):
        print("No credentials file found.")
        return

    try:
        with open("creds.json", "r") as f:
            cred = json.load(f)

        if not cred:
            print("No credentials stored.")
            return

        search_option = input("Do you want to search for specific credentials? (y/enter): ").strip().lower()
        if search_option == "y":
            search_term = input("Enter URL or username to search for: ").strip().lower()
            search_results = {url: accounts for url, accounts in cred.items() if search_term in url.lower()}

            if search_results:
                display_credentials(search_results)
            else:
                print("No matching credentials found.")
        else:
            display_credentials(cred)
    except json.JSONDecodeError:
        print("Error: Unable to load credentials. The file may be corrupted.")

# Helper function to display credentials
def display_credentials(cred_dict):
    sorted_cred = dict(sorted(cred_dict.items()))
    print("\nStored Credentials:")
    for url, accounts in sorted_cred.items():
        print(f"\nURL: {url}")
        for uname, details in accounts.items():
            print(textwrap.indent(f"Username: {uname}", prefix="    "))
            print(textwrap.indent(f"Password: {details['password']}", prefix="    "))
            print(textwrap.indent(f"Notes: {details.get('notes', 'None')}", prefix="    "))

# Main Function
def main():
    load_credentials()
    while True:
        choice = menuchoice()
        if choice == 1:
            viewcred()
        elif choice == 2:
            credman()
        elif choice == 3:
            passgen()
        elif choice == 4:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
