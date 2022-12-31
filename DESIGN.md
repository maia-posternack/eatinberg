MOTIVATION:
    Do you ever want to know who is in Berg? It may be easy to send the "Dinner at 6?" text to a close friend, but it's harder if you want to get close with someone you don't know that well. Now, you can know who is in berg to meet that someone there or decide if you want to go!

A CHANGE IN GOALS:
    Originally, I had a lot of ideas for this project. I wanted to show a berg menu, allow you to set calender dates with your friends, and see exactly what table people are at so you don't just wander around. These goals changed as I started coding the project. I realized that it would be a better learning experience to learn how to use APIs (specifically login with gmail, google maps, and flask-mail) so my goals shifted to including as many APIs as possible, rather than just increasing functionality, and this goal was really successful!

GOALS I ACCOMPLISHED:
    Get's your location and allows you to see who is in berg!
    Uses a lot of APIs --> sign in with google :) :)
    Allows you to add delete and invite friends. 
    Allows you to hide frome people using Ghost mode. 
    Looks aesthetically pleasing ;) 

DESIGN DECISION:
    1. LOGIN WITH GOOGLE
        I really wanted login with google so that I could  prove that you were a harvard student. (You need to verify that you have a college.harvard.edu email using HarvardKey) It seems really creepy if anyone could just join the website and see the names of people who are in Berg. I also wanted the website to seem reliable and high-tech. 
        I use details from log in with google to dynamically know the full name of users and the profile pic of users. 
        To that extent, the profile pic of users is a circle in the navbar that allows the users to logout. This is just to make the website seem cleaner and remind users to sign in. 
    2. THE MAIN PAGE
        At some point, I needed to send a request to the google maps API to find the location of a user. This request takes a while though (and if I send too many I have to pay for them) so it seems bad if this request is constently being sent because the website would be slow and expensive. 
        Thus, I thought it would be smart if it just gets your location when you login. This is the point of the "/" page. It is sendign a request to get your location and saving it. 
        The reason I made the page autorefresh is that I didn't want a user to click off before the API finished getting their location. The page autorefreshes as soon as the API is done. 
        Note that location, much like snapmaps, only works based on the last time you signed into the app. For example, if you were in Berg, signed in, and then left and never reopened the app it would still say you are in berg. This works exactly like SnapMaps becuase legally I can't track your computer otherwise. 
    3. THE "ME" PAGE
        First, I thought it was important to show the user whether the application is publicizing that they are in Berg or not. 
        Second, I realized that sometimes people may want to see who is in Berg but not be seen themselevs (maybe they are avoiding someone). Thus, I made "ghost mode" that allows a user to be perpetually "Not in Berg"
        Finally, I thought it was important to display where the computer thinks the user currently is (in case it is wrong) so I show the map
    4. THE "FRIENDS" PAGE
        Users are automatically friends with "Example Person In Berg" and "Example Person Not In Berg". This is to show them how the app works when they first download it. If they don't like it, they can "remove" them. 
        To begin, users needed to be able to add friends. I wanted this on the same page for ease so we see it at the top. User's search by email so there is no discrepency about nicknames or using first names vs first and last. If the email can't be added for some reason (they are already friends or the user doesn't have an account) feedback is displayed directly on the page saying why. If they can be added, the page autorefreshes
        As with any social media, you want as many people on it as possible. Thus, I thought an "Invite" button would be helpful to get people to invite their friends. This pops up if they insert and email of a friend who doesn't have an account
        I purposefully didn't want users to have to "acceept" friends. This goes against my goals in the MOTIVATION section (it might feel awkward to request the location of someone you don't know well but want to know). Users shoudl feel safe about their data though as you need a harvard email to even access the app. 
        Friends are autosorted so that people "IN BERG" are at top for ease of viewing
        Users can delete friends if they don't care about locations

CODE REFERENCES:
    I used references and tutorials to code some of this. Here are my citations:
    TO MAKE LOGIN WITH GOOGLE in app.py and helpers.py
        https://realpython.com/flask-google-login/ 
    TO RUN GOOGLE MAPS AND GET GEOLOCATION in get_data.html and map.html 
        https://medium.com/future-vision/google-maps-in-python-part-2-393f96196eaf 
        https://www.w3schools.com/graphics/google_maps_basic.asp 
    TO USE AJAX TO SEND THE DATA FROM HTML TO PYTHON in get_data.html and app.py 
         https://dataanalyticsireland.ie/2021/12/13/how-to-pass-a-javascript-variable-to-python-using-json/ 
    TO FORMAT TOGGLE map.html and style.css
        https://www.htmllion.com/css3-toggle-switch-button.html 
    TO AUTOSEND EMAILS in friends.html and app.py
        https://www.geeksforgeeks.org/sending-emails-using-api-in-flask-mail/ 
        https://developers.google.com/gmail/api/guides/sending#python 
    TO GET FAVICON AND LOGO
        https://www.redbubble.com/i/sticker/Annenberg-Harvard-by-claireburst/51967937.EJUG5
