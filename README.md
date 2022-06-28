# Python-Flight-Tracker

Group Project
Flight Tracker with Python: Flightradar24 Edelweiss Tracker

Assignment Overview

We developed a Python program to process web data and extract meaningful information from it. In particular, our program downloads data from flightradar24.com, creates a data frame and performs few actions on it. 

Assignment Background

Planes are now a widespread means of transportation all over the world. Flying has become essential even in daily life for many people, thus it is not surprising that up to date information about flights and airlines are extremely necessary. 
Flightradar24 is a Swedish website providing real-time aircraft flight tracking information, including date and time, departure and arrival, flight number, flight time, type of aircraft, current status, altitude, headings and speeds. 
In this project, we focus on data for Edelweiss Airline, based in Zurich. 

Assignment Specifications

Our program first of all creates a data frame based on flightradar24 data for Edelweiss. This data frame includes: 
-	Date
-	Departure
-	Arrival
-	Flight number
-	Flight time
-	Scheduled Time Departure (STD)
-	Actual Time Departure (ATD)
-	Scheduled Time Arrival (STA)
-	Current Status
for each aircraft of Edelweiss fleet (HB-IHX, HB-IHY, HB-IHZ, HB-IJU, HB-IJV, HB-IJW, HB-JJK, HB-JJL, HB-JJM, HB-JJN, HB-JMD, HB-JME, HB-JMG). 

After this, the program asks the user what function he/she would like to perform among 2 different functions: 
1.	Displaying the average delay of Edelweiss aircrafts during last week
2.	Finding a flight connection between two places

The code then prints out the results.
