# Imports
import calendar
import datetime
import re
from django.shortcuts import render
from calendar import HTMLCalendar
from django.db import models
from app.models import UserData
from django.http import HttpResponseRedirect
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


# Daily/"At a glance" view
def daily(request):
    today       = datetime.date.today();
    tomorrow    = datetime.date.today() + datetime.timedelta(1);
    overmorrow  = datetime.date.today() + datetime.timedelta(2);
    
    todayName      = DAY_NAMES[today.weekday()][0];
    tomorrowName   = DAY_NAMES[tomorrow.weekday()][1];
    overmorrowName = DAY_NAMES[overmorrow.weekday()][1];

    args = {
                "today"     : today,
                "tomorrow"  : tomorrow,
                "overmorrow": overmorrow,
                
                "today_name"        : todayName,
                "tomorrow_name"     : tomorrowName,
                "overmorrow_name"   : overmorrowName,
            };

    return render(request, "glance.html", args);

# Main Page View
def index(request):
    args = {};

    return render(request, "index.html", args);

# Login page
def login(request):
    # If user submitted username/password
    if(request.method == "POST"):
        email    = request.POST["mail"];
        password = request.POST["password"];

        # Verification flags
        emailValid  = False;
        passValid   = False;

        # Check if username & password are valid
        for user in UserData.objects.all():
            if(user.email == email):
                emailValid = True;
                if(user.password == password):
                    passValid = True;
                    break;
        
        # Verification output
        args = {    "emailValid":   emailValid,
                    "passValid":    passValid   };

        # If authed then go to user home page
        if(emailValid and passValid):
            return render(request, "glance.html", args);
        else: # Show invalid username/password error
            return render(request, "login.html", args);

    # Default render page
    return render(request, "login.html");

def signup_success(request):
    firstName   = request.POST["firstName"];
    lastName    = request.POST["lastName"];
    birthday    = request.POST["birthday"];
    mail        = request.POST["mail"];
    password    = request.POST["password"];

    mailSplit = str(mail).split('@', 1);

    userData = UserData(email=mail, first_name=firstName, last_name=lastName, dob=birthday, user_name=mailSplit[0], password=password);
    userData.save();
    
    args = {};

    return render(request, "signup_success.html", args);


# Signup Page
def signup(request):
    if(request.method == "POST"):
        firstName   = request.POST["firstName"];
        lastName    = request.POST["lastName"];
        birthday    = request.POST["birthday"];
        mail        = request.POST["mail"];
        password    = request.POST["password"];
        
        mailSplit = str(mail).split('@', 1);

        # Check if user is 13 or older
        userBirth = datetime.datetime.strptime(birthday, "%Y-%m-%d").date();
        activeDay = datetime.date.today();

        userAge = (activeDay - userBirth).days / 365.25;

        # Regex for valid email
        emailReg = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)";

        # Check if email is in use
        emailNotUsed = True;
        for user in UserData.objects.all():
            if(user.email == mail):
                emailNotUsed = False;
                break;

        # account creation flags
        oldEnough = (userAge >= 13);
        validEmail = emailNotUsed and re.search(emailReg, mail);

        if(oldEnough and validEmail):
            userData = UserData(email=mail, first_name=firstName, last_name=lastName, dob=birthday, user_name=mailSplit[0], password=password);
            userData.save();

            args = {};

            return render(request, "signup_success.html", args);
        else:
            
            args = { "ageFail": oldEnough, "emailFail": validEmail };

            return render(request, "signup.html", args);

    args = {};

    return render(request, "signup.html", args);