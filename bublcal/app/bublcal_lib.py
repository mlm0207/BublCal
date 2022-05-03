# Imports
import datetime
import re
import calendar
from app.models import UserData
from app.models import Bubl

#################################
# nextMonthDate
# 
# returns the next month and year
# using given month/year
#################################
def nextMonthDate(month, year):
    month += 1;

    if(month > 12):
        month = 1;
        year += 1;

    return [month, year];

#################################
# previousMonthDate
# 
# returns the previous month and 
# year using given month/year
#################################
def previousMonthDate(month, year):
    month -= 1;

    if(month < 1):
        month = 12;
        year -= 1;

    return [month, year];

#################################
# getWeekFromDay
# 
# Get the week from a given day
#################################
def getWeekFromDay(day):

    # The name of the game is find sunday
    # if the day given is not a sunday, then we will go back 1 day until we find sunday
    # once sunday is found we return a list of datetime objects mon-sun

    dayName = day.strftime("%A");

    if(dayName == "Sunday"): # Found!

        days = [];

        day = day - datetime.timedelta(1);

        # Append days in week
        for i in range(7):
            day = day + datetime.timedelta(1);
            days.append(day);

        return days;
    else:
        return getWeekFromDay(day - datetime.timedelta(1)); # Go back 1 day

#################################
# getMonthWeeks
# 
# Get all weeks associated with this month
#################################
def getMonthWeeks(year, month):
    firstDay    = datetime.datetime(year=year, month=month, day=1);
    lastDay     = calendar.monthrange(year, month)[1];

    # Week list to return
    weeks = [];

    # First week
    weeks.append(getWeekFromDay(firstDay));

    # Flag for when last week is found
    lastWeekFound = False;

    # Add remaining weeks
    while not lastWeekFound:
        # Get the last week in the list and check if that is the last week
        weekLastDay = weeks[len(weeks) - 1][6];

        if(weekLastDay.month == month): # Same Month
            if(weekLastDay.day != lastDay): # Not Last Mont Day
                nextDay = weekLastDay + datetime.timedelta(1);
                weeks.append(getWeekFromDay(nextDay)); # Add the next week
            else:
                lastWeekFound = True;
        else:
            lastWeekFound = True;

    return weeks; # Return results

# Get previous week
def getPreviousWeek(day):

    week = getWeekFromDay(day);

    previousWeekDay = week[0] - datetime.timedelta(1);

    return getWeekFromDay(previousWeekDay);

# Get next week
def getNextWeek(day):

    week = getWeekFromDay(day);

    nextWeekDay = week[6] + datetime.timedelta(1);

    return getWeekFromDay(nextWeekDay);

# Verify if a user is logged in
def verifyLogin(request):
    session = request.session;

    if("email" in session):
        if(session["email"] != None):
            email = session["email"]
        
            return [True, email];

    return [False, None];

# Login a user
def loginUser(request, email):
    request.session["email"] = email;

# Logout user
def logoutUser(request):
    request.session["email"] = None;

# Get a user object via email
def getUserObject(email):
    for user in UserData.objects.all():
        if(user.email == email):
            return user; # Object found

    return None; # No object found

# Account creation fail types
AC_FAIL_AGE             = 0;
AC_FAIL_EMAIL_INVALID   = 1;
AC_FAIL_EMAIL_USED      = 2;

# Create a user
def createuser(email, password, firstName, lastName, birthday):

    # Calculate users age
    userBirth   = datetime.datetime.strptime(birthday, "%Y-%m-%d").date();
    activeDay   = datetime.date.today();
    userAge     = (activeDay - userBirth).days / 365.25;

    # Make user user is >= 13 age
    if(userAge < 13):
        return [False, AC_FAIL_AGE];

    # Check if email is in proper format
    emailReg = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)";

    if(not re.search(emailReg, email)):
        return [False, AC_FAIL_EMAIL_INVALID];

    # Check if email is not being used
    if(getUserObject(email) != None):
        return [False, AC_FAIL_EMAIL_USED];

    # Create account & save it to DB
    userData = UserData(email=email, 
                        password=password, 
                        firstName=firstName, 
                        lastName=lastName, 
                        birthday=birthday);
    userData.save();

    return [True, -1]; # Account is created

def deleteUser(email):
    print("\nWARNING: FUNCTION deleteUser NOT CREATED\nUSER: \"", email, "\" WILL  NOT DELETED!!!!\n");

# Sign-in fail types
SI_FAIL_EMAIL       = 0;
SI_FAIL_PASSWORD    = 1;

# Check a users login details
def userLoginCheck(email, password):
    user = getUserObject(email);

    if(user != None):
        if(user.password == password):
            return [True, -1];
        else:
            return [False, SI_FAIL_PASSWORD];
    
    return [False, SI_FAIL_EMAIL];

