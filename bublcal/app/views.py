from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
import datetime

DAYS_NAME = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
DAYS_NAME_SHORT = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

# Create your views here.

def home(request):
    name = "ubaldo";

    htcal = HTMLCalendar().formatmonth(2022, 1);

    return render(request, "home.html", {"name": name, "htcal": htcal});

def daily(request):

    today = datetime.date.today();
    yesterday = datetime.date.today()-datetime.timedelta(1);
    tomorrow = datetime.date.today()+datetime.timedelta(1);

    todayName = DAYS_NAME[today.weekday()];
    yesterdayName = DAYS_NAME_SHORT[yesterday.weekday()];
    tomorrowName = DAYS_NAME_SHORT[tomorrow.weekday()];


    return render(
                    request, 
                    "glance.html", 
                    {
                        "today": today,
                        "yesterday": yesterday,
                        "tomorrow": tomorrow,
                        
                        "today_name" : todayName,
                        "yesterday_name" : yesterdayName,
                        "tomorrow_name" : tomorrowName,
                    });