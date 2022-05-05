# BublCal
A simply powerful calendar app
Created as a capstone project for CSC 289

## Requirements
- Python 3.10+ & pip
- Django and Whitenoise

## Downloading
Clone the repo:
`git clone https://github.com/mlm0207/BublCal.git`

Install the requirements:
`pip install -r requirements`

## Preparing the Server
Create the database
- On Windows run `dbupdate.bat`
- On Linux run `dbupdate.sh`

Create a admin account
- On Windows run `createsuperuser.bat`
- On Linux run `createsuperuser.sh`

## Running for a Local Machine
On Windows
`py manage.py runserver`

On Linux
`python manage.py runserver`

## Running for a Public Server
Do the following:
- Open `bublcal/bublcal/settings.py`
- Set `DEBUG` to `False`
- Add `localhost` and your public IP to `ALLOWED_HOSTS`
- Uncomment `STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles");`
- On Windows run `py manage.py collectstatic`
- On Linux run `python manage.py collectstatic`

Run:
- On Windows `run_public.bat`
- On Linux `run_public.sh`
