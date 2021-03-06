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

current_date = datetime.date.today()
year, week_num, day_of_week = current_date.isocalendar()
month_year = current_date.strftime("%B") + " " + str(year)
day_of_week = calendar.day_name[day_of_week - 1]

#################################
# Glance view
# 
# Displays a view of the users
# day and the next to days
#################################
def glance(request):

    # Check if user is logged in
    result = bublcal_lib.verifyLogin(request);

    # Tell user the need to be signed in
    if(not result[0]):
        return render(request, "login_message.html");
    
    # Grab the user and update their bubls
    user = result[1];
    bublcal_lib.timeCheck(user);

    # Grab the active day and the two days after
    today       = datetime.date.today();
    tomorrow    = datetime.date.today() + datetime.timedelta(1);
    overmorrow  = datetime.date.today() + datetime.timedelta(2);
    
    # Grab the names for the days above
    todayName      = today.strftime("%A");         # Long name
    tomorrowName   = tomorrow.strftime("%a");      # Short name
    overmorrowName = overmorrow.strftime("%a");    # Short name

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
    tomorrowTasks = [];
    overmorrowTasks = [];

    # Go through users bubls to check what to do to them
    if(bubls != None):
        for bubl in bubls:

            # Get the day the bubl lands on
            day = bubl.date.day;

            # Check if the tasks lands tomorrow
            if(day == tomorrow.day):
                tomorrowTasks.append(bubl);

            # Check if the tasks lands overmorrow
            if(day == overmorrow.day):
                overmorrowTasks.append(bubl);

            # Add bubls that do fall under the active day
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

    # Get the greeting
    hour = datetime.datetime.now().hour;
    
    greeting = "evening";

    if(hour < 16):
        greeting = "afternoon";
    
    if(hour < 12):
        greeting = "morning";
    
    # Arguments to pass
    args = {
                "loggedIn"  : True,
                "today"     : today,
                "tomorrow"  : tomorrow,
                "overmorrow": overmorrow,
                "greeting"  : greeting,
                "firstName" : bublcal_lib.getUserObject(user).firstName,
                
                "today_name"        : todayName,
                "tomorrow_name"     : tomorrowName,
                "overmorrow_name"   : overmorrowName,

                "tomorrowLink" : tomorrow.strftime("%m/%d/%Y/"),
                "overmorrowLink" : overmorrow.strftime("%m/%d/%Y/"),

                "timeSlots"         : timeSlots,
                "tomorrowTasks"     : tomorrowTasks,
                "overmorrowTasks"   : overmorrowTasks,
            };

    # Render the page
    return render(request, "glance.html", args);