# Bubble create fail types
BC_FAIL_NO_USER         = 0;
BC_FAIL_INVALID_DATE    = 1;
BC_FAIL_INVALID_LENGTH  = 2;

# Create a bubble
def createBubble(email, name, note, date, time, length):
    
    # Find the owner of the bubble
    user = getUserObject(email);

    # If no owner is found then we will return an error
    if(user == None):
        return [False, BC_FAIL_NO_USER];

    # TODO: add datetime check, name check, length check
    bubl = Bubl(email=user, 
                name=name, 
                note=note, 
                date=date, 
                time=time, 
                length=length);
    bubl.save();

    return [True, -1];

# Get a list of bubbls using given user
def getUserBubbles(email):
    user = getUserObject(email);

    if(user == None):
        return None;

    bubls = [];

    for bubl in Bubl.objects.all():
        if(bubl.email.email == email and bubl.dead == False): # Can be changed - this 2nd if removed 'deleted' bubls from view
            bubls.append(bubl);
    
    # Bubble sort for user bubls, array is now ordered by time
    i = len(bubls)
    for b1 in range(i-1):
        for b2 in range(0, i-1):
            if bubls[b2].time > bubls[b2 + 1].time:
                bubls[b2], bubls[b2 + 1] = bubls[b2 + 1], bubls[b2]

    return bubls;

# Get a list of dead bubls using given user
def getUserDeadBubls(email):
    user = getUserObject(email);

    if(user == None):
        return None;

    bubls = [];

    for bubl in Bubl.objects.all():
        if(bubl.email.email == email and bubl.dead == True):
            bubls.append(bubl);

    return bubls; 

# Get a bubble info via DB ID
def getBubbleObject(id):
    for bubl in Bubl.objects.all():
        if(bubl.id == id):
            return bubl;

# Restore a bubl via DB ID
def restoreBubl(request, id):
    result = verifyLogin(request);

    if(result[0]):
        user = getUserObject(result[1]);
        bubls = getUserDeadBubls(user.email);

        if(bubls != None):
            print(bubls);
            for bubl in bubls:
                if(bubl.id == id):
                    if(request.method == "POST"):
                            bubl.name = request.POST["name"];
                            bubl.note = request.POST["note"];
                            bubl.date = request.POST["date"];
                            bubl.time = request.POST["time"];
                            bubl.length = request.POST["length"];
                            bubl.dead = False;
                            bubl.save();

                            bubl.save();
                    return True;

    return False;

# Kill a bubble via DB ID
def killBubble(request, id):
    result = verifyLogin(request);

    if(result[0]):
        user = getUserObject(result[1]);
        bubls = getUserBubbles(user.email);

        if(bubls != None):
            for bubl in bubls:
                if(bubl.id == id):
                    bubl.dead = True;
                    bubl.save();
                    return True;

    return False;

# Delete a bubble via DB ID
def deleteBubble(request, id):
    result = verifyLogin(request);

    # Grab user
    if(result[0]):
        user = getUserObject(result[1]);
        bubls = getUserDeadBubls(user.email);

        if(bubls != None):
            for bubl in bubls:
                if(bubl.id == id):
                    bubl.delete();
                    return True; # item was deleted
    
    return False; # item was not deleted

# Check for bubl past due and move them back to schedule
def timeCheck(email):
    user = getUserObject(email)
    if(user == None):
        return False

    for bubl in Bubl.objects.all():
        if bubl.email.email == email and bubl.dead == False and bubl.done == False:

            # If date is today then check time
            if bubl.date == datetime.date.today():
                if bubl.time <= datetime.datetime.now().time():
                    bubl.time = (datetime.datetime.now() + datetime.timedelta(hours=1)).time()
                    bubl.moved = bubl.moved + 1
                    if bubl.moved == 3:
                        bubl.dead = True
                    bubl.save()    # Moves event 1 hour ahead of current time if time available
                    for b2 in Bubl.objects.all():
                        if b2.email.email == email:
                            if b2.time == bubl.time:
                                bubl.time = (datetime.datetime.now() + datetime.timedelta(hours=2)).time()
                                bubl.save()   # Moves bubl another hour ahead if time slot taken

            # If date is earlier, able to skip bubl.time check
            if bubl.date < datetime.date.today():
                bubl.date = datetime.date.today() # Moves event to same time today if time is not taken.
                bubl.moved = bubl.moved + 1
                if bubl.moved == 3:
                    bubl.dead = True
                bubl.save()
                for b2 in Bubl.objects.all():
                    if b2.email.email == email:
                        if b2.date == datetime.date.today():
                            if bubl.time == b2.time:
                                bubl.date = datetime.date.today() + datetime.timedelta(1) # If time slot is taken, move to tomorrow.
                                bubl.save() # Moves event to same time tomorrow
