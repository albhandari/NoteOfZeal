Repo: https://github.com/JosephGerani/NotesOfZeal
 
# Use Case Description
Date: 9/15/2021
## Product Name: NotesOfZeal
## Contributors: 

James Cai: https://github.com/jcai5

Joseph Gerani: https://github.com/JosephGerani

Richard Nguyen: https://github.com/richardnguyen734

Alex Bhandari: https://github.com/albhandari

### Problem Statement: The number one issue for students with studying is that students often procrastinate. To help fix the issue, we will develop an app that will help students study in three different ways. These three methods are memorizing, taking good notes, and managing their time efficiently. 
### Non-functional Requirements: The source code should be compatible in cross-platform use. No Operating System specific system calls should be used. It should not take more than a few seconds (preferably less than 3 seconds) to start the program. The program should be preferably compiled, not interpreted (plan to write in compiled language, to avoid the natural slowness of languages such as Python and not require an external program to be executed).
 
## Create account.
### Summary
Ability for users to sign-up, login/logout. That’s all there is to it. No email is required. Just make a username and password so that multiple users can use the same program and files will not overlap. 
## Actors
All the students, instructors, and studious people running this program. It’s a bare minimum to use the rest of this program (each person makes their own account in order to use it).
 
## Preconditions
No preconditions. This *is* the precondition to use the rest of the program’s features.
## Triggers
Customer types in new account credentials. Customer logins to an existing account by typing in his credentials.
## Primary Sequence
Click on “create account”


Login with new account


Now from every point that user wants to use the program, they just login.


## Primary Postconditions
They login to their account.
OR
They have an account created.
 
## Be able to delete account
## Summary
A customer created an account to try the app, but wants to delete their account due to privacy issues or lost interest in the app. 
## Actors
Students
Instructors
## Preconditions
* Have an account and be logged in
## Triggers
Students select the option “delete account”. 
## Primary Sequence
Student logs into their account
Student clicks on their account information and selects the delete account option
Student types some type of confirmation to delete account
## Primary Postconditions
* Student no longer has an account
 
## Input a markdown file and output flash cards
 Summary
The user wants to create flash cards out of a markdown file.
## Actors
The user.
## Preconditions
* The user has logged in.
* A markdown file.
## Triggers
The user selects “create flashcards using markdown file”
## Primary Sequence
System asks the user to upload a markdown file.
User uploads a markdown file.
The system checks if the markdown file is in the correct format.
System creates flashcards from the markdown file.
## Primary Postconditions
* The user gets flashcards from the markdown file.
## Alternate Sequences
* The user’s markdown file is not formatted correctly.
* The system displays an error.
## Sharing the flash cards
## Summary
Students want to share their notes to friends or classmates that missed the class. 
## Actors
Students
## Preconditions
* Have an account 
* Have the notes ready to be exported or shared 
## Triggers
Student saves the notes and converts it to a specific file type like pdf or doc. 
## Primary Sequence
Student logs on to their account
Student selects the file where they saved their notes
Student selects the option “save as” 
Students email it to their friend, or get it through a flash drive.
## Primary Postconditions
* User should have an account and be signed in
* The friend should have an account.
* The friend receives the students notes. 
## Alternate Sequences
Student logs on to their account
Student selects the file where they saved their notes
Student selects the share option
Students input their friends' username/email and share it to them.
### Alternate Trigger
Click share button 
### Alternate Postconditions
Friend now has the notes
## Render Markdown Notes
## Summary
Take the notes from markdown
## Actors
Programmers mainly
## Preconditions
Be logged in
Have markdown files to manipulate in the first place
## Triggers
Allow the user to display, view, and edit markdown files.
## Primary Sequence
step 1 action
step 2 action
etc
## Primary Postconditions
The user has an edited markdown file filled with whatever pictures and bold text he wants.
## Convert markdown notes to pdf
## Summary
Allow the user to convert a markdown file to a pdf file.
## Actors
The user
## Preconditions
* User should have an account and be signed in
* The user has a markdown file.
## Triggers
User clicks on “Convert markdown notes file to pdf.”
## Primary Sequence
The system asks the user to upload a markdown file.
User uploads markdown file.
The system converts the markdown file to a pdf
The user receives a pdf file.
## Primary Postconditions
* The customer receives a pdf file.
 
