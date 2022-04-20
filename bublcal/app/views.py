# Imports
import calendar
import datetime
import time
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

def profile(request):
    result = bublcal_lib.verifyLogin(request)
    if(not result[0]):
        return redirect("index")
    
    usermail = result[1];

    if(request.method == "POST"):
        for user in UserData.objects.all():
            if user.email == usermail:
                user.firstName = request.POST["fName"];
                user.lastName = request.POST["lName"];
                user.birthday = request.POST["birthDay"];
                user.email = request.POST["email"];
                user.save()
    
    return render(request, "profile.html")

#################################
# Monthly view
# 
# Displays a view of the month
# and allows for the users to view
# other months
#################################
def monthly(request, month, year):

    # Check if user is logged in
    result = bublcal_lib.verifyLogin(request);

    # Tell user the need to be signed in
    if(not result[0]):
        return render(request, "loggin_message.html");
    
    # Grab the user and update their bubls
    user = result[1];
    bublcal_lib.timeCheck(user);

    # Grab the users bubls
    bubls = bublcal_lib.getUserBubbles(user);

    # Grab and create the links for the previous and next months
    nextMonth = bublcal_lib.nextMonthDate(month, year);
    prevMonth = bublcal_lib.previousMonthDate(month, year);

    nextMonthLink = F"/app/monthly/{str(nextMonth[0])}/{str(nextMonth[1])}/";
    prevMonthLink = F"/app/monthly/{str(prevMonth[0])}/{str(prevMonth[1])}/";
    
    # Get the month weeks to be displayed
    weeks = bublcal_lib.getMonthWeeks(year, month);

    # Get month firstDay
    monthFirstDay = datetime.datetime(month=month, year=year, day=1);
    monthName = monthFirstDay.strftime("%B");

    # Get todays actual month and day for proper bubl filtering & month rendering
    today = datetime.datetime.now();

    # This months bubls
    monthBubls = [];

    for bubl in bubls:
        if(bubl.date.year == year and bubl.date.month == month):
            monthBubls.append(bubl);
    
    args =  {
                "loggedIn"      : True,
                "weeks"         : weeks,
                "month"         : month,
                "year"          : year,
                "monthName"     : monthName,
                "today"         : today.day,
                "nextMonthLink" : nextMonthLink,
                "prevMonthLink" : prevMonthLink,
                "bubls"         : monthBubls,
            };

    return render(request, "monthly.html", args);

#################################
# Weekly view
# 
# Displays a view of the week
# and allows for the users to view
# other weeks
#################################
def weekly(request, month, day, year):
        
    # Check if user is logged in
    result = bublcal_lib.verifyLogin(request);

    # Tell user the need to be signed in
    if(not result[0]):
        return render(request, "loggin_message.html");
    
    # Grab the user and update their bubls
    user = result[1];
    bublcal_lib.timeCheck(user);

    # Grab the users bubls
    bubls = bublcal_lib.getUserBubbles(user);

    # Get the days and week that we are viewing
    today = datetime.datetime(year=year, month=month, day=day);
    week = bublcal_lib.getWeekFromDay(today);

    weekFormatted = {};

    # Format the week
    for day in week:
        weekFormatted[day.strftime("%a")] = day.day;

    # Get next & previous week links
    nextWeek = bublcal_lib.getNextWeek(today)[0];
    prevWeek = bublcal_lib.getPreviousWeek(today)[0];

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

    args = {
        "loggedIn"          : True,
        "bubls"             : bubls,
        "day_of_week"       : day_of_week,
        "day"               : suffix(today.day),
        "week"              : weekFormatted,
        "year"              : year,
        "month"             : month,
        "month_year"        : today.strftime("%B %Y"),
        "nextWeekLink"      : nextWeek.strftime("/app/weekly/%m/%d/%Y"),
        "prevWeekLink"      : prevWeek.strftime("/app/weekly/%m/%d/%Y"),
    };

    return render(request, "weekly.html", args);

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
            return redirect(request.META.get('HTTP_REFERER'));
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
        return redirect(request.META.get('HTTP_REFERER'));

    # Make sure user owns bubble
    if(bubl.email.email != user):
        return redirect(request.META.get('HTTP_REFERER'));
    
    bublcal_lib.deleteBubble(request, id);

    return redirect(request.META.get('HTTP_REFERER'));

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

