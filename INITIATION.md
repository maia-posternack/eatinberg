MY SHORT VIDEO:
    Sorry it has so many cuts it was orginally 5 mins and I had to get it down to 2!
    https://youtu.be/DKb7UH868lk

HOW TO RUN:
    Begin by downloading all code files, putting them in a folder, and opening them in a desktop VS Code

    In ther terminal of VS Code, enter the folder then run the following lines

        source env/bin/activate
            // this line gets you to a workspace where all the necessary libaries are downloaded. if this doesn't work, run : pip install -r  requirements.txt

        See SECRETS.md to find what google ids to export

        python app.py
            // this runs the program
            // you should see the terminal response: * Serving Flask app 'app'
                * Debug mode: off
                INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
                * Running on https://127.0.0.1:5000
                INFO: Press CTRL+C to quit

HOW TO VIEW:
    Once you run the program go to https://127.0.0.1:5000 on any browser

    You may see a page that says "Your connection is not private"

    This is because I need a HTTPS to run the Google API but the page is actually a HTTP

    Don't worry. This is normal.
        ON GOOGLE CHROME: click "advanced" and then "Proceed to 127.0.0.1 (unsafe)"

        ON SAFARI: click "show details" and then "visit the website"

SETTING UP THE PROGRAM:
    Begin by clicking Login and logging in with a your google account. You need to log in with a college.harvard.edu email. If you are already signed into chrome on a none Harvard email, you may need to open an incognito browser

    Once signed in, allow Location Services.
        ON GOOGLE CHROME:

            If you see a popup saying: Error (1): User denied Geolocation click the location icon in the right of your browser search bar and click "Always allow https://127.0.0.1:5000 to access your location"

                If this doesn't work, you might have to manuelly go to settings and allow location access for https://127.0.0.1:5000
                Then go to system preferences on your computer and make sure Google Chrome has permission to get your location

            Otherwise, you are all good. You already shared them! Click "NOT SECURE" in the left of the search bar and make sure Location is toggled on to double check

        ON SAFARI: there should be a popup that says “127.0.0.1” would like to use your current location. Click "allow"

Now you are ready to go!

PROGRAM FUNCTIONALITY:
    "/" is the homepage. It simply records your location and redirects you to "/map". Don't do anything on this page

    "/map" also known as "Me" in the NavBar allows you to
        1. See the closest path to Annenberg
            This is on the Google Map
        2.Turn on Ghost mode (which makes it so that the program thinks you are not in Annenberg even if you are)
            Toggle and click the save button
        3.See your Annenberg status
            This is a statement at the top of page
            Note that if you are in ghost mode it will say you are not in Berg even if you are


    "/friends" also known as "Friends" in the NavBar allows you to:
        1. See whether your friends are in Berg
            This is the table on the page
        2. Remove friends
            Do this by clicking "Remove Friend" for the desired user
        3. Add Friends
            Type the email of a friend who has an account into the input box and click "Add Friend
        4. Invite People
            Type the email of a friend who doesn't have an account and click "Invite" They will get a custom email from a custom email address telling them you want them to join

DEBUGGING:
    If there is any error, it could be 1 of 2 things
        1. Your location services aren't on

        2. There is a Depreciation error. Check the Terminal and see if it says:

            DeprecationWarning: 'session_cookie_name' is deprecated and will be removed in Flask 2.3. Use 'SESSION_COOKIE_NAME' in 'app.config' instead.

        If this is the case, it is just flask being annoying. There is now way to fix it that I found. Simply rerun python app.py and you should be good!!
