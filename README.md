# SKYBIRD.

Skybird is a lightweight cloud service for personal servers. It provides
a email and calendar interface, file management, and server statistics
dashboards. Skybird can be run locally, or through Apache with WSGI.

I worked on this project in late 2014 to try my hand web development and
hosting, database administration, and user authentication with OAuth. This
is not intended to be consumable service, but as a sample of my work across
a variety of technical arenas.

## Installation.

Install Skybird and all dependencies:

    pip install -r requirements.txt

## Setup.

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
