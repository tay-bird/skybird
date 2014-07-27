# SKYBIRD.
This is the code that serves **http://skybird.taybird.com/**. It can
be run locally, or through Apache with WSGI.

## Requirements.
Skybird is run on **Flask**. On the server, a **wsgi python file** is
used to initiate a call to the Flask logic.

### Authentication.
User authentication is handled with the **Flask-Stormpth** extension.
A valid Stormpath API key and app name must be pointed to in the
**CONFIG** file.

### Email.
Email functionality is provided by the Mailchecker package. A
valid Mailchecker **mail.json** file must be pointed to in the
**CONFIG** file.

## Usage.
Import the app object from the interface package. Pass it a
randomized secret key for the session.

Note that the app object must be imported with the name
**application** in order to be recognized.

    from interface import app as application

    application.secret_key = "SECRET_KEY"
