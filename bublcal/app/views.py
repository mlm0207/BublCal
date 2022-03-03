# Imports
import calendar
import datetime
from django.shortcuts import render
from calendar import HTMLCalendar
from django.db import models
from app.models import UserData, UserLogin
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
    args = {};

    return render(request, "login.html", args);


# Signup Page
def signup(request):

    if request.method == "POST":
        
        fname = forms.CharField(label='firstName')
        lname = forms.CharField(label='lastName')
        bday = forms.DateField(label='birthday')
        mail = forms.CharField(label='mail')
        pswd = forms.CharField(label='password')

    
        mailSplit = str(mail).split('@', 1)

        ud = UserData(email=mail, first_name=fname, last_name=lname, dob='2021-1-24') #Placeholder dob
        ud.save()
        #ul = UserLogin(user_name=mailSplit[0], email=mail, password=pswd)
        #ul.save()
        # UserLogin foreign key required a UserData instance of 'mail' so this has been left out
        # may be best to condense UserLogin and UserData in the database

        return HttpResponseRedirect('/app/login/')

  
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

