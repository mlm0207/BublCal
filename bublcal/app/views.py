# Imports
import calendar
import datetime
from django.shortcuts import render
from calendar import HTMLCalendar

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


def home(request):
    current_date = datetime.date.today()
    current_year = current_date.year
    current_month = current_date.month
    htcal = HTMLCalendar().formatmonth(current_year, current_month)

    return render(request, "home.html", {
        "htcal": htcal,
        "year": current_year,
        "month": current_month,
    })

def weekly(request):
    current_date = datetime.date.today()
    year, week_num, day_of_week = current_date.isocalendar()
    month_year = current_date.strftime("%B") + " " + str(year)
    day_names = calendar.weekheader(3)
    day = current_date.day

    # dates in the current week
    weeks_list = []
    for weeks in calendar.monthcalendar(year, current_date.month):
        weeks_list.append(weeks)

    dates = ''
    for w in weeks_list:
        if day in w:
            dates = "  ".join(str(d) for d in w)

    return render(request, "weekly.html", {
        "day": day,
        "day_names": day_names,
        "month_year": month_year,
        "dates": dates,
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
