if request.method == "GET":
    data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='/tierlist/boss'")
    return render_template('stlb.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username, nav="ON",
                           power=power, check=0, data=data, link="tierlist/boss")
else:
    # Posting Comment ==============================================================================================
    try:  # We are trying to see if the POST request we got is from inputting a comment.
        var_comment = request.form["comment"]
    except:  # We are not trying to alert the user, so we pass the except.
        pass
    else:
        var_link = "tierlist/boss"  # This is mainly for the search function so that we can link the search result.
        check = post_comments(var_comment, var_link)
        data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='/tierlist/boss'")
        return render_template('stlb.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username,
                               nav="ON", power=power, check=check, data=data, link="tierlist/boss")
    # Deleting Comment =============================================================================================
    try:  # We are trying to see if the POST request we got is from pressing the delete button
        var_comment_id = request.form["delete"]
    except:  # Same with the above, we are just trying to see if this was the option chosen.
        pass
    else:  # This is the code for deleting the chosen item by using its id.
        check = delete_comments(var_comment_id)
        data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='/tierlist/boss'")
        return render_template('stlb.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username,
                               nav="ON", power=power, check=check, data=data, link="tierlist/boss")
    # Editing Comment ==============================================================================================
    try:  # We are trying to see if the POST request we got is from pressing the Edit button
        # While iti s not a good practice to have more than one line here, I need to see if any of the two fails.
        var_edit_id = request.form["editid"]  # This holds the id of the old comment
        var_edit = request.form["edit"]  # This holds the new comment
    except:
        pass
    else:
        check = edit_comments(var_edit_id, var_edit)
        data = getDBdata(openDB(1), "SELECT * FROM comments WHERE link='/tierlist/boss'")
        return render_template('stlb.html', tier0Main=tier0main, tier0Vanguard=tier0vanguard, username=username,
                               nav="ON", power=power, check=check, data=data, link="tierlist/boss")
