# SATStracker: Track Your Bitcoin Balance

#### Video Demo: https://youtu.be/rcwPCWZqK_U

#### Description:

SATStracker is a bitcoin value tracker. The user creates an account in which the amount and value of their bitcoin is stored.The user is able to log withdrawals and deposits, each time the program keeps track of their account balance.

This particular program exists because of the frustration the programmer felt with trying to keep on top of the value of his bitcoin assets in the less familiarly used bitcoin unit of sats (explained below).

Thus, Satstracker makes it easier for users who track Bitcoin's value in "Satoshis" or "Sats" (1 sat = 1/100000000 BTC) to keep on top of their asset's value. The program also supports converting the value of bitcoin to local currencies.

#### Code Description:

SATStracker code implementation required the following modules/libraries;
* csv
* sys
* requests
* datetime
* os
* re

The code contains a class representing a user account with methods for deposit, withdrawal, and updating account information. There is a main function that runs the SATSTracker program, and five additional functions accessed by the main function.

From top down the code design is as follows;

First, the required modules are imported, and then a group of global constants are declared for better readability.

Next, the class (Account) is defined with the following methods;
* An __init__ constructor to initialise an account instance with a name and balance
* A class method to get an existing account or create a new one.
* A class method to create a new account (called by the other class methods that create and update changes)
* A class method to update the amount in the account and write changes to the database.
* A class method to update the database of accounts
* Two decorated instance functions that get and set the properties "name" and "class"
* Two instance functions that withdraw, and deposit to the user's accounts

After the class is defined, the main function is defined. The main function first creates an object (account) from the Account class by calling the class method that gets an existing account or creates a new one. It then starts a loop that asks the user for the service they would like, after collecting the user's input, the function then responds to the user based on a series of if-else conditional statements.

Each statement prints an output to the user, and then calls a function that presents them a final option to quit or repeat the loop to access another service.

After the main function, there is a convert function. This function takes one parameter(the user's balance) and converts it to any local currency of their choice.

The function contains requests to two APIs, one to coingecko that returns the price of bitcoin in USD and another to openexchangerates that returns the exchange rate of a specified local currency to dollars. The rest of the function converts the local currency to USD and then to BTC and then to Sats. It returns the local currency specified by the conversion.

Importantly, the exchange rates are stored by the function in a csv file, effectively caching the rates for later use without needing to collect the information from the internet everytime.

There is also a function to check the exchange rates csv files last modified date to assess whether the data in them is too old and requires a new update. This function returns a boolean value that stipulates True when the file is too old (last modified over 30mins earlier). This informs the convert function whether to perform a get request on the internet or get information from the cached data on the csv.

A seperate function handles presenting the services to the user and returning their response for evaluation by the main function. A similar function (called at the end of every main function's response to a user request), presents two options at the end of a user experience to either quit the program or request another service.

The last function is used to format a number of dashes used in the program UI.

Overall, SATSTracker is designed to create and store user account information in csv files, update the information as requested by the user and perform API requestst to convert the user's balance to any local currency that they are interested in.

The program handles errors raised during input of amounts, KeyErrors and RequestErrors during fetching information from the API.
