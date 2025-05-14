# PPE Management System
This Python project is an assignment for the Python programming module in semester 3 of my diploma program at APU. Although being a very basic command-line program with no graphical user interface, it has served a crucial purpose of strengthening my understanding of programming concepts and fundamentals. 

Note: This repository is only intended solely for academic reference and personal learning. It should not be reused or resubmitted as original work under any circumstance. Unauthorized reproduction or misuse is strictly discouraged.


## Project Assumptions (And How It Works)

### A. Controller/Administrator Registration 
1. User is required to conduct controller (administrator) registration during its first launch (assuming an empty system). Four controllers are required to complete the registration and move on to the next task. Therefore, the system will prompt the user for a set of administrator username and password for four times.
2. Username input by user cannot be the same with other existing usernames.
3. The credentials (username and password) of the registered controllers are then saved in a file named “controller.txt”.


### B. Initial Inventory Creation
After administrator registration is completed, user proceeds to the initial inventory creation phase. Our inventory management system has a total of five text files that users will have to create and insert values. Those files are categorized as either mandatory or optional to be filled up during this phase.

**Mandatory**
  - ppe.txt
  - hospitals.txt
  - supplier.txt
**Optional**
  - distribution.txt
  - supply.txt

1. ppe.txt consists of four attributes:
  - Item code (primary key)
  - Item name
  - Current quantity
  - Supplier code
A minimum of six items (according to assignment’s requirement) alongside their attributes must be filled into ppe.txt to be considered setup complete for the file. The item name is unique and cannot repeat.

2. hospital.txt consists of two attributes:
  - Hospital code (primary key)
  - Hospital name
A minimum of four unique hospitals alongside their attributes are required to be filled up by user initially into hospital.txt to be considered setup complete for the file. The hospital name is unique and cannot repeat.

3. supplier.txt consists of three attributes:
  - Supplier code (primary key)
  - Supplier name
A minimum of four unique suppliers alongside their attributes are required to be filled up by user initially into supplier.txt to be considered setup complete for the file. The supplier’s name is unique and cannot repeat.

4. distribution.txt consists of seven attributes:
  - Distribution code (primary key)
  - Item code
  - Hospital code
  - Distribution year
  - Distribution month
  - Distribution day
  - Distribution quantity
As mentioned, user can choose to either enter data into distribution.txt or skip it during initial inventory creation.

5. supply.txt consists of seven attributes:
 - Supply code (primary key)
 - Item code
 - Supplier code
 - Supply year
 - Supply month
 - Supply day
 - Supply quantity
As mentioned, user can choose to either enter data into supply.txt or skip it during initial inventory creation.


### C. System Booting
1. With the assumptions from section A and B, the main system will only be launched with the following conditions:
  - controller.txt must exist and not empty.
  - A total of only four controllers are registered in the system and saved in controller.txt.
  - The three mandatory text files mentioned must exist, not empty, and complete with data according to minimum content requirements.

2. Once the conditions above are fulfilled, main system will be booted.

3. This process of checking files will be carried out every time the programme is run to ensure that these internal files are valid and operatable.


## D. Login System
As soon as the system boots successfully, user can start logging in to the system.

1. According to the four controller credentials previously registered and saved in controller.txt, user has to correctly input the username and its corresponding password in order to log in to the system successfully. A validation process will be carried out to confirm the user’s validity to enter the system.

2. User only has three tries to log in to the system. If user fails to log in after three attempts, the program's run session will be instantly terminated, ultimately stopping the user from logging in.

3. A technical detail to be noted is that both username and password will be validated together at once by comparing to controller.txt after inputting.


## E. Inventory Tracking and Searching Functionality
1. At the start of the main system, each file’s content are separated into a group

2. A successful login grants the user access to the inventory management system's main functionalities.

3. In our system's tracking functionality, user access desired information on any file by inputting data value of a chosen field (attribute).

4. The record(s) associated with the data value will be displayed accordingly.


## F. Inventory Update Functionality
1. In this section, user is able to choose between adding, changing, or removing data from text files in the system.

2. User is able to add new data into all of the five existing text files.

3. User is able to change data in all of the five existing text files, except for the primary key attribute (code) of each text file. If the data being changed can be found elsewhere, that data across the system will also be updated accordingly.

4. User is able to remove a single record (a row of data) by pin-pointing the location of the record using the primary key of the record. This functionality is only available for distribution.txt and supply.txt text file.

5. Once user finish updating the data, the updated record will be saved and displayed to the user.


## G. Report Functionality
1. Our system comprises three types of general reports to be printed out:
  i) PPE Distribution Report
  ii) PPE Supply Report
  iii) Overall Transaction Report (month specific)

2. PPE Supply Report displays list of suppliers with the supply quantity for the PPE they supply.
  • File source: supplier.txt, ppe.txt and supply.txt.

3. PPE Distribution Report displays list of hospitals with the distribution quantity for every type of PPE.
  • File source: hospital.txt, ppe.txt, distribution.txt.

4. Overall Transaction Report displays all distribution and supply transactions made within a specified month, which are then arranged according to the ascending order of the transaction date.
  • File source: distribution.txt, supply.txt.

5. These reports serve as a summary or overview of the PPE inventory flow to ensure efficient monitoring and management of the inventory system.
