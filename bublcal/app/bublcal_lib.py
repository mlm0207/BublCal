# Imports
import datetime
import re
from app.models import UserData
from app.models import Bubl

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
        if(bubl.email.email == email):
            bubls.append(bubl);

    return bubls;

# Get a bubble info via DB ID
def getBubbleObject(id):
    for bubl in Bubl.objects.all():
        if(bubl.id == id):
            return bubl;

# Delete a bubble via DB ID
def deleteBubble(request, id):
    result = verifyLogin(request);

    # Grab user
    if(result[0]):
        user = getUserObject(result[1]);
        bubls = getUserBubbles(user.email);
        
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
        if bubl.email.email == email: #and bubl.deleted == False

            # If date is today then check time
            if bubl.date == datetime.date.today():
                if bubl.time <= datetime.datetime.now().time():
                    bubl.time = (datetime.datetime.now() + datetime.timedelta(hours=1)).time()
                    # bubl.moved = bubl.moved + 1
                    # if bubl.moved == 3:
                        # bubl.deleted = True
                    bubl.save()    # Moves event 1 hour ahead of current time if time available
                    for b2 in Bubl.objects.all():
                        if b2.email.email == email:
                            if b2.time == bubl.time:
                                bubl.time = bubl.time + (datetime.timedelta(hours=1)).time()
                                bubl.save()   # Moves bubl another hour ahead if time slot taken

            # If date is earlier, able to skip bubl.time check
            if bubl.date < datetime.date.today():
                bubl.date = datetime.date.today() # Moves event to same time today if time is not taken.
                # bubl.moved = bubl.moved + 1
                    # if bubl.moved == 3:
                        # bubl.deleted = True
                bubl.save()
                for b2 in Bubl.objects.all():
                    if b2.email.email == email:
                        if b2.date == datetime.date.today():
                            if bubl.time == b2.time:
                                bubl.date = datetime.date.today() + datetime.timedelta(1) # If time slot is taken, move to tomorrow.
                                bubl.save()
                # Moves event to same time tomorrow
                

                
