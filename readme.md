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

## Running for a Local Machine
On Windows
`py manage.py runserver`

On Linux
`python manage.py runserver`

## Running for a Server
- Open `bublcal/bublcal/settings.py`
- Set `DEBUG` to `False`
- Add `localhost` and your public IP to `ALLOWED_HOSTS`
- Uncomment `STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles");`
- On Windows run `py manage.py collectstatic`
- On Linux run `python manage.py collectstatic`

Run the following command with a desired port

- On Windows `py manage.py runserver 0.0.0.0:8000`
- On Linux `python manage.py runserver 0.0.0.0:8000`
