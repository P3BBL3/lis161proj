from flask import Flask, request, redirect, url_for, session, render_template
import sqlite3

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'abc123'

# FUNCTION SHORTCUTS ===================================================================================================

# This will make it easier for me to change the path of the database for all parts of the program.
def openDB(db):
    if db == 1:
        conn = sqlite3.connect('users.db')
        return conn
    elif db == 2:
        conn = sqlite3.connect('shiptier.db')
        return conn


# These two functions will be usable for all parts of the code that needs to open the database.
def getDBdata(conn, sql_line):
    cur = conn.cursor()
    cur.execute(sql_line)
    data = cur.fetchall()
    cur.close()
    return data


def saveDBdata(conn, sql_line):
    cur = conn.cursor()
    cur.execute(sql_line)
    conn.commit()
    cur.close()
    return None


# The comment section is available for most pages so I made these three functions to shorten the repeats.
def post_comments(var_comment, var_link):
    var_username = session["username"]
    if var_comment == "":  # If there are no inputs, it will just reload page.
        check = 4
        return check
    else:  # If there are changes, it will edit the comment.
        saveDBdata(openDB(1), "INSERT INTO comments (username,comment,link) VALUES ('" + var_username + "','" + var_comment + "'," + "'" + var_link + "')")
        check = 1
        return check


def edit_comments(var_edit_id, var_edit):
    if var_edit == "":
        check = 4
        return check
    else:
        saveDBdata(openDB(1), "UPDATE comments SET comment='" + var_edit + "' WHERE id='" + var_edit_id + "'")  # Saving the Edit
        check = 2
        return check


def delete_comments(var_comment_id):
    saveDBdata(openDB(1), "DELETE FROM comments WHERE id='" + var_comment_id + "'")  # Saving the Delete
    check = 3
    return check

# MAIN PAGE ============================================================================================================

# Route to the main page
# I have two sessions, username and power (user privilege)
@app.route('/', defaults={"username":"User","power":"2"})
@app.route('/<username>,<power>', methods=['POST', 'GET'])
def index(username, power):
    #These if statement ensures that whenever I go back to home, my session wouldn't be rewritten by the default values.
    if session.get("username") is None or session.get("username") == "User":
        session["username"] = username
    if session.get("power") is None or session.get("power") == "2":
        session["power"] = power
    #nav="ON/OFF" will show in most route. This is just so a certain part of the nav wouldn't appear where nav="OFF"
    return render_template('home.html', username=session["username"], nav="ON", power=session["power"])

# Main Content (1/4) ===================================================================================================

