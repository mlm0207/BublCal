# Imports
import calendar
import datetime
from os import times
from . import bublcal_lib
from django.shortcuts import render
from calendar import HTMLCalendar
from django.db import models
from app.models import UserData
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django import forms

# Names of the days
DAY_NAMES = [
                [ "Monday",     "Mon" ], 
                [ "Tuesday",    "Tue" ], 
                [ "Wednesday",  "Wed" ], 
                [ "Thursday",   "Thu" ], 
                [ "Friday",     "Fri" ], 
                [ "Saturday",   "Sat" ], 
                [ "Sunday",     "Sun" ], 
            ];

current_date = datetime.date.today()
year, week_num, day_of_week = current_date.isocalendar()
month_year = current_date.strftime("%B") + " " + str(year)
day_of_week = calendar.day_name[day_of_week - 1]


def main(request):
    htcal = HTMLCalendar().formatmonth(current_date.year, current_date.month)

    return render(request, "main.html", {
        "htcal": htcal,
        "month_year": month_year,
    })

def weekly(request):
    day = current_date.day
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat","Sun" ]

    weeks_list = []
    for weeks in calendar.monthcalendar(year, current_date.month):
        weeks_list.append(weeks)

    dates = []
    for w in weeks_list:
        if day in w:
            for date in w:
                dates.append(date)

    days = dict(zip(day_names, dates))

    # add suffix to date
    def suffix(day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            day = str(day) + "th"
        elif day == 1 or day == 21 or day == 31:
            day = str(day) + "st"
        elif day == 2 or day == 22:
            day = str(day) + "nd"
        elif day == 3 or day == 23:
            day = str(day) + "rd"
        return day

    return render(request, "weekly.html", {
        "day_of_week": day_of_week,
        "day": suffix(day),
        "month_year": month_year,
        "days": days,
    })

def createBubl(request):
    if(request.method == "POST"):

        # Grab user data
        email   = bublcal_lib.getLoggedUser(request);
        
        print(request.POST);

        name    = request.POST["name"];
        note    = request.POST["note"];
        date    = request.POST["date"];
        time    = request.POST["time"];
        length  = request.POST["length"];

        result = bublcal_lib.createBubble(email, name, note, date, time, length);

        if(result[0]):
            return render(request, "bubl_create.html");
        else:
            return render(request, "bubl_create.html");
            
    return render(request, "bubl_create.html");

def logout(request):
    if(bublcal_lib.checkUserLogged(request)):
        user = bublcal_lib.getLoggedUser(request);
        request.session["loggedIn"] = False;

    return redirect("index");

def deleteBubl(request, id):
    bublcal_lib.deleteBubble(request, id);
    return redirect("daily-view");

def modifyBubl(request, id):

    if(request.method == "POST"):

        name    = request.POST["name"];
        note    = request.POST["note"];
        date    = request.POST["date"];
        time    = request.POST["time"];
        length  = request.POST["length"];

        bubl = bublcal_lib.getBubbleById(id);

        bubl.name = request.POST["name"];
        bubl.note = request.POST["note"];
        bubl.date = request.POST["date"];
        bubl.time = request.POST["time"];
        bubl.length = request.POST["length"];

        bubl.save();

        return render(request, "modify_bubl.html");

    else:
        bubl = bublcal_lib.getBubbleById(id);

        bDate = str(bubl.date.year) + '-' + str(bubl.date.month).zfill(2) + '-' + str(bubl.date.day).zfill(2);
        bTime = str(bubl.time.hour).zfill(2) + ':' + str(bubl.time.minute).zfill(2) + ":00";

        args = {
                    "bName": bubl.name,
                    "bNote": bubl.note,
                    "bDate": bDate,
                    "bTime": bTime,
                    "bLength": bubl.length,
                    "bID":  bubl.id,
                };

        print(bublcal_lib.getBubbleById(id).date.month);

        return render(request, "modify_bubl.html", args);


# Daily/"At a glance" view
def daily(request):

    # Grab the active day and the two days after
    today       = datetime.date.today();
    tomorrow    = datetime.date.today() + datetime.timedelta(1);
    overmorrow  = datetime.date.today() + datetime.timedelta(2);
    
    # Grab the names for the days above
    todayName      = DAY_NAMES[today.weekday()][0];         # Long name
    tomorrowName   = DAY_NAMES[tomorrow.weekday()][1];      # Short name
    overmorrowName = DAY_NAMES[overmorrow.weekday()][1];    # Short name

    # Get current time
    currentTime = datetime.datetime.today().time();
    currentHour = currentTime.hour;

    # This array will hold the time slots for the current day up to 12:00PM
    # the array starts at the current hour the user is viewing the page
    # each array item holds two things, the hour in 24 base and the formatted time
    # i.e.  [4, "4:00 PM"]
    #       [20, "10:00 PM"]
    timeSlots = [[currentHour, currentTime.replace(minute=0).strftime("%I:%M %p")]];
    
    # Grab the users bubls
    bubls = bublcal_lib.getUserBubbles(bublcal_lib.getLoggedUser(request));

    # Number of tasks for tomorrow and overmorrow
    tomorrowTasks = 0;
    overmorrowTasks = 0;

    # Go through users bubls to check what to do to them
    if(bubls != None):
        for bubl in bubls:

            # Get the day the bubl lands on
            day = bubl.date.day;

            print("\n\n", bubl.id);

            # Check if the tasks lands tomorrow
            if(day == tomorrow.day):
                tomorrowTasks += 1;

            # Check if the tasks lands overmorrow
            if(day == overmorrow.day):
                overmorrowTasks += 1;

            # Remove bubbls that do not fall under the active day
            if(day != today.day):
                bubls.remove(bubl);

    todayTime = datetime.datetime.today();

    # Create the rest of the timeslots for the array
    for i in range(currentHour + 1, 24):
        newT = todayTime;
        newT = newT.replace(hour=i, minute=0);
        timeSlots.append([i, newT.strftime("%I:%M %p")]);

    # Check if user is logged in
    loggedIn = bublcal_lib.checkUserLogged(request);
    
    # Arguments to pass
    args = {
                "loggedIn"  : loggedIn,
                "today"     : today,
                "tomorrow"  : tomorrow,
                "overmorrow": overmorrow,
                
                "today_name"        : todayName,
                "tomorrow_name"     : tomorrowName,
                "overmorrow_name"   : overmorrowName,

                "timeSlots" : timeSlots,
                "bubls" : bubls,
                "tomorrowTasks" : range(tomorrowTasks),
                "overmorrowTasks" : range(overmorrowTasks),
            };

    # Render the page
    return render(request, "glance.html", args);

# Main Page View
def index(request):
    args = {};

    return render(request, "index.html", args);

# Login page
def login(request):

    # Make sure user is not logged in    
    if(bublcal_lib.checkUserLogged(request) == False):

        # If user submitted username/password
        if(request.method == "POST"):
            email    = request.POST["mail"];
            password = request.POST["password"];

            # Check if username & password are valid
            loginCheck = bublcal_lib.userLoginCheck(email, password);

            if(loginCheck[0]):

                # Save the session
                request.session["user"] = email;
                request.session["loggedIn"] = True;

                return redirect("daily-view");
            else:
                args = { "siFailType": loginCheck[1] };

                return render(request, "login.html", args);

        # Default render page
        return render(request, "login.html");

    else:
        return redirect("main"); # Redirect to home page if logged in

# Signup Page
def signup(request):

    # Make user a user is not logged in
    if(bublcal_lib.checkUserLogged(request) == False):
        # If user is submitting data
        if(request.method == "POST"):

            # Grab user data
            email       = request.POST["email"];
            password    = request.POST["password"];
            firstName   = request.POST["firstName"];
            lastName    = request.POST["lastName"];
            birthday    = request.POST["birthday"];

            # Try to create the user
            result = bublcal_lib.createuser(email, password, firstName, lastName, birthday);

            if(result[0]):
                return render(request, "signup_success.html"); # If success
            else:
                args = { "acFailType": result[1] };

                return render(request, "signup.html", args); # If fail

        return render(request, "signup.html");

    else:
        return redirect("main"); # Redirect to home page if logged in