## Create time blocks (using markdown)
## Summary
Allow the user to input times and get a markdown file with time blocks.
write summary here
## Actors
The user.
## Preconditions
* User should have an account and be signed in
* User has specific time periods to input.
## Triggers
User clicks on “Create time blocks with times”
## Primary Sequence
The system asks the user to input times to make as blocks.
The user enters times.
The system creates time blocks in a markdown file
The user receives the markdown file.
## Primary Postconditions
* User receives a markdown file with time blocks.
## Alternate Sequences
* User enters invalid times.
* System gives an error message to the user.
* User inputs correct times.
## Use pomodoro timer.
## Summary
Student uses the app to setup a pomodoro timer to help students study in certain time intervals and take breaks in certain time intervals
## Actors
Students
## Preconditions
* User should have an account and be signed in
* User is either looking at notes or doing exercises. 
* User knows how long the intervals for studying and taking breaks are
## Triggers
The trigger is when the student selects how long they study for and selects the timer for how long the break is going to be. 
## Primary Sequence
Student goes on to the app and goes on their notes or exercises
Student clicks on the timer button
Student selects the pomodoro option
Student selects how long their breaks and study sessions are
Study selects start timer
## Primary Postconditions
* User has a timer that will effectively ring when the study session is over/start the break session and when the break session is over, the study session starts
 
## Change order of flash cards based on how often user got answer correct
## Summary
Allows user to change the order of their flash cards based on which ones they got correct. Puts the ones they missed in front.
## Actors
The User.
## Preconditions
* User should have an account and be signed in
* The user must have a set of flash cards.
* The user must have studied the flash cards at least once.
* The user must be viewing the flash cards
## Triggers
User clicks the sort flash cards button. 
## Primary Sequence
User clicks the sort flash cards button 
The system sorts the flash cards by what they got correct and incorrect.
## Primary Postconditions
* The user has a set of flash cards sorted in order of most missed to least missed.
## Create pdf of flash cards to print
## Summary
Students will be able to create a pdf of their flash cards so that they can print out the flash cards and be able to cut them out and study them 
## Actors
Students
## Preconditions
* Student has an account
* Student has to have a file of flash cards ready to print
## Triggers
The trigger is when the student selects the print option when having the file opened
## Primary Sequence
Student selects the file of the flash cards that they want to open
Student selects the print option in the top
Student selects what printer and then presses print
## Primary Postconditions
* Student will have a sheet of flash cards ready to be cut and to study from
## Find text in files
## Summary
Users will be able to find specific lines of text/files through a find/search option      
## Actors
Students
Instructors
## Preconditions
* Users must have files in their directory/account already.
 
## Triggers
User goes to their files and clicks on the search bar and types what files/text they are looking for
## Primary Sequence
Users click on their files tab
User clicks the search bar in the top
User types in what file name they are looking for
## Primary Postconditions
* User should have an account and be signed in
* Users are now able to find specific files that they were looking for
## Alternate Sequences
* Step 1 If file was recently viewed, user will be able to select it from the recently viewed section
### Alternate Trigger
* Users clicked on the file that they wanted from the recently viewed section 
### Alternate Postconditions
* Users have accessed their file from the home page.
## Track hours worked per day
## Summary
Students will be able to track the amount of hours worked during that session and will be able to check the amount of hours studied per week/month. 
## Actors
Students
Teachers
## Preconditions
* Student must have an account
## Triggers
User checks the statistics of their account
## Primary Sequence
User logs on to their account
Student clicks on “User statistics”
User selects the time option and is able to see how long their current session is or how long they have spent on the app over the week. 
## Primary Postconditions
* Users will be able to see how long they have spent on the app over the past day or past week.
## Visualize hours worked and projects
## Summary
Bar graphs will be drawn that visually display how much time the user spent working each day of the week, month, year (or whatever time frame the user requests). The bar graphs are drawn based off information stored on the computer by the program that holds all the times the user was working.
## Actors
Students
Instructors
 
## Preconditions
* Precondition 1: Have an account and be signed into it.
* Precondition 2: Have hours logged in the first place. If the user wasn’t logging in his hours, he can’t have this information because it hasn’t been saved.
## Triggers
The user clicks on a button for visualizing (maybe the button is in a menu), and then they click another button 
## Primary Sequence
User logs into account
User clicks a few buttons adjusting for the time frame (one week, a few days, etc.) 
## Primary Postconditions
* Bar graphs displayed to screen
 
