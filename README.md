# Fomo_telebot
Telegram bot that would run in conjunction with the web application.

Find the Telegram bot on telegram by searching @NUS_Fomo_bot
Find the web application at 

## Background
This Telegram bot is created to compliment the web application by making
the process of finding events more convenient for its users. Since there
are already many existing channels on Telegram being used by NUS students.
We believe that Telegram would be the best channel to reach out to students.


## Features
This Telegram bot allows users to find events that have been created in 
the database using the website. They can query using 'category', 'date'
and venue. 

## Usage
To run the program, one simply has to install all the necessary packages 
that have already been conveniently placed in the requirements.txt file by
passing

'''bash
pip install -r requirements.txt
'''

After the necessary packages have been install. Simply run the file using 
python.

'''bash
python fomo.py
'''

## Explanation
fomo.py is the main script that contians all the functions that can be 
called in the Telegram bot. 

db_functions.py contains all the functions that are used to query in SQL. 

Event.py is the class created for the events.

format_event.py simply just contains the format in which events will be 
displayed to its users. 

## Support
For support you can contact the creator of the repository through direct 
messages

## Contributing
No direct contributions are welcomed for the project, but comments and 
criticism is accepted.

## Authors and acknowledgement
Angela Chen Zhiyao and Bobby Cai Rong are the main contributors to this 
project that is done for NUS Orbital.

## Project status
Complete  