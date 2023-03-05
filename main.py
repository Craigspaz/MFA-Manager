import pyotp
import os
import os.path
import datetime
import time
import signal
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto import Random

'''
    Encrypts the data with the secret password
'''
def encrypt(raw, secret_password):
    private_key = hashlib.sha256(secret_password.encode("utf-8")).digest()
    raw = raw + (AES.block_size - len(raw) % AES.block_size) * chr(AES.block_size - len(raw) % AES.block_size)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw.encode()))

'''
    Decrypts the data using the secret password
'''
def decrypt(cipher_text, secret_password):
    private_key = hashlib.sha256(secret_password.encode("utf-8")).digest()
    encoded_text = base64.b64decode(cipher_text)
    iv = encoded_text[:AES.block_size]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    value = (cipher.decrypt(encoded_text[AES.block_size:])).decode('utf-8')
    return value[:-ord(value[len(value)-1:])]

'''
    Manages the configuration file
'''
class Config_File:

    def __init__(self):
        print("Loading Config file...")
        first_opening = False
        if os.path.exists("./config.txt") == False:
            self.secret_password = input("Enter a password used to encrypt the secret tokens: ")
            open("./config.txt", "a").close()
            first_opening = True
        else:
            self.secret_password = input("Enter the password you used to encrypt the tokens: ")
        config_file = open("./config.txt", "r")
        self.items = []

        if first_opening:
            config_file.close()
            return # If this is the first time opening the file there are no tokens so skip trying to read them

        file_contents = ""

        for line in config_file:
            file_contents += line
        
        if len(file_contents) == 0:
            config_file.close()
            return # There are no tokens to decrypt

        config_file_contents = decrypt(file_contents, self.secret_password).split("\n")

        for line in config_file_contents:
            if len(line) == 0:
                continue
            split_line = line.split("|")
            tmp = {"Name": split_line[0].strip(), "URL": split_line[1].strip(), "SECRET": split_line[2].strip()}
            self.items.append(tmp)
        config_file.close()

    '''
        Adds item into the configuration file
    '''
    def add_item(self, name, url=None, secret=None):
        if secret != None or url != None and secret != url:
            self.items.append({"Name": name, "URL": str(url), "SECRET": str(secret)})
        else:
            print("URL or Secret Must be set when adding a value")
            return

        payload = ""
        for item in self.items:
            payload += str(item["Name"]) + "|" + str(item["URL"]) + "|" + str(item["SECRET"]) + "\n"
        try:
            encrypted_payload = encrypt(payload, self.secret_password)
        except Exception as e:
            print("Caught exception during encryption: " + str(e))

        config_file = open("./config.txt", "w")
        config_file.write(str(encrypted_payload.decode("utf-8")))
        config_file.close()

    '''
        Removes item from the configuration file
    '''
    def remove_item(self, item_name):
        config_file = open("./config.txt", "w")
        item_to_remove = None
        payload = ""
        for item in self.items:
            if item["Name"] == item_name:
                item_to_remove = item
                continue
            payload += str(item["Name"]) + "|" + str(item["URL"]) + "|" + str(item["SECRET"]) + "\n"
        try:
            encrypted_payload = encrypt(payload, self.secret_password)
        except:
            print("Caught exception during encryption: " + str(e))
        config_file.write(str(encrypted_payload.decode("utf-8")))
        config_file.close()
        if item_to_remove != None:
            self.items.remove(item_to_remove)


'''
    Manages the terminal interface for the application
'''
class Terminal:

    def __init__(self):
        print("Starting up terminal")
        self.config_file = Config_File()
        self.current_menu = 0 # 0 is main menu. 1 is view tokens. 2 is add new token. 3 is remove token. 4 is the closing state
        signal.signal(signal.SIGINT, self.sigint_handler)
        self.run()

    '''
        Runs the terminal
    '''
    def run(self):
        while True:
            if self.current_menu == 0:
                self.print_main_menu()
                user_input = input()
                if self.parse_input(user_input) == False:
                    continue
            elif self.current_menu == 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                self.print_view_token_menu()
                time.sleep(1)
            elif self.current_menu == 2:
                self.print_add_new_token_menu()
                self.print_main_menu()
                user_input = input()
                if self.parse_input(user_input) == False:
                    continue
            elif self.current_menu == 3:
                self.print_remove_token_menu()
                self.current_menu = 0
            elif self.current_menu == 4:
                print("Shutting down...")
                exit(0)


    '''
        Prints out the Main Menu
    '''
    def print_main_menu(self):
        print("Enter the number of the item you want to do: ")
        print("Enter 1 to view OTP values")
        print("Enter 2 to add a new OTP token")
        print("Enter 3 to Remove an existing OTP token")
        print("Enter 4 to quit")

    '''
        Parses input and sets the menu accordingly
    '''
    def parse_input(self, user_input):
        try:
            value = int(user_input)
            if value == 0:
                self.current_menu = 0
            elif value == 1:
                self.current_menu = 1
            elif value == 2:
                self.current_menu = 2
            elif value == 3:
                self.current_menu = 3
            else:
                self.current_menu = 4
        except:
            print("Value was not an integer...")
            return False

    '''
        Prints out the view token menu
    '''
    def print_view_token_menu(self):
        print("Tokens: (Press Cntrl-C to go back to main menu)")
        print("Token Name | Current Token | Time Left")
        for item in self.config_file.items:
            value = None
            totp = None
            if item["URL"] == "None" and item["SECRET"] != "None":
                totp = pyotp.TOTP(item["SECRET"])
            elif item["SECRET"] == "None" and item["URL"] != "None":
                totp = pyotp.parse_uri(item["URL"])
            else:
                print("Value is not valid. URL: " + str(item["URL"]) + " Secret: " + str(item["SECRET"]))
            time_remaining = int(totp.interval - datetime.datetime.now().timestamp() % totp.interval)
            value = totp.now()
            print(item["Name"] + " | " + str(value) + " | " + str(time_remaining))

    '''
        Prints the add new token menu
    '''
    def print_add_new_token_menu(self):
        print("Add New Token")
        token_name = input("Enter the name of the token (this is a friendly name for you): ")
        token_name = token_name.strip()
        token_url = None
        token_secret = None
        is_token_url_or_secret = input("Enter 1 if secret is a URL or 2 if the value is a secret value: ")
        try:
            value = int(is_token_url_or_secret.strip())
            if value == 1:
                token_url = input("Enter secret URL: ")
                token_url = token_url.strip()
            elif value == 2:
                token_secret = input("Enter secret value: ")
                token_secret = token_secret.strip()
            else:
                print("Unexpected value entered. Going back to main menu")
                self.current_menu = 0
            self.config_file.add_item(token_name, token_url, token_secret)
        except:
            print("Value entered is not a number. Going back to main menu")
            self.current_menu = 0

    '''
        Print the remove token menu
    '''
    def print_remove_token_menu(self):
        token_name = input("Enter the name of the token that you would like to remove (Press Cntrl-C to go back to main menu): ")
        self.config_file.remove_item(token_name)
        print("Succesfully removed token")

    '''
        Handles the sigint signal (cntrl-c)
    '''
    def sigint_handler(self, sig, frame):
        if self.current_menu != 0:
            self.current_menu = 0
        else:
            exit(1)

Terminal()