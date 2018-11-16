Blog Website with Django
========
### To setup this website on your system:-
**Step1:-** Create a virtual env.

    python3 -m pip install virtualenv
    virtualenv blog_env

**Step2:-** Activate the Virtual Environment.

    for linux or mac users:-
        source blog_env/bin/activate

    for windows guy:-
        cd blog_env/scripts/
        activate
        cd ../../


**Step3:-** One the downloaded folder. Then run these command:-

    python3 -m pip install -r requirements.txt
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py collectstatic
    python3 manage.py runserver

#### Now your website will be ready on url http://localhost:8000 and on http://127.0.0.1:8000

You can create Superuser by the command

    python3 manage.py createsuperuser

then it will ask username, email, password, confirm password. Type those correctly and the user will be created. 

#### Then You can access Admin on http://localhost:8000/admin/

### ***Created By:*** Yash Goyal ***with*** love
