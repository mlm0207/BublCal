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

# Monthly view
def monthly(request):
        
    # Make sure a user is logged in
    result = bublcal_lib.verifyLogin(request);

    if(not result[0]):
        return redirect("index");
    
    htcal = HTMLCalendar().formatmonth(current_date.year, current_date.month)

    return render(request, "monthly.html", {
        "loggedIn"  : True,
        "htcal": htcal,
        "month_year": month_year,
    })

# Weekly view
def weekly(request):
        
    # Make sure a user is logged in
    result = bublcal_lib.verifyLogin(request);

    if(not result[0]):
        return redirect("index");
    
    user = result[1];

    # Grab the users bubls
    bubls = bublcal_lib.getUserBubbles(user);

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
        "loggedIn"  : True,
        "bubls": bubls,
        "day_of_week": day_of_week,
        "day": suffix(day),
        "month_year": month_year,
        "days": days,
    })

# Create a bubble
def createBubl(request):
    # Make sure user is logged in
    result = bublcal_lib.verifyLogin(request);

    if(not result[0]):
        return redirect("index");
    
    user = result[1];

    # If data is being submitted
    if(request.method == "POST"):

        # Grab bubble data
        name    = request.POST["name"];
        note    = request.POST["note"];
        date    = request.POST["date"];
        time    = request.POST["time"];
        length  = request.POST["length"];

        result = bublcal_lib.createBubble(user, name, note, date, time, length);

        if(result[0]):
            return redirect("glance-view");
        else:
            return render(request, "bubl_create.html");
            
    return render(request, "bubl_create.html");

# Logout a user
def logout(request):
    # Make sure user is logged in
    result = bublcal_lib.verifyLogin(request);

    if(not result[0]):
        return redirect("index");

    bublcal_lib.logoutUser(request);

    return render(request, "logged_out.html");

# Delete a bubble
def deleteBubl(request, id):
    # Make sure a user is logged in
    result = bublcal_lib.verifyLogin(request);
    
    if(not result[0]):
        return redirect("index");
    
    user = result[1];
    bubl = bublcal_lib.getBubbleObject(id);

    # Make sure bubble exists
    if(bubl == None):
        return redirect("glance-view");

    # Make sure user owns bubble
    if(bubl.email.email != user):
        return redirect("glance-view");
    
    bublcal_lib.deleteBubble(request, id);

    return redirect("glance-view");

# Modify a bubble
def modifyBubl(request, id):
    # Make sure a user is logged in
    result = bublcal_lib.verifyLogin(request);
    
    if(not result[0]):
        return redirect("index");
    
    user = result[1];
    bubl = bublcal_lib.getBubbleObject(id);

    # Make sure bubble exists
    if(bubl == None):
        return redirect("glance-view");

    # Make sure user owns bubble
    if(bubl.email.email != user):
        return redirect("glance-view");

    # Make sure user is not updating info
    if(request.method == "POST"):
        bubl.name = request.POST["name"];
        bubl.note = request.POST["note"];
        bubl.date = request.POST["date"];
        bubl.time = request.POST["time"];
        bubl.length = request.POST["length"];

        bubl.save();

        return redirect("glance-view");

    else: # If first time viewing

        # Get correct format
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

        return render(request, "bubl_modify.html", args);

# Daily/"At a glance" view
def glance(request):
    
    # Make sure a user is logged in
    result = bublcal_lib.verifyLogin(request);

    if(not result[0]):
        return redirect("index");
    
    user = result[1];

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
    bubls = bublcal_lib.getUserBubbles(user);

    # Todays bubbles
    todaysBubls = [];

    # Number of tasks for tomorrow and overmorrow
    tomorrowTasks = 0;
    overmorrowTasks = 0;

    # Go through users bubls to check what to do to them
    if(bubls != None):
        for bubl in bubls:

            # Get the day the bubl lands on
            day = bubl.date.day;

            # Check if the tasks lands tomorrow
            if(day == tomorrow.day):
                tomorrowTasks += 1;

            # Check if the tasks lands overmorrow
            if(day == overmorrow.day):
                overmorrowTasks += 1;

            # Add bubbls that do fall under the active day
            if(day == today.day):
                todaysBubls.append(bubl);

    todayTime = datetime.datetime.today();

    # Create the rest of the timeslots for the array
    for i in range(currentHour + 1, 24):
        newT = todayTime;
        newT = newT.replace(hour=i, minute=0);
        timeSlots.append([i, newT.strftime("%I:%M %p")]);

    # Arguments to pass
    args = {
                "loggedIn"  : True,
                "today"     : today,
                "tomorrow"  : tomorrow,
                "overmorrow": overmorrow,
                
                "today_name"        : todayName,
                "tomorrow_name"     : tomorrowName,
                "overmorrow_name"   : overmorrowName,

                "timeSlots" : timeSlots,
                "bubls" : todaysBubls,
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
    result = bublcal_lib.verifyLogin(request);

    # Make sure user is not logged in
    if(result[0]):
        return redirect("glance-view");

    # If user submitted username/password
    if(request.method == "POST"):
        email    = request.POST["mail"];
        password = request.POST["password"];

        # Check if username & password are valid
        loginCheck = bublcal_lib.userLoginCheck(email, password);

        if(loginCheck[0]):

            # Save the session
            bublcal_lib.loginUser(request, email);

            return redirect("glance-view");
        else:
            args = { "siFailType": loginCheck[1] };

            return render(request, "login.html", args);

    # Default render page
    return render(request, "login.html");

# Signup Page
def signup(request):
    result = bublcal_lib.verifyLogin(request);

    # Make user a user is not logged in
    if(result[0]):
        return redirect("glance-view");

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