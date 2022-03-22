# Imports
import datetime
import re
from app.models import UserData
from app.models import Bubl

# Get a user object via email
def getUserObject(email):
    for user in UserData.objects.all():
        if(user.email == email):
            return user; # Object found

    return None; # No object found

# Get a users info via email
def getUserInfo(email):

    user = getUserObject(email);

    if(user != None):
        return [user.firstName, user.lastName, user.birthday];
    else:
        return None;

# Check if a user is logged into the session
def checkUserLogged(request):

    session = request.session;

    if("loggedIn" in session):
        return session["loggedIn"];

    return False;

# Return the user that is logged in / None = no user logged in
def getLoggedUser(request):

    session = request.session;

    if(checkUserLogged(request)):
        return session["user"];
    else:
        return None;

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
    userData = UserData(    email=email, 
                            password=password, 
                            firstName=firstName, 
                            lastName=lastName, 
                            birthday=birthday       );
    userData.save();

    return [True, -1];

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
    owner = getUserObject(email);

    # If no owner is found then we will return an error
    if(owner == None):
        return [False, BC_FAIL_NO_USER];

    # TODO: add datetime check, name check, length check

    bubl = Bubl(email=owner, name=name, note=note, date=date, time=time, length=length);
    bubl.save();

    return [True, -1];

def getUserBubbles(email):
    user = getUserObject(email);
    
    if(user == None):
        return None;

    userbubls = [];

    for bubl in Bubl.objects.all():
        if(bubl.email.email == email):
            userbubls.append(bubl);

    return userbubls;

def getBubblesByUserDate(email, year, month, day):
    print("\nWARNING: FUNCTION getBubblesByUserDate NOT CREATED\n");

def deleteBubble(request, id):
    user = getLoggedUser(request);

    if(user != None):
        bubls = getUserBubbles(user);

        if(bubls != None):
            for bubl in bubls:
                if(bubl.id == id):
                    bubl.delete();

def modifyBubble():
    print("\nWARNING: FUNCTION modifyBubble NOT CREATED\n");
