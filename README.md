# Adapt website
a website for Adapt which is a youth lead civil work community for teenagers from 13 to 18 in Egypt
## main pages
This project contains many pages including
### 1- main page
this page contains the about, contact, committee description and much more that make you understand what Adapt is, its design is inspired by the main page for hackclub
### 2- events page
this page contains all the events that we did and you can filter them by location, time, tags or just filter by name or description of the event from a real database connected to an api that will be explained down later
### 3- login/register page
these are the sign in and sign up for this website, it includes a database of users and admins, if you want to login as a user try just sign up for being an admin you can login using this account

username: ziad_elhusiny

password: 12345678

this account is a temporary admin so it will be removed once the testing is finished

### 4- dashboard
this page is a dashboard that contains the users tasks according to his committee and his committee news that automatically remove themselves when their end date comes
#### admin dashboard:
this is a part of the dashboard only visible to admins

it contains parts to add or remove tasks and news

## technology used
used a navbar for better navigation in the website in all pages
### events page
in the events page I used python to make an API using FastAPI that uses SQLite3 and has databases for the events as the back end, I also used JS as the front end and added the filtering system using it
### login/register pages
in these pages i used python to make the API and connected it to SQLite3 database, I also used jwt tokens for logging out automatically after 30 minutes like other platforms, I also made a verification system for these jwt tokens and before every request these jwt tokens are requested from local storage
### dashboard
in the dashboard i used the same api for the login/register and put new tables that contain the news and tasks and every user finished tasks and added endpoints for adding and removing news and tasks as an admin

every post and patch request also use api keys that are stored in the database

the example for everyone to try is "1"

## features
the front end is made using HTML, CSS, vanilla JS, I also used google fonts and font awesome icons and deployed on github on this link

https://zezo386.github.io/events-api/

the back end is made using python FastAPI, SQLite3, JWT and deployed on railway on this link

https://events-api-production-4a05.up.railway.app/docs#/
## setup
Clone the repository
    bash

    git clone <https://github.com/zezo386/events-api>
    cd adapt

# Contributes

Made by Ziad Elhusiny the GOAT of programming