# Route to the tier list
@app.route('/tierlist', methods=['POST', 'GET'])
def tierlist():
    # Saves the session for this route.
    username = session["username"]
    power = session["power"]
    link = "tierlist"
    # This takes data from tables tier0Main and tier0Vanguard with openDB(2) or shiptier.db
    tier0main = getDBdata(openDB(2), 'SELECT * FROM tier0Main')
    tier0vanguard = getDBdata(openDB(2), 'SELECT * FROM tier0Vanguard')
    # This renders the stlo template while passing values received from database, the session values and the nav value.
    if request.method == "GET":
        data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
        return render_template('stlo.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username, nav="ON", power=power, check=0, data=data, link=link)
    else:
        # Posting Comment ==============================================================================================
        try:  # We are trying to see if the POST request we got is from inputting a comment.
            var_comment = request.form["comment"]
        except:  # We are not trying to alert the user, so we pass the except.
            pass
        else:
            check = post_comments(var_comment, link)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('stlo.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username, nav="ON", power=power, check=check, data=data, link=link)
        # Deleting Comment =============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the delete button
            var_comment_id = request.form["delete"]
        except:  # Same with the above, we are just trying to see if this was the option chosen.
            pass
        else:  # This is the code for deleting the chosen item by using its id.
            check = delete_comments(var_comment_id)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('stlo.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username, nav="ON", power=power, check=check, data=data, link=link)
        # Editing Comment ==============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the Edit button
            # While iti s not a good practice to have more than one line here, I need to see if any of the two fails.
            var_edit_id = request.form["editid"]  # This holds the id of the old comment
            var_edit = request.form["edit"]  # This holds the new comment
        except:
            pass
        else:
            check = edit_comments(var_edit_id, var_edit)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('stlo.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username, nav="ON", power=power, check=check, data=data, link=link)

# Route to the tier list for boss battles (NOT YET DONE Database-wise)
@app.route('/tierlist/boss', methods=['POST', 'GET'])
def tierlistboss():
    # Saves the session for this route.
    username = session["username"]
    power = session["power"]
    link = "tierlistboss"
    # This takes data from tables tier0Main and tier0Vanguard with openDB(2) or shiptier.db
    tier0main = getDBdata(openDB(2), 'SELECT * FROM tier0Main')
    tier0vanguard = getDBdata(openDB(2), 'SELECT * FROM tier0Vanguard')
    # This renders the stlo template while passing values received from database, the session values and the nav value.
    if request.method == "GET":
        data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
        return render_template('stlb.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username, nav="ON", power=power, check=0, data=data, link=link)
    else:
        # Posting Comment ==============================================================================================
        try:  # We are trying to see if the POST request we got is from inputting a comment.
            var_comment = request.form["comment"]
        except:  # We are not trying to alert the user, so we pass the except.
            pass
        else:
            check = post_comments(var_comment, link)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('stlb.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username, nav="ON", power=power, check=check, data=data, link=link)
        # Deleting Comment =============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the delete button
            var_comment_id = request.form["delete"]
        except:  # Same with the above, we are just trying to see if this was the option chosen.
            pass
        else:  # This is the code for deleting the chosen item by using its id.
            check = delete_comments(var_comment_id)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('stlb.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username, nav="ON", power=power, check=check, data=data, link=link)
        # Editing Comment ==============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the Edit button
            # While iti s not a good practice to have more than one line here, I need to see if any of the two fails.
            var_edit_id = request.form["editid"]  # This holds the id of the old comment
            var_edit = request.form["edit"]  # This holds the new comment
        except:
            pass
        else:
            check = edit_comments(var_edit_id, var_edit)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('stlb.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username, nav="ON", power=power, check=check, data=data, link=link)


# Route to the tier list for mob battles (NOT YET DONE Database-wise)
@app.route('/tierlist/mobs', methods=['POST', 'GET'])
def tierlistmob():
    # Saves the session for this route.
    username = session["username"]
    power = session["power"]
    link = "tierlistmob"
    # This takes data from tables tier0Main and tier0Vanguard with openDB(2) or shiptier.db
    tier0main = getDBdata(openDB(2), 'SELECT * FROM tier0Main')
    tier0vanguard = getDBdata(openDB(2), 'SELECT * FROM tier0Vanguard')
    # This renders the stlo template while passing values received from database, the session values and the nav value.
    if request.method == "GET":
        data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
        return render_template('stlm.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username,
                               nav="ON", power=power, check=0, data=data, link=link)
    else:
        # Posting Comment ==============================================================================================
        try:  # We are trying to see if the POST request we got is from inputting a comment.
            var_comment = request.form["comment"]
        except:  # We are not trying to alert the user, so we pass the except.
            pass
        else:
            check = post_comments(var_comment, link)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('stlm.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username,
                                   nav="ON", power=power, check=check, data=data, link=link)
        # Deleting Comment =============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the delete button
            var_comment_id = request.form["delete"]
        except:  # Same with the above, we are just trying to see if this was the option chosen.
            pass
        else:  # This is the code for deleting the chosen item by using its id.
            check = delete_comments(var_comment_id)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('stlm.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username,
                                   nav="ON", power=power, check=check, data=data, link=link)
        # Editing Comment ==============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the Edit button
            # While iti s not a good practice to have more than one line here, I need to see if any of the two fails.
            var_edit_id = request.form["editid"]  # This holds the id of the old comment
            var_edit = request.form["edit"]  # This holds the new comment
        except:
            pass
        else:
            check = edit_comments(var_edit_id, var_edit)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('stlm.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username,
                                   nav="ON", power=power, check=check, data=data, link=link)


# Main Content (the other 3/4 that is not yet done) ====================================================================
# These three functions are not yet done because of time-constraints ===================================================
# They all have the same template now, saving the session w/in their function, and passing it, with nav value ==========
# Route for recommended pvp compositions
@app.route('/pvpcomp', methods=['POST', 'GET'])
def pvpcomp():
    username = session["username"]
    power = session["power"]
    link = "pvpcomp"
    # GET is for when a user just goes to the page
    if request.method == "GET":
        data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
        return render_template('pvpcomp.html', username=username, nav="ON", power=power, data=data, check=0, link=link)
    # POST is for when a user goes to the page through submitting some kind of form.
    else:
        # Posting Comment ==============================================================================================
        try:  # We are trying to see if the POST request we got is from inputting a comment.
            var_comment = request.form["comment"]
        except:  # We are not trying to alert the user, so we pass the except.
            pass
        else:
            check = post_comments(var_comment, link)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('pvpcomp.html', username=username, nav="ON", power=power, data=data, check=check, link=link)
        # Deleting Comment =============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the delete button
            var_comment_id = request.form["delete"]
        except:  # Same with the above, we are just trying to see if this was the option chosen.
            pass
        else:  # This is the code for deleting the chosen item by using its id.
            check = delete_comments(var_comment_id)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('pvpcomp.html', username=username, nav="ON", power=power, data=data, check=check, link=link)
        # Editing Comment ==============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the Edit button
            # While iti s not a good practice to have more than one line here, I need to see if any of the two fails.
            var_edit_id = request.form["editid"]  # This holds the id of the old comment
            var_edit = request.form["edit"]  # This holds the new comment
        except:
            pass
        else:
            check = edit_comments(var_edit_id,var_edit)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('pvpcomp.html', username=username, nav="ON", power=power, data=data, check=check, link=link)


# Route for recommended equipment load out
@app.route('/eqloadout', methods=['POST', 'GET'])
def eqloadout():
    username = session["username"]
    power = session["power"]
    link = "eqloadout"
    # GET is for when a user just goes to the page
    if request.method == "GET":
        data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
        return render_template('geneq.html', username=username, nav="ON", power=power, data=data, check=0, link=link)
    # POST is for when a user goes to the page through submitting some kind of form.
    else:
        # Posting Comment ==============================================================================================
        try:  # We are trying to see if the POST request we got is from inputting a comment.
            var_comment = request.form["comment"]
        except:  # We are not trying to alert the user, so we pass the except.
            pass
        else:
            check = post_comments(var_comment, link)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('geneq.html', username=username, nav="ON", power=power, data=data, check=check, link=link)
        # Deleting Comment =============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the delete button
            var_comment_id = request.form["delete"]
        except:  # Same with the above, we are just trying to see if this was the option chosen.
            pass
        else:  # This is the code for deleting the chosen item by using its id.
            check = delete_comments(var_comment_id)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('geneq.html', username=username, nav="ON", power=power, data=data, check=check, link=link)
        # Editing Comment ==============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the Edit button
            # While iti s not a good practice to have more than one line here, I need to see if any of the two fails.
            var_edit_id = request.form["editid"]  # This holds the id of the old comment
            var_edit = request.form["edit"]  # This holds the new comment
        except:
            pass
        else:
            check = edit_comments(var_edit_id,var_edit)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('geneq.html', username=username, nav="ON", power=power, data=data, check=check, link=link)


# Route for equipment tier list
@app.route('/eqtierlist', methods=['POST', 'GET'])
def eqtierlist():
    username = session["username"]
    power = session["power"]
    link = "eqtierlist"
    # GET is for when a user just goes to the page
    if request.method == "GET":
        data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
        return render_template('etl.html', username=username, nav="ON", power=power, data=data, check=0, link=link)
    # POST is for when a user goes to the page through submitting some kind of form.
    else:
        # Posting Comment ==============================================================================================
        try:  # We are trying to see if the POST request we got is from inputting a comment.
            var_comment = request.form["comment"]
        except:  # We are not trying to alert the user, so we pass the except.
            pass
        else:
            check = post_comments(var_comment, link)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('etl.html', username=username, nav="ON", power=power, data=data, check=check,
                                   link=link)
        # Deleting Comment =============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the delete button
            var_comment_id = request.form["delete"]
        except:  # Same with the above, we are just trying to see if this was the option chosen.
            pass
        else:  # This is the code for deleting the chosen item by using its id.
            check = delete_comments(var_comment_id)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('etl.html', username=username, nav="ON", power=power, data=data, check=check,
                                   link=link)
        # Editing Comment ==============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the Edit button
            # While iti s not a good practice to have more than one line here, I need to see if any of the two fails.
            var_edit_id = request.form["editid"]  # This holds the id of the old comment
            var_edit = request.form["edit"]  # This holds the new comment
        except:
            pass
        else:
            check = edit_comments(var_edit_id, var_edit)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('etl.html', username=username, nav="ON", power=power, data=data, check=check,
                                   link=link)


# About Page ===========================================================================================================
# Route for the about page
@app.route('/about', methods=['POST', 'GET'])
def about():
    # Standard action of saving session into a local variable within the function
    username = session["username"]
    power = session["power"]
    link = "about"
    # GET is for when a user just goes to the page
    if request.method == "GET":
        data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
        return render_template('about.html', username=username, nav="ON", power=power, data=data, check=0, link=link)
    # POST is for when a user goes to the page through submitting some kind of form.
    else:
        # Posting Comment ==============================================================================================
        try:  # We are trying to see if the POST request we got is from inputting a comment.
            var_comment = request.form["comment"]
        except:  # We are not trying to alert the user, so we pass the except.
            pass
        else:
            check = post_comments(var_comment, link)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('about.html', username=username, nav="ON", power=power, data=data, check=check, link=link)
        # Deleting Comment =============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the delete button
            var_comment_id = request.form["delete"]
        except:  # Same with the above, we are just trying to see if this was the option chosen.
            pass
        else:  # This is the code for deleting the chosen item by using its id.
            check = delete_comments(var_comment_id)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('about.html', username=username, nav="ON", power=power, data=data, check=check, link=link)
        # Editing Comment ==============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the Edit button
            # While iti s not a good practice to have more than one line here, I need to see if any of the two fails.
            var_edit_id = request.form["editid"]  # This holds the id of the old comment
            var_edit = request.form["edit"]  # This holds the new comment
        except:
            pass
        else:
            check = edit_comments(var_edit_id,var_edit)
            data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='" + link + "'")
            return render_template('about.html', username=username, nav="ON", power=power, data=data, check=check, link=link)
# User interaction routes ==============================================================================================

# Route for signin page
@app.route('/signin', methods=['POST', 'GET'])
def signin():
    usercheck = 0  # Checks if the username is valid, = 0 just for initialization
    passcheck = 0 # Checks if the password is valid, = 0 just for initialization
    power = session["power"]  # session
    if request.method == "GET":  # When users enter the signin route through links.
        if power == "0" or power == "1":  # This will prevent registered user and admin in accessing this page.
            return redirect(url_for('index'))
        else:
            return render_template("form.html", check=0, nav="OFF")
    else:  # When users enter their username and password, the form redirects to this route and this else statement
        # catches it. This is so when there are errors in user input, user can easily try again.
        var_username = request.form["username"]
        var_password = request.form["password"]
        data = getDBdata(openDB(1), 'SELECT * FROM user')

        for datum in data:
            if var_username == datum[1]:  # This checks if the input in the form is equal to any of the username in the database.
                usercheck = 1  # It changes usercheck from 0 to 1 for later if statement
                if var_password == datum[2]:  # If the username is correct, check if the password is correct, if so,
                    passcheck = 1  # Change passcheck from 0 to 1 for later if statement
                    power = datum[3]  # And store the power of the user to know their account capabilities.
                else:
                    passcheck = 2  # If the password doesn't match, change passcheck from 0 to 2 for later if statement.

        if usercheck == 1 and passcheck == 1:  # If both user and pass check are 1, then it is a successful log-in
            return redirect(url_for('index', username=var_username, power=power))
        elif usercheck == 1 and passcheck == 2:  # If password is 2, renders the form template and asks for input again.
            return render_template("form.html", check=1, nav="OFF")
        else:  # This is just to catch other instances.
            return render_template("form.html", check=2, nav="OFF")

#Route for signup page
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    power = session["power"]
    if request.method == "GET":  # When user enters the signup route through links.
        if power == "0" or power == "1":  # This will prevent registered user and admin in accessing this page.
            return redirect(url_for('index'))
        else:
            return render_template("signup.html", check=0, nav="OFF")
    else:  # Upon entering value in the form, the form will send the data back to this route to be processed.
        var_username = request.form["username"]
        var_password = request.form["password"]
        data = getDBdata(openDB(1), 'SELECT * FROM user')

        for datum in data:
            if var_username == "" or var_password == "":  # In cases where users doesn't input anything
                return render_template("signup.html", check=1, nav="OFF")
            elif var_username == datum[1] or var_username == "User":  # In cases where user inputs what is already in the database or is the default value
                return render_template("signup.html", check=2, nav="OFF")
            elif (len(var_username) < 5 or len(var_username) > 20) and (len(var_password) < 5 or len(var_password) > 20):  # In cases where username or password is either too short or too long
                return render_template("signup.html", check=3, nav="OFF")
            else:  # If no errors are caught, proceed to insert new user account and redirect to the signin route.
                saveDBdata(openDB(1), "INSERT INTO user (username,password, power) VALUES ('" + var_username + "','" + var_password + "', 1)")
                return render_template("form.html", check=3, nav="OFF")

# Route for user list. This is only available for admins or users with power 0.
@app.route('/users', methods=['POST', 'GET'])
def users():
    # Standard action of saving session into a local variable within the function
    username = session["username"]
    power = session["power"]

    if request.method == "GET":  # When user enters the users route through links.
        if power == "0":  # Stops non-admins from getting in!!!
            data = getDBdata(openDB(1), 'SELECT * FROM user')  # lists all the users
            return render_template("users.html", data=data, username=username, power=power, nav="ON", check=0)
        else:
            return redirect(url_for('index'))
    else:
        # Deleting Users =============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the delete button
            var_edit_id = request.form["delete"]
        except:
            pass
        else:  # This is the code for deleting the chosen item by using its id.
            saveDBdata(openDB(1), "DELETE FROM user WHERE id='" + var_edit_id + "'")  # Saving the Delete
            data = getDBdata(openDB(1), "SELECT * FROM user")  # Loading the table without the deleted data
            return render_template("users.html", data=data, username=username, power=power, nav="ON", check=0)
        # Editing Users ==============================================================================================
        try:  # We are trying to see if the POST request we got is from pressing the Edit button
            # While iti s not a good practice to have more than one line here, I need to see if any  fails.
            var_edit_id = request.form["editid"]  # This holds the id of the old user id
            var_edit_user = request.form["user"]  # This holds the new username
            var_edit_initial_user = request.form["initialuser"]  # This is used to check if the user is changed.
            var_edit_pass = request.form["pass"]  # This holds the new password
            var_edit_power = request.form["power"]  # This holds the new power.
        except:
            pass
        else:
            data = getDBdata(openDB(1), "SELECT * FROM user")

            if var_edit_user != var_edit_initial_user:  # This means the user field has been changed and must be checked for uniqueness
                for datum in data:
                    if var_edit_user == datum[1]:  # This is now checking if there are any similarities, if there are, it will just render the html again but with a warning message.
                        return render_template("users.html", data=data, username=username, power=power, nav="ON", check=4)

            if var_edit_power == "0" or var_edit_power == "1":  #  This checks if 0 or 1 is inputted as they are the only valid inputs.
                if var_edit_user == "" or var_edit_pass == "":  # This checks if no input is given.
                    return render_template("users.html", data=data, username=username, power=power, nav="ON", check=2)
                elif len(var_edit_user) < 5 or len(var_edit_user) > 20 or len(var_edit_pass) < 5 or len(var_edit_pass) > 20:  # This checks for the length of the inputs.
                    return render_template("users.html", data=data, username=username, power=power, nav="ON", check=3)
                else:  # If no error is caught
                    saveDBdata(openDB(1), "UPDATE user SET username='" + var_edit_user + "', password='" + var_edit_pass + "', power='" + var_edit_power + "' WHERE id='" + var_edit_id + "'")  # Saving the Edit
                    data = getDBdata(openDB(1), "SELECT * FROM user")
                    return render_template("users.html", data=data, username=username, power=power, nav="ON", check=5)
            else:  # This happens when neither 0 or 1 is inputted in the power.
                return render_template("users.html", data=data, username=username, power=power, nav="ON", check=1)
# Route for searching function. This is available for all users even guests.
@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == "GET":  # When user enters the users route through links.
        return redirect(url_for('index'))
    else:
        count = 0  # Initialize the value of count. This shows how many database has the keyword chosen.
        var_search = request.form["search"]
        # Standard action of saving session into a local variable within the function
        username = session["username"]
        power = session["power"]
        searchoutput=[]  # Initialize list where tuples will be saved.

        #For Comments#
        # This whole line looks for the keyword in the comments table from the user database.
        data = getDBdata(openDB(1), 'SELECT * FROM comments WHERE comment LIKE "%' + var_search + '%" or username LIKE "%' + var_search + '%" or link LIKE "%' + var_search + '%";')
        for datum in data:
            # (link, username, comment, check if this is a comment line)
            temp_tup = (datum[3],datum[1],datum[2],"comment")  # This arranges the data inside the tuples in a way that is convinient for me when putting them in the html.
            searchoutput.append(temp_tup)  # This puts the tuples into the list
            count += 1  # This counts how many search output there are.
        #For Ship Details#
        data = getDBdata(openDB(2), 'SELECT * FROM tier0Main WHERE ship_id LIKE "%' + var_search + '%" or ship_name LIKE "%' + var_search + '%" or ship_rarity LIKE "%' + var_search + '%" or ship_extra LIKE "%' + var_search + '%" or link LIKE "%' + var_search + '%";')
        data_temp = getDBdata(openDB(2), 'SELECT * FROM tier0Vanguard WHERE ship_id LIKE "%' + var_search + '%" or ship_name LIKE "%' + var_search + '%" or ship_rarity LIKE "%' + var_search + '%" or ship_extra LIKE "%' + var_search + '%" or link LIKE "%' + var_search + '%";')
        data = data + data_temp  # Combined the search result for two tables

        for datum in data:
            temp_tup = (datum[7],datum[2],datum[1],"content",datum[4],datum[6])  # This arranges the data inside the tuples in a way that is convinient for me when putting them in the html.
            searchoutput.append(temp_tup)  # This puts the tuples into the list
            count += 1  # This counts how many search output there are.

        return render_template("search.html",username=username, power=power, nav="ON", data=searchoutput, count=count, search=var_search)

# Route for signout (I am aware that I named them differently.)
@app.route('/logout')
def logout():
    session.pop("username")  # Stops the session for username
    session.pop("power")  # Stops the session for the power of the username
    return redirect(url_for('index'))

# Run App ==============================================================================================================
if __name__ == '__main__':
    app.run()

# git init in the location
# git config --global user.name 'Mark Dumlao'
# git config --global user.email 'markdumlao1234@gmail.com'
# git add <folder>
# git status
# EXTRA: if you want to remove an added file/folder > git rm --cached
# EXTRA: if you want to add all > git add . or git add * (note: *.html means add all that has html)
# EXTRA: if you want a file/folder not to be commited > touch .gitignore
# git commit -m "Comment Here"
# git remote add origin <github repository>.git
# git push -u origin master