#################################
# Profile
# 
# Allows users to view and 
# change their profile info
#################################
def profile(request):

    # Check if user is logged in
    result = bublcal_lib.verifyLogin(request);

    # Tell user the need to be signed in
    if(not result[0]):
        return render(request, "login_message.html");
    
    # Grab the user
    usermail = result[1];

    correctPassword = True;
    infoUpdated = False;

    # Update info if passed
    if(request.method == "POST"):
        for user in UserData.objects.all():
            if user.email == usermail:
                if user.password == request.POST["password"]:
                    user.firstName = request.POST["fName"];
                    user.lastName = request.POST["lName"];
                    user.birthday = request.POST["birthDay"];
                    user.save();
                    infoUpdated = True;
                else:
                    correctPassword = False;

    # args for default form values
    args = { 
                "loggedIn": True, 
                "correctPassword": correctPassword,
                "infoUpdated": infoUpdated, 
            };

    for user in UserData.objects.all():
        if user.email == usermail:
            args["first_name"] = user.firstName;
            args["last_name"] = user.lastName;
            args["bday"] = user.birthday.strftime("%Y-%m-%d");
            args["email"] = user.email;
    
    return render(request, "profile.html", args);

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
        return render(request, "login_message.html");
    
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

    newT = [];

    for week in bublcal_lib.getMonthWeeks(year, month):
        sweek = [];
        for day in week:
            
            bublsDone = [];
            bublsComing = [];

            toolTipString = "";


            for bubl in monthBubls:
                if(bubl.date.day == day.day and bubl.date.month == day.month):
                    if(bubl.done):
                        if(len(bublsDone) < 2):
                            bublsDone.append(bubl);
                    else:
                        if(len(bublsComing) < 2):
                            bublsComing.append(bubl);

                    toolTipString += F"{bubl.name} @ {bubl.time.strftime('%I:%M %p')}\n";

            sweek.append([day, bublsDone, bublsComing, toolTipString]);

        newT.append(sweek);
    
    args =  {
                "loggedIn"      : True,
                "weeks"         : newT,
                "month"         : month,
                "year"          : year,
                "monthName"     : monthName,
                "today"         : today,
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
        return render(request, "login_message.html");
    
    # Grab the user and update their bubls
    user = result[1];
    bublcal_lib.timeCheck(user);

    # Grab the users bubls
    bubls = [];

    for bubl in bublcal_lib.getUserBubbles(user):
        if(bubl.date.month == month and bubl.date.year == year):
            bubls.append(bubl);

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

#################################
# Daily view
# 
# Displays a view of the day
# and allows for the users to view
# other days
#################################
def daily(request, month, day, year):
    
    # Check if user is logged in
    result = bublcal_lib.verifyLogin(request);

    # Tell user the need to be signed in
    if(not result[0]):
        return render(request, "login_message.html");
    
    # Grab the user and update their bubls
    user = result[1];
    bublcal_lib.timeCheck(user);

    # Make sure a valid date passed is valid
    dayToView = None;
    
    try:
        dayToView = datetime.date(year=year, month=month, day=day);
    except ValueError:
        dayToView = None;

    # Show invalid date error to user
    if(dayToView == None):
        args = { "validDate": False };

        return render(request, "day.html", args);
    
    # Grab date objects for yesterday, today, and tomorrow
    today       = dayToView;
    yesterday   = dayToView - datetime.timedelta(1);
    tomorrow    = dayToView + datetime.timedelta(1);
    
    # Grab the names for the days above
    todayName       = today.strftime("%A");         # Long name
    yesterdayName   = yesterday.strftime("%a");     # Short name
    tomorrowName    = tomorrow.strftime("%a");      # Short name
    
    # Time slots for the day, in this instantce we will be viewing all 24 hours
    timeSlots = [];

    for i in range(24):
        newT = datetime.datetime.now();
        newT = newT.replace(hour=i, minute=0);
        timeSlots.append([i, newT.strftime("%I:%M %p"), []]);

    # Grab the users bubls
    bubls = bublcal_lib.getUserBubbles(user);

    # Number of tasks for yesterday and tomorrow
    yesterdayTasks = [];
    tomorrowTasks = [];

    # Go through users bubls to check what to do to them
    if(bubls != None):
        for bubl in bubls:

            # Get the day the bubl lands on
            day = bubl.date.day;

            # Check if the tasks lands yesterday
            if(day == yesterday.day):
                yesterdayTasks.append(bubl);

            # Check if the tasks lands tomorrow
            if(day == tomorrow.day):
                tomorrowTasks.append(bubl);

            # Add bubls that do fall under the active day
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

    # Grab previous/next days
    previousDayLink = yesterday.strftime("%m/%d/%Y/");
    nextDayLink = tomorrow.strftime("%m/%d/%Y/")

    # Arguments to pass
    args = {
                "loggedIn"          : True,
                "today"             : today,
                "yesterday"         : yesterday,
                "tomorrow"          : tomorrow,
                
                "today_name"        : todayName,
                "yesterday_name"    : yesterdayName,
                "tomorrow_name"     : tomorrowName,
                "month_name"        : today.strftime("%B"),

                "timeSlots"         : timeSlots,
                "yesterdayTasks"    : yesterdayTasks,
                "tomorrowTasks"     : tomorrowTasks,
                "previousDayLink"   : previousDayLink,
                "nextDayLink"       : nextDayLink,
                "validDate"         : True,
            };

    return render(request, "day.html", args);

#################################
# Create bubl
# 
# Allows users to create bubls
# if data is being passed, if
# not then we just redirect to
# index
#################################
def createBubl(request):
    
    # Check if user is logged in
    result = bublcal_lib.verifyLogin(request);

    # Tell user the need to be signed in
    if(not result[0]):
        return render(request, "login_message.html");
    
    # Grab the user
    user = result[1];

    # Make sure data is being submitted
    if(request.method == "POST"):

        # Grab bubble data
        name    = request.POST["name"];
        note    = request.POST["note"];
        date    = request.POST["date"];
        time    = request.POST["time"];
        length  = request.POST["length"];

        result = bublcal_lib.createBubble(user, name, note, date, time, length);

        # TODO add feature that tells users if bubl was created or not
        return redirect(request.META.get('HTTP_REFERER'));

    return redirect("index");

#################################
# Delete bubl
# 
# Allows users to delete bubls
# this WILL DELETE the bubl from
# the database
#################################
def deleteBubl(request, id):
    
    # Check if user is logged in
    result = bublcal_lib.verifyLogin(request);

    # Tell user the need to be signed in
    if(not result[0]):
        return render(request, "login_message.html");
    
    # Grab the user and get the bubl to delete
    user = result[1];
    bubl = bublcal_lib.getBubbleObject(id);

    # Make sure bubble exists
    if(bubl == None):
        return redirect(request.META.get('HTTP_REFERER'));

    # Make sure user owns bubble
    if(bubl.email.email != user):
        return redirect(request.META.get('HTTP_REFERER'));
    
    # Delete it!
    bublcal_lib.deleteBubble(request, id);

    # TODO add feature that tells user if the bubl was deleted
    return redirect(request.META.get('HTTP_REFERER'));

#################################
# Kill bubl
# 
# Allows users to kill bubls
# this WILL NOT DELETE the bubl 
# from the database
#################################
def killbubl(request, id):
    
    # Check if user is logged in
    result = bublcal_lib.verifyLogin(request);

    # Tell user the need to be signed in
    if(not result[0]):
        return render(request, "login_message.html");
    
    # Grab the user and get the bubl to kill
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

#################################
# Modify bubl
# 
# Allows users to modify bubls
# information
#################################
def modifyBubl(request, id):
    
    # Check if user is logged in
    result = bublcal_lib.verifyLogin(request);

    # Tell user the need to be signed in
    if(not result[0]):
        return render(request, "login_message.html");
    
    # Grab the user and get the bubl to modify
    user = result[1];
    bubl = bublcal_lib.getBubbleObject(id);

    # Make sure bubble exists
    if(bubl == None):
        return redirect("glance-view");

    # Make sure user owns bubble
    if(bubl.email.email != user):
        return redirect("glance-view");

    # Make sure user is submitting data
    if(request.method == "POST"):

        # Save the new info
        bubl.name = request.POST["name"];
        bubl.note = request.POST["note"];
        bubl.date = request.POST["date"];
        bubl.time = request.POST["time"];
        bubl.length = request.POST["length"];

        bubl.save();

        #TODO add feature that tells if bubl was modified
        return redirect(request.META.get('HTTP_REFERER'));

    return redirect("index");

#################################
# Complete bubl
# 
# Allows users to mark bubls as
# "done"
#################################
def complete(request, id):
        # Check if user is logged in
    result = bublcal_lib.verifyLogin(request);

    # Tell user the need to be signed in
    if(not result[0]):
        return render(request, "login_message.html");
    
    # Grab the user and get the bubl to modify
    user = result[1];
    bubl = bublcal_lib.getBubbleObject(id);

    # Make sure bubble exists
    if(bubl == None):
        return redirect("glance-view");

    # Make sure user owns bubble
    if(bubl.email.email != user):
        return redirect("glance-view");
    
    bubl.done = True;
    bubl.save();

    return redirect(request.META.get('HTTP_REFERER'));

    

#################################
# Index
# 
# Shows the index view for new
# users, redirects logged in
# users to their glance view
#################################
def index(request):
    
    # Make sure a user is logged in
    result = bublcal_lib.verifyLogin(request);

    if(not result[0]):
        return render(request, "index.html");
    
    return redirect("glance-view");

#################################
# Dead bubl view
# 
# Allows users to view their
# dead bubls
#################################
def deadview(request):
    
    # Check if user is logged in
    result = bublcal_lib.verifyLogin(request);

    # Tell user the need to be signed in
    if(not result[0]):
        return render(request, "login_message.html");
    
    # Grab the user and get the dead bubls
    user = result[1];
    bubls = bublcal_lib.getUserDeadBubls(user);

    args =  {
                "loggedIn": True,
                "bubls": bubls,
            };

    return render(request, "deadview.html", args);

#################################
# Restore bubl
# 
# Allows users to restore dead
# bubls
#################################
def restorebubl(request, id):
    
    # Check if user is logged in
    result = bublcal_lib.verifyLogin(request);

    # Tell user the need to be signed in
    if(not result[0]):
        return render(request, "login_message.html");
    
    # Grab the user and the bubl to restore
    user = result[1];
    bubl = bublcal_lib.getBubbleObject(id);

    # Make sure bubble exists
    if(bubl == None):
        return redirect("dead-view");

    # Make sure user owns bubble
    if(bubl.email.email != user):
        return redirect("dead-view");
    
    # Restore it!
    bublcal_lib.restoreBubl(request, id);

    return redirect("dead-view");

#################################
# Signup
# 
# Allows users to create accounts
#################################
def signup(request):

    # Make user a user is not logged in
    result = bublcal_lib.verifyLogin(request);

    if(result[0]):
        return redirect("index");

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

        # Display results
        if(result[0]):
            return render(request, "signup_success.html"); # If success
        else:
            args = { "acFailType": result[1] };

            return render(request, "signup.html", args); # If fail

    return render(request, "signup.html");

#################################
# Login
# 
# Allows users to login/
#################################
def login(request):

    # Make user a user is not logged in
    result = bublcal_lib.verifyLogin(request);

    if(result[0]):
        return redirect("index");

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

#################################
# Logout
# 
# Allows users to logout
#################################
def logout(request):

    # Make sure there is a user to logout
    result = bublcal_lib.verifyLogin(request);

    if(not result[0]):
        return redirect("index");

    # logout
    bublcal_lib.logoutUser(request);

    return render(request, "logged_out.html");
