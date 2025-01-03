import cs50
    username = cs50.get_string("Enter username: ")
    password = cs50.get_string("Enter password: ")

    db_username = db.execute(
            """
            SELECT "username" FROM "users"
            WHERE "username" = ?;
            """,
            username
        )
    db_password = db.execute(
            """
            SELECT "password" FROM "users"
            WHERE "password" = ?;
            """,
            password
        )
    # So basically the select clause and the db.execute retruns a list, and this is how you access it!
    print(db_username[0]["username"])
    print(db_password[0]["password"])

    # this is formated string:
    print(f'id = {db_username_id[0]["id"]}')
