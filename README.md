# viblog - a blogging website made from django

This is a simple blogging website made on top of django web-framework. It allows user to create posts or articles and view other as well.

Features:
    preview panel while writing articles
    search feature
    comment section
    like and dislike option
    user profile section
    managing articles
    draft feature etc.

#### How to run project
    1. clone/download the repo
    2. goto terminal/cmd and navigate to requirements.txt folder
    3. run command 'pip install -r requirements.txt'
    4. run command 'python manage.py migrate'
    5. run command 'python manage.py makemigrations'
    6. run command 'python manage.py migrate'
    7. run command 'python manage.py createsuperuser' and enter your username and password (may skip this if not wanted to acces admin)
    8. run command 'python manage.py runserver' to run the server
    9. goto 'http://127.0.0.1:8000/' to checkout the site
    10. goto 'http://127.0.0.1:8000/admin' to access admin interface with your step-7 credentials
