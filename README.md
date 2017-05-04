# Penalty Counter
---------
Originally written by Roy Gero in Python 2.7.10
Currently version is in Python 3.6

## Purpose of the Program
Every NHL season there are 1,230 games played between the 30 teams. In each one of these games, there can be any number of penalties called. I want to provide people with the ability to make more informed statements when it comes to penalties that occur. The way that this program performs this is by parsing through the NHL website's game data and gathering all the penalties that occur. After gathering the information, the script hands the data to a SQLite Database. This website, [The Penalty Tracker](http://roymond.net/penaltytracker) displays this data to the user in a sortable manner.

## Description of Files
There are really four main files of the project.
* PenaltyTracker.py - This is the main file. It will handle getting the list of games on a specific date, parsing through them for the penalty data, generating the HTML, uploading to parse, and uploading the file to my website.
* Penalty.py - This is the file that defines the Penalty objects used in the PenaltyTracker. I wanted to create my own data structure for this project and it made sense to separate it out into its own file.
* Tester.py - This file is where all the unit tests live. Right now it tests the PenaltyTracker.py and the Penalty.py files.
* DataChecker.py - This file lives in the DataChecker folder. It is used to quickly compare the data generated by the NHL's website and the data contained on my website.
* DatabaseManager.py - This file handles everything involving the Database. The reason I did this was to make it so I could change the database implementation completely without having to dig through all the other files.

## File needed to run the script
In order to run the script, you need to define a file called "credientials.py". This file contains the FTP address, user name, password as well as the API keys for Parse. I've added it to the gitignore so I didn't inadvertently post it on the internet.

## Future Considerations for this project
With the offseason quickly approaching, I am currently investigating several enhancements that I will be making to this. Here are a brief couple.
* I'd also like to display more information. I've had several people request data be added to the website.

## Things learned through this project
* unittest module - One of the skill I wanted to strengthen was the ability to think through and use automated tests to insure that changes made to algorithms or functions didn't change the overall result.
* The SQLite3 Module - I use this to store data for the 2016-17 season.

## Deprecated Modules that I used in previous versions
* Parse's python module
* The FTP module
