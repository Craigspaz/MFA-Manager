# MFA-Manager

This tool generates tokens like Google Authenticator. It currently only supports time based tokens.

## Installation

### Prerequisites
1. Python 3
1. PIP
1. pipenv

1. Clone the repo to your computer
1. Run the command below when in a command prompt/terminal in the directory where the Pipfile was cloned to. This will install the required packages
```
pipenv install
```

### How to run
1. Next enter the virtual environment's shell and then run the main.py file or do it all at once with the command below
```
pipenv run ./main.py
```
You will then see the text below
```
Starting up terminal
Loading Config file...
Enter a password used to encrypt the secret tokens:
```
1. Follow the onscreen prompt and enter a password. This password will be used to encrypt a configuration file where the secret tokens will be stored. After setting the password you should see the screen below.
```
Enter the number of the item you want to do: 
Enter 1 to view OTP values
Enter 2 to add a new OTP token
Enter 3 to Remove an existing OTP token
Enter 4 to quit
```
You can enter the number 1 and press enter to view your current OTP tokens. You can enter the number 2 and press enter to add a new token. You can enter the number 3 and press enter to remove an existing token. You can enter the number 4 and press enter to quit.

Note: If you already set a password you will see a slightly different prompt when you launch the application. It will look like the output below. You will need to use the same password you entered in the steps above.
```
Starting up terminal
Loading Config file...
Enter the password you used to encrypt the tokens:
```

### How to start over
If you set the wrong password or you need to change the password you should make note of your current tokens. A future feature may add a way to address this in the application so you don't lose all of your tokens. 
1. Find the config.txt file. It should be in the same folder as the main.py file.
1. Delete the file. this will force the code to generate a new one and ask for a password (NOTE: This will mean you lose all of your tokens)

## Viewing Tokens
When you launch the application and pick option 1 you should see a screen like the one below.
```
Tokens: (Press Cntrl-C to go back to main menu)
Token Name | Current Token | Time Left
TestToken1 | 843204 | 3
TestToken6 | 842049 | 3
TestToken7 | 784297 | 3
TestToken8 | 249720 | 3
```

The first column is the friendly name of the token. This is so you can find which tokens are for what application. Currently these names are not changable

The second column is the current token value.

The third column is the time left in seconds until the token changes

The page will automatically refresh once every second. If you want to go back to the main menu press Cntrl-C on your keyboard.

## Adding a new Token
1. Pick option 2 in the main menu
1. Follow the on screen instructions

Below is an example of adding a new token
```
Enter the number of the item you want to do: 
Enter 1 to view OTP values
Enter 2 to add a new OTP token
Enter 3 to Remove an existing OTP token
Enter 4 to quit
2
Add New Token
Enter the name of the token (this is a friendly name for you): Sample Token
Enter 1 if secret is a URL or 2 if the value is a secret value: 2
Enter secret value: JBSWY3DPEHPK3PXP
Enter the number of the item you want to do: 
Enter 1 to view OTP values
Enter 2 to add a new OTP token
Enter 3 to Remove an existing OTP token
Enter 4 to quit
1
Tokens: (Press Cntrl-C to go back to main menu)
Token Name | Current Token | Time Left
Sample Token | 156225 | 19
```

## Removing a Token
1. Pick option 3 in the main menu
1. Follow the on screen instructions

Below is an example of adding a new token
```
Enter the number of the item you want to do: 
Enter 1 to view OTP values
Enter 2 to add a new OTP token
Enter 3 to Remove an existing OTP token
Enter 4 to quit
3
Enter the name of the token that you would like to remove (Press Cntrl-C to go back to main menu): Sample Token
Succesfully removed token
Enter the number of the item you want to do:
Enter 1 to view OTP values
Enter 2 to add a new OTP token
Enter 3 to Remove an existing OTP token
Enter 4 to quit
1
Tokens: (Press Cntrl-C to go back to main menu)
Token Name | Current Token | Time Left
```