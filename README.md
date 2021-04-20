# django-api

## About the project
This project aims at providing RESTful API for users to upload images (only "JPEG"/"JPG" and "PNG" formats). Not all features have been implemented as of yet, to be continued.
This project is written in Python 3.

## How to run the project
1. Create a virtual environment (e.g. "python -m venv venv") and run it, then clone the repository/download the files.
2. Install dependencies from requirements.txt ("pip install -r requirements.txt") into the virtual environment.
3. To run the project, start the development server by typing python manage.py runserver.
4. Go to the localhost:800/images endpoint in your browser (to use Django Rest Frameworks' browsable API functionality) or send an equivalent GET request.
5. To post your first file use the same endpoint, but first you'll need an account. 
6. Create Django superuser to be able to create new users.
7. Go to localhost:800/admin to create a new user or use your admin account to post files.
8. Log into your account. Now you can post an image (see point 5).
9. The /images view now shows that image as well as any other images posted by that user.
10. Go to images/1 (assuming it's the very fist image on the filesystem) to see a detailed view of the image.
11. Use the link to get a link to your thumbnail(s). This feature will need to be improved, as it currently takes the user to the html template with the image thumbnail, rather than the thumbnail itself.
