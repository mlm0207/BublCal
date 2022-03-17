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
        name    = request.POST["name"];
        note    = request.POST["note"];
        date    = request.POST["datetime"];
        length  = request.POST["length"];

        result = bublcal_lib.createBubble(email, name, note, date, length);

        if(result[0]):
            return render(request, "bubl_create.html");
        else:
            return render(request, "bubl_create.html");
            
    return render(request, "bubl_create.html");

# Daily/"At a glance" view
def daily(request):

    # Grab active day
    today       = datetime.date.today();
    tomorrow    = datetime.date.today() + datetime.timedelta(1);
    overmorrow  = datetime.date.today() + datetime.timedelta(2);
    
    # Grab active days names
    todayName      = DAY_NAMES[today.weekday()][0];
    tomorrowName   = DAY_NAMES[tomorrow.weekday()][1];
    overmorrowName = DAY_NAMES[overmorrow.weekday()][1];

    currentTime = datetime.datetime.today().time()
    currentHour = currentTime.hour;

    timeSlots = [[currentHour, currentTime.replace(minute=0).strftime("%I:%M %p")]];
    
    bubls = bublcal_lib.getUserBubbles(bublcal_lib.getLoggedUser(request));

    for bubl in bubls:
        print("\n\n", bubl.date, "\n\n");

    for i in range(currentHour, 24):
        newT = datetime.datetime.today() + datetime.timedelta(hours=i - 1);
        newT = newT.replace(minute=0);
        timeSlots.append([newT.hour, newT.strftime("%I:%M %p")]);

    args = {
                "today"     : today,
                "tomorrow"  : tomorrow,
                "overmorrow": overmorrow,
                
                "today_name"        : todayName,
                "tomorrow_name"     : tomorrowName,
                "overmorrow_name"   : overmorrowName,

                "timeSlots" : timeSlots,
                "bubls" : bubls,
            };

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

                return render(request, "glance.html");
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