# View a certain day
def daily(request, month, day, year):
    
    # Make sure a user is logged in
    result = bublcal_lib.verifyLogin(request);

    if(not result[0]):
        return redirect("index");

    user = result[1];

    # Make sure a valid date passed is valid
    dayToView = None;
    
    try:
        dayToView = datetime.date(year=year, month=month, day=day);
    except ValueError:
        dayToView = None;

    if(dayToView == None):
        args = { "validDate": False };

        return render(request, "day.html", args);
    
    # Grab date objects for yesterday, today, and tomorrow
    today       = dayToView;
    yesterday   = dayToView - datetime.timedelta(1);
    tomorrow    = dayToView + datetime.timedelta(1);
    
    # Grab the names for the days above
    todayName       = DAY_NAMES[today.weekday()][0];         # Long name
    yesterdayName   = DAY_NAMES[yesterday.weekday()][1];     # Short name
    tomorrowName    = DAY_NAMES[tomorrow.weekday()][1];      # Short name
    
    # Time slots for the day, in this instantce we will be viewing all 24 hours
    timeSlots = [];

    for i in range(24):
        newT = datetime.datetime.now();
        newT = newT.replace(hour=i, minute=0);
        timeSlots.append([i, newT.strftime("%I:%M %p"), []]);

    # Grab the users bubls
    bubls = bublcal_lib.getUserBubbles(user);

    # Number of tasks for yesterday and tomorrow
    yesterdayTasks = 0;
    tomorrowTasks = 0;

    # Go through users bubls to check what to do to them
    if(bubls != None):
        for bubl in bubls:

            # Get the day the bubl lands on
            day = bubl.date.day;

            # Check if the tasks lands yesterday
            if(day == yesterday.day):
                yesterdayTasks += 1;

            # Check if the tasks lands tomorrow
            if(day == tomorrow.day):
                tomorrowTasks += 1;

            # Add bubbls that do fall under the active day
            if(day == today.day):

                # Go through each time slot for sorting
                for time in timeSlots:

                    # If the bubl and timeslot share the same hour
                    if(time[0] == bubl.time.hour):

                        # If array is empty then just insert into the first spot
                        if len(time[2]) == 0:
                            time[2].append(bubl);
                        else:
                            # Search for a spot within the bubls
                            foundSpot = False;

                            # Go through each bubl in timeslot
                            for i in range(len(time[2])):
                                tbubl = time[2][i];

                                # Match found
                                if(bubl.time.minute < tbubl.time.minute):
                                    time[2].insert(i, bubl);
                                    foundSpot = True;
                                    break;

                            # If no spot was found then append it to the end
                            if(not foundSpot):
                                time[2].append(bubl);

    previousDayLink = yesterday.strftime("%m/%d/%Y/");
    nextDayLink = tomorrow.strftime("%m/%d/%Y/")

    # Arguments to pass
    args = {
                "loggedIn"  : True,
                "today"     : today,
                "yesterday" : yesterday,
                "tomorrow"  : tomorrow,
                
                "today_name"        : todayName,
                "yesterday_name"    : yesterdayName,
                "tomorrow_name"     : tomorrowName,

                "timeSlots"         : timeSlots,
                "yesterdayTasks"    : range(yesterdayTasks),
                "tomorrowTasks"     : range(tomorrowTasks),
                "previousDayLink"   : previousDayLink,
                "nextDayLink"       : nextDayLink,
                "validDate"         : True,
            };

    return render(request, "day.html", args);

# Daily/"At a glance" view
def glance(request):
    
    # Make sure a user is logged in
    result = bublcal_lib.verifyLogin(request);

    if(not result[0]):
        return redirect("index");
    
    user = result[1];
    
    # Checks that no bubls are over due
    bublcal_lib.timeCheck(user)

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
    timeSlots = [[currentHour, currentTime.replace(minute=0).strftime("%I:%M %p"), []]];

    todayTime = datetime.datetime.today();

    # Create the rest of the timeslots for the array
    for i in range(currentHour + 1, 24):
        newT = todayTime;
        newT = newT.replace(hour=i, minute=0);
        timeSlots.append([i, newT.strftime("%I:%M %p"), []]);
    
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

                # Go through each time slot for sorting
                for time in timeSlots:

                    # If the bubl and timeslot share the same hour
                    if(time[0] == bubl.time.hour):

                        # If array is empty then just insert into the first spot
                        if len(time[2]) == 0:
                            time[2].append(bubl);
                        else:
                            # Search for a spot within the bubls
                            foundSpot = False;

                            # Go through each bubl in timeslot
                            for i in range(len(time[2])):
                                tbubl = time[2][i];

                                # Match found
                                if(bubl.time.minute < tbubl.time.minute):
                                    time[2].insert(i, bubl);
                                    foundSpot = True;
                                    break;

                            # If no spot was found then append it to the end
                            if(not foundSpot):
                                time[2].append(bubl);

    # Arguments to pass
    args = {
                "loggedIn"  : True,
                "today"     : today,
                "tomorrow"  : tomorrow,
                "overmorrow": overmorrow,
                
                "today_name"        : todayName,
                "tomorrow_name"     : tomorrowName,
                "overmorrow_name"   : overmorrowName,

                "timeSlots"         : timeSlots,
                "tomorrowTasks"     : range(tomorrowTasks),
                "overmorrowTasks"   : range(overmorrowTasks),
            };

    # Render the page
    return render(request, "glance.html", args);

# Main Page View
def index(request):
     # Make sure a user is logged in
    result = bublcal_lib.verifyLogin(request);

    if(not result[0]):
        return render(request, "index.html");
    
    return redirect("glance-view");


# Dead Bubl View
def deadview(request):
     # Make sure a user is logged in
    result = bublcal_lib.verifyLogin(request);

    if(not result[0]):
        return redirect("index");
    
    user = result[1];

    bubls = bublcal_lib.getUserDeadBubls(user);

    args = {
        "loggedIn": True,
        "bubls": bubls,
    };

    return render(request, "deadview.html", args);

# Kill a bubl
def killbubl(request, id):
    # Make sure a user is logged in
    result = bublcal_lib.verifyLogin(request);
    
    if(not result[0]):
        return redirect("index");
    
    user = result[1];
    bubl = bublcal_lib.getBubbleObject(id);

    # Make sure bubble exists
    if(bubl == None):
        return redirect(request.META.get('HTTP_REFERER'));

    # Make sure user owns bubble
    if(bubl.email.email != user):
        return redirect(request.META.get('HTTP_REFERER'));
    
    bublcal_lib.killBubble(request, id);

    return redirect(request.META.get('HTTP_REFERER'));

# Restore a bubl
def restorebubl(request, id):
    # Make sure a user is logged in
    result = bublcal_lib.verifyLogin(request);
    
    if(not result[0]):
        return redirect("index");
    
    user = result[1];
    bubl = bublcal_lib.getBubbleObject(id);

    # Make sure bubble exists
    if(bubl == None):
        return redirect("dead-view");

    # Make sure user owns bubble
    if(bubl.email.email != user):
        return redirect("dead-view");
    
    bublcal_lib.restoreBubl(request, id);

    return redirect("dead-view");

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
