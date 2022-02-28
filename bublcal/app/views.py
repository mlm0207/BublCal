# Imports
import calendar
import datetime
from django.shortcuts import render
from calendar import HTMLCalendar
import cgi
from django.db import models
from app.models import UserData, UserLogin

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


def main(request):
    current_date = datetime.date.today()
    current_year = current_date.year
    current_month = current_date.month
    htcal = HTMLCalendar().formatmonth(current_year, current_month)

    return render(request, "main.html", {
        "htcal": htcal,
        "year": current_year,
    })


def weekly(request):
    current_date = datetime.date.today()
    year, week_num, day_of_week = current_date.isocalendar()
    month_year = current_date.strftime("%B") + " " + str(year)
    day_of_week = calendar.day_name[day_of_week-1]
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

    return render(request, "weekly.html", {
        "day_of_week": day_of_week,
        "day": day,
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
    args = {};

    return render(request, "login.html", args);


# Signup Page
def signup(request):
    form = cgi.FieldStorage()

    if request.method == "POST":
        fname = form.getvalue('firstName')
        lname = form.getvalue('lastName')
        bday = form.getvalue('birthday')
        mail = form.getvalue('mail')
        pswd = form.getvalue('password')

    
        mailSplit = str(mail).split('@', 1)

        ud = UserData(email=mail, first_name=fname, last_name=lname, dob=bday)
        ul = UserLogin(user_name=mailSplit[0], email=mail, password=pswd)

  
    args = {};

    return render(request, "signup.html", args);

## NOT USED. KEEPING FOR REFERENCE CURRENTLY. TO BE REMOVED AT SOME POINT - Cesar Carrillo
#def home(request):
#    current_date = datetime.date.today()
#    current_year = current_date.year
#    current_month = current_date.month
#    htcal = HTMLCalendar().formatmonth(current_year, current_month)#
#
#    return render(request, "home.html", {
#        "htcal": htcal,
#        "year": current_year,
#        "month": current_month,
#    })