## Add todo tracker
## Summary
A to-do interface (like a checklist )where the user inputs all the necessary things that they need to accomplish. As they progress and complete the things that they input, they can check it off. 
## Actors
Students
Instructors
## Preconditions
* Have an account and account and be signed in so each item in the to-do list can be saved to a specific user.
## Triggers
User has to click on the to-do button to open the Interface where the user then has to input a list of items they want to complete. Next to get rid of the items that the user completed, they would have to click on the check-box which would remove the completed item from the list. 
## Primary Sequence
When clicked on the To-Do feature, an interface opens.
In the interface a input system is visible where the user can input a series of items with a check-box beside it.
When a user Check’s off items that are fulfilled, the item gets removed from the list.
## Primary Postconditions
* Each time they input the item that is required to be done, it is displayed visually with a checkbox.
* Every time they click the checkbox, that specific item gets removed from the list both internally and visually.
 
## Visualize timeblocks (similar to day view on google calendar)
## Summary
Users will be able to see their planned out schedules in a calendar type format and will be able to see what is planned for the week. (kind of like what Canvas has currently). 
## Actors
Students
Instructors
## Preconditions
* Users need to have an account
* Users need to have things on their to-do list/ have assignments that are due in the future/planned study sessions
## Triggers
When students create items that they want to finish for their to-do list, they will select what date and time they would like to have the assignment be done by.
## Primary Sequence
Students clicks on the calendar view button
Students are able to see what they have for that month.
Students can click under specific objectives to see a description and what is due
## Primary Postconditions
* Students now have a working calendar that will tell them when things are due and when they have set their times for study sessions. 
 
## Add ability to navigate between notes using this syntax [[this other note]].
## Summary
Students can create links to other notes using the syntax [[this other note]] in their other notes.
## Actors
Students
## Preconditions
* another note file that will be linked to
## Triggers
The user writes the syntax [[this other note]] in their note file. 
## Primary Sequence
User is in their original note file 
User writes [[this other note]] in their note file
Use can click on [[this other note]] to move to the “this other note” file.
## Primary Postconditions
* User should have an account and be signed in
* User is on the linked note file.
## Alternate Sequences
* User puts [[this other note]] in their notes but “this other note” does not exist
* [[this other note]] will stay as normal text instead of becoming a link.
 
## Create HTML of flash cards (for sake of adding to custom website or webpage/blogpost)
## Summary
The user can choose to convert their flash cards into HTML.
## Actors
Student
## Preconditions
* User has a set of flash cards.
## Triggers
User clicks on the “convert to flash cards to HTML” button while on a set of flashcards
## Primary Sequence
The system converts the flashcards to HTML
The user gets HTML of their flashcards
## Primary Postconditions
* User now has HTML of their chosen flashcards
## Convert markdown to HTML
## Summary
Allow users to change their markdown files to HTML files.
## Actors
Student
## Preconditions
* User should have an account and be signed in
* User must have a markdown file to convert
## Triggers
User will click on “convert markdown file to HTML”.
## Primary Sequence
User uploads their markdown file.
The system changes the markdown file to and HTML file
The system returns the HTML file.
## Primary Postconditions
* The user now has an HTML file.
## Syntax highlighting (In context of programming related notes)
## Summary
The user is either writing source code or writing notes that contains source code. However the user doesn’t want all the text to be shown as plain-text. The user wants to see for example, data types be highlighted as a different color than function names.
## Actors
Students
Instructors
## Preconditions
* User should have an account and be signed in
## Triggers
The user opens a new file by clicking on a button that says “new file” and specifies the file extension to save as so that the program automatically knows what language he’s working with. Alternatively of course, the user can open a file that has that extension OR click on a button that tells the program to view a file as a source file of a specific language.
## Primary Sequence
User opens his new file or existing file.
Program informs the user that he’s viewing it with syntax highlighting of a certain language (say Python)
## Primary Postconditions
The source code that the user is typing and has been typed will stay highlighted.
* etc
## Alternate Sequence
User opens an existing file that doesn’t have an extension such as .py and wants to view it as source code .
User clicks on a button that tells the program to view it as a certain source code.
Syntax is displayed.
 
### Alternate Trigger
User has to inform program through a series of button presses to view it as source code.
### Alternate Postconditions 
 
The source code that the user is typing and has been typed will stay highlighted.
