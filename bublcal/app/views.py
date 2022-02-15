import calendar

from django.shortcuts import render
from calendar import HTMLCalendar
import datetime

DAYS_NAME = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAYS_NAME_SHORT = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# Create your views here.

def home(request):
    name = "ubaldo"
    current_date = datetime.date.today()
    current_year = current_date.year
    current_month = current_date.month
    htcal = HTMLCalendar().formatmonth(current_year, current_month)

    return render(request,
                  "home.html", {
                      "name": name,
                      "htcal": htcal,
                      "year": current_year,
                      "month": current_month,
                  })


def daily(request):
    today = datetime.date.today()
    yesterday = datetime.date.today() - datetime.timedelta(1)
    tomorrow = datetime.date.today() + datetime.timedelta(1)

    today_name = DAYS_NAME[today.weekday()]
    yesterday_name = DAYS_NAME_SHORT[yesterday.weekday()]
    tomorrow_name = DAYS_NAME_SHORT[tomorrow.weekday()]

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
