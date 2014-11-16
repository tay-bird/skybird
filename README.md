# SKYBIRD.
This is the code that serves **http://skybird.taybird.com/**. It can
be run locally, or through Apache with WSGI.

## Installation.
Install Skybird and all dependencies:

    mkdir skybird
    cd skybird

    git clone https://taybird@bitbucket.org/taybird/skybird.git
    git clone https://taybird@bitbucket.org/taybird/mailchecker.git
    git clone https://taybird@bitbucket.org/taybird/gcalendar.git

    git pip install -r interface/req.txt

## Setup.
Now that Skybird is installed, you'll want to create a config
file and a script to run the server:

    touch CONFIG
    touch runserver.py

### CONFIG.
Your CONFIG file should look like this:

    { "STORMPATH":
          { "STORMPATH_API_KEY_FILE": "[[PATH TO SKYBIRD]]/keys/apiKey.properties",
            "STORMPATH_APPLICATION": "YOUR STORMPATH APP NAME" },
      "EMAIL":
          { "MAIL_STORAGE": "[[PATH TO SKYBIRD]]/mailchecker/mail.json" },
      "DOC_MANAGER":
          { "UPLOADS_FOLDER": "[[PATH TO SKYBIRD]]/docmanager/root/",
            "MAX_SIZE_IN_MB": 32 },
      "CALENDAR":
          {"CLIENT_ID": "[[YOUR GOOGLE CLIENT ID]]",
           "CLIENT_SECRET": "[[YOUR GOOGLE CLIENT SECRET]]",
           "credential_storage": "credentials/",
           "callback_uri": "http://[[YOUR DOMAIN]]/callback" }
      }

### Run Script.
If you want to run a local version, your run script should look like this:

    from interface import app as application
    application.secret_key = '[[A SECRET KEY]]'
    application.run(debug=True)

If you want to run a production version with **wsgi**, your run script might look like this:

    import sys
    import logging
    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0,"[[PATH TO SKYBIRD]]/interface/")

    from interface import app as application
    application.secret_key = '[[A SECRET KEY]]'
