# django-api

## About the project
This project aims at providing RESTful API for users to upload images (only "JPEG"/"JPG" and "PNG" formats). Not all features have been implemented as of yet, to be continued.
This project is written in Python 3. As this is a development server, the images are stored in the default Django File Storage system (i.e. MEDIA_ROOT constant) that's not password-protected. As this has to be changed in production anyway, the authentication for this media storage url was not implemented (as opposed to API endpoints).

## How to run the project
1. Create a virtual environment (e.g. "python -m venv venv") and run it, then clone the repository/download the files.
2. Install dependencies from requirements.txt ("pip install -r requirements.txt") into the virtual environment.
3. Before running the server type in the following 2 commands: python manage.py make migrations, python manage.py migrate.
5. To run the project, start the development server by typing python manage.py runserver.
6. Go to the localhost:800/images endpoint in your browser (to use Django Rest Frameworks' browsable API functionality) or send an equivalent GET request.
7. To post your first file use the same endpoint, but first you'll need an account. 
8. Create Django superuser to be able to create new users ("python manage.py createsuperuser").
9. Go to localhost:800/admin to create a new user or use your admin account to post files.
10. Log into your account. Now you can post an image (see point 5).
11. The /images view now shows that image as well as any other images posted by that user.
12. Go to images/1 (assuming it's the very fist image on the filesystem) to see a detailed view of the image.
13. Use the link to get a url to your thumbnail(s). This feature will need to be improved, as it currently takes the user to the html template with the image thumbnail, rather than the thumbnail itself.
