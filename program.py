import cs50
import sys

# Database
db = cs50.SQL("sqlite:///wallet.db")

# User Welcome
print("-" * 35)
print("Welcome to the SQLite Wallet App!")
print("-" * 35)

# Stating services avaliable
print("Services Available:\n1- Login\n2- Create Account\n3- Exit\n")

# Getting user input for the process
process_number = cs50.get_int("Please Enter Process Number: ")

#-----------------------------------------------------------------------------------------------------------------------
# Login (1)
if process_number == 1:
    # Prompt for username
    username = cs50.get_string("Enter username: ")

    # Check that there's a user with that username in the database so lets get all the usernames in the database
    db_usernames = db.execute(
            """
            SELECT "username" FROM "users";
            """
        )

    # Searching for the username in the list of dictionaries / Boolean value
    # iterating over the dictionary of db_usernames and checking for that username
    found = any(name["username"] == username for name in db_usernames)

    # Exiting if their username was not found.
    if not found:
        print("There is no user with that username..")
        sys.exit()

    # Get that username's id (if found)
    db_username_id = db.execute(
            """
            SELECT "id" FROM "users"
            WHERE "username" = ?;
            """,
            username
        )

    # Store it in a variable for visual (to not be complex)
    user_id = db_username_id[0]["id"]

    # Prompt user for password (if we got through username checking process!)
    password = cs50.get_string("Enter password: ")

    # Get the actual password from the database
    db_password = db.execute(
            """
            SELECT "password" FROM "users"
            WHERE "id" = ?;
            """,
            user_id
        )

    # Store it in a variable for visual (to not be complex), and to be reusable
    database_password = db_password[0]["password"]

    # Now compare the user written password with the actual password to validate login
    if (password != database_password ):
        print("Incorrect Password...")
        sys.exit()
    else:
        print("=" * 35)
        print("\nLogin Successful!\n")
        print("=" * 35)

    #***************************************************************************************************************
    # Let's continue and provide other services If Login was successful!!
    # We have username, user_id, password at our disposal! (will be useful variables)

    # Set its default value to continue in a while loop
    user_choice = 'Y'

    # .upper() to be case insensitive
    # loop will only continue if user enters the letter 'y'
    while user_choice.upper() == "Y":
        # Display Services
        print("-" * 35)
        print("Select one of these services:\n1- Display Wallets\n2- Deposit\n3- Withdraw\n4- Transfer To a User\n5- Add Wallet\n6- Delete Wallet\n7- Change Password\n8- Change Username\n9- DELETE Account\n10- Sign Out")
        print("-" * 35)

        # Prompt user for service number
        service_number = cs50.get_int("Please Enter Service Number: ")

        ##########################################################################################################
        # Display Wallets [1]
        if service_number == 1:
            # Get all user's wallets using his id
            wallets = db.execute(
                """
                SELECT "name", "amount" FROM "wallets"
                WHERE "user_id" = ?;
                """,
                user_id
            )

            # To keep track of the wallet's number while displaying, set a variable and increment it
            number = 1
            print("~" * 35)
            print(f'{username}`s Wallets: \n')

            # Using formated strings in python for displaying of wallet numbers and their amounts!
            for wallet in wallets:
                print(f'WALLET NUMBER {number} NAME: {wallet["name"]}')
                print(f'AMOUNT STORED = ${wallet["amount"]}\n')
                number += 1

            print("~" * 35)

        #########################################################################################################
        # Deposit [2]
        elif service_number == 2:
            # First we will need to know which wallet the user wants to insert into
            wallet_name = cs50.get_string("\nWhich wallet are you doing the deposit on? ")

            # Get all wallets with the user's id
            db_user_wallets = db.execute(
                """
                SELECT "name" FROM "wallets"
                WHERE "user_id" = ?;
                """,
                user_id
            )

            # Iterate to check if that wallet exists
            found = any(wallet["name"] == wallet_name for wallet in db_user_wallets)

            if not found:
                print("~" * 35)
                print("\nThere is no wallet with that name...\n")
                print("~" * 35)
            else:
                # If found lets prompt for the amount
                deposit_amount = cs50.get_float("Deposit amount? $")

                # And apply/ update it on the data base (there are no restrictions in a deposit!)
                db.execute(
                    """
                    UPDATE "wallets"
                    SET "amount" = "amount" + ?
                    WHERE "name" = ?
                    AND "user_id" = ?;
                    """,
                    deposit_amount, wallet_name, user_id
                )
                print("~" * 35)
                print("\nDeposit Successful!\n")
                print("~" * 35)

        #########################################################################################################
        # Withdraw [3]
        elif service_number == 3:
            # You can only withdraw when you enter your password!
            check_password = cs50.get_string("\nTo WITHDRAW, Please enter your password first:  ")

            # If password isn't correct, exit immediatly
            if check_password != password:
                print("~" * 35)
                print("\nIncorrect password...\n")
                print("~" * 35)
            else:
                print("\nCorrect Password!\n")

                # First we will need to know which wallet the user wants to withdraw from
                wallet_name = cs50.get_string("Which wallet are you doing the withdraw from? ")

                # Get all wallets with the user's id
                db_user_wallets = db.execute(
                    """
                    SELECT "name" FROM "wallets"
                    WHERE "user_id" = ?;
                    """,
                    user_id
                )

                # Iterate to check if that wallet exists
                found = any(wallet["name"] == wallet_name for wallet in db_user_wallets)

                if not found:
                    print("~" * 35)
                    print("\nThere is no wallet with that name...\n")
                    print("~" * 35)
                else:
                    # If found lets prompt for the amount
                    withdraw_amount = cs50.get_float("Withdraw amount? $")
                    try:
                        # And apply/ update it on the data base (there are restrictons of column constraint in a withdraw)
                        db.execute(
                            """
                            UPDATE "wallets"
                            SET "amount" = "amount" - ?
                            WHERE "name" = ?
                            AND "user_id" = ?;
                            """,
                            withdraw_amount, wallet_name, user_id
                        )
                        print("~" * 35)
                        print("\nWithdraw Successful!\n")
                        print("~" * 35)

                    # The cs50 libary raises a value error if a constraint like the check("wallet" >= 0 ) is violated! So we try first, except if a valueError is raised!
                    except ValueError:
                        print("~" * 35)
                        print("\nNot enough funds in the wallet...\n")
                        print("~" * 35)

        #########################################################################################################
        # Transfer To a User[4]
        elif service_number == 4:
            # We're gonna use a transaction for ATOMICITY! (Incase anything is Violated / Raises an error)
            db.execute(
                """
                BEGIN TRANSACTION;
                """
            )

            # To begin transfer we'll need to get the user's password again. (As a safety measure)
            check_password = cs50.get_string("To Begin TRANSFER, Please enter your password first:  ")

            # If password isn't correct don't start transfer and ROLLBACK
            if check_password != password:
                print("~" * 35)
                print("\nIncorrect password...\n")
                print("~" * 35)
                db.execute(
                            """
                            ROLLBACK;
                            """
                        )
            else:
                print("\nCorrect Password!\n")

                # So to transfer to a user we'll need to know multiple of things: 1. Which wallet we're doing the transfer from, 2. Amount, 3. User we're transfering to and his id, 4. to_user wallet
                # Let's get the wallet first and check it
                wallet_name = cs50.get_string("Which wallet are you doing the transfer from? ")

                # Get all wallets with the user's id
                db_user_wallets = db.execute(
                    """
                    SELECT "name" FROM "wallets"
                    WHERE "user_id" = ?;
                    """,
                    user_id
                )

                # Iterate to check if that wallet exists
                found = any(wallet["name"] == wallet_name for wallet in db_user_wallets)

                if not found:
                    print("~" * 35)
                    print("\nThere is no wallet with that name...\n")
                    print("~" * 35)
                    db.execute(
                            """
                            ROLLBACK;
                            """
                        )
                else:
                    # If the wallet is valid let's ask for the amount
                    transfer_amount = cs50.get_float("Transfer amount? $")

                    # Then do the same process of the withdraw service
                    try:
                        db.execute(
                            """
                            UPDATE "wallets"
                            SET "amount" = "amount" - ?
                            WHERE "name" = ?
                            AND "user_id" = ?;
                            """,
                            transfer_amount, wallet_name, user_id
                        )
                    except ValueError:
                        # If there are not enough funds we cancel it and ROLLBACK
                        print("~" * 35)
                        print("\nNot enough funds in the wallet...\n\nYou will be signed out.\n")
                        print("~" * 35)

                        # Cancel out the wallet update and sign user out
                        db.execute(
                            """
                            ROLLBACK;
                            """
                        )
                        sys.exit()

                    # After we updated that user's wallet lets ask which user we're transfering to! (Same process as login!)
                    to_username = cs50.get_string("Username of the person we're transferring to? ")

                    # Let's check if that username exists
                    found = any(name["username"] == to_username for name in db_usernames)

                    if not found:
                        print("~" * 35)
                        print("\nThere is no user with that username..\n")
                        print("~" * 35)
                        db.execute(
                            """
                            ROLLBACK;
                            """
                        )
                    else:
                        # Get the user we're transfering to's id using his username
                        db_to_username_id = db.execute(
                                """
                                SELECT "id" FROM "users"
                                WHERE "username" = ?;
                                """,
                                to_username
                            )
                        to_user_id = db_to_username_id[0]["id"]

                        # Now that we have that user's id, let's display his wallets (but without showing the amount) to ask the user which wallet he is transfering to
                        to_wallets = db.execute(
                            """
                            SELECT "name" FROM "wallets"
                            WHERE "user_id" = ?;
                            """,
                            to_user_id
                        )

                        # To keep track of the wallet's number
                        number = 1
                        print("\n")
                        print("~" * 35)
                        print(f'{to_username}`s Wallets: \n')

                        # Using formated strings in python for displaying of wallet numbers and their amounts again! (Done before!)
                        for wallet in to_wallets:
                            print(f'WALLET NUMBER {number} NAME: {wallet["name"]}')
                            number += 1

                        print("~" * 35)

                        # Prompt user which wallet he is transfering to
                        transfer_to_walletName = cs50.get_string("\nWhich wallet are you transferring to? ")

                        # Let's check wallet validation incase he wrote it wrong./ doesn't exist
                        found = any(wallet["name"] == transfer_to_walletName for wallet in to_wallets)

                        if not found:
                            print("~" * 35)
                            print("\nThere is no wallet with that name...\n")
                            print("~" * 35)
                            db.execute(
                            """
                            ROLLBACK;
                            """
                            )
                        else:
                            # Now we let's deposit into that to_user's wallet!
                            # Same process as Deposit.
                            db.execute(
                                """
                                UPDATE "wallets"
                                SET "amount" = "amount" + ?
                                WHERE "name" = ?
                                AND "user_id" = ?;
                                """,
                                transfer_amount, transfer_to_walletName, to_user_id
                            )

                            # If we reached this far in the transaction, then commit!
                            db.execute(
                                """
                                COMMIT;
                                """
                            )
                            print("~" * 35)
                            print("\nTransfer Successful!\n")
                            print("~" * 35)

        #########################################################################################################
        # Add Wallet [5]
        elif service_number == 5:
            wallet_name = cs50.get_string("What would you like to name this wallet? ")
            amount = cs50.get_float("Enter amount stored in the wallet: ")
            db.execute(
                """
                INSERT INTO "wallets"("name", "amount", "user_id")
                VALUES (?, ?, ?);
                """,
                wallet_name, amount, user_id
            )
            print("~" * 35)
            print("\nWallet Created Successfully!\n")
            print("~" * 35)

        ###########################################################################################################
        # Delete Wallet [6]
        elif service_number == 6:
            # Ask user which wallet he'd like to delete
            wallet_name = cs50.get_string("Which wallet would you like to delete? ")

            # Return a list of actual wallets of the user
            db_user_wallets = db.execute (
                """
                SELECT "name" FROM "wallets"
                WHERE "user_id" = ?;
                """,
                user_id
            )

            # Now let's iterate over the actual wallets to check if it actually exists!
            found = any(wallet["name"] == wallet_name for wallet in db_user_wallets)

            # Exiting if the wallet doesn't exist
            if not found:
                print("~" * 35)
                print("\nThere is no wallet with that name...\n")
                print("~" * 35)
            else:
                # To delete the wallet, we have to check the password
                deleteWallet_password = cs50.get_string("To DELETE your wallet, Please enter your password: ")
                if deleteWallet_password != password:
                    print("~" * 90)
                    print("\nWallet will not be deleted and you will be signed out due to an incorrect password...\n")
                    print("~" * 90)
                    sys.exit()

                # If password is correct let's delete the wallet
                db.execute (
                    """
                    DELETE FROM "wallets"
                    WHERE "name" = ?
                    AND "user_id" = ?;
                    """,
                    wallet_name, user_id
                )
                print("~" * 35)
                print("\nWallet Deleted Successfully!\n")
                print("~" * 35)

        ###############################################################################################################
        # Change Password [7]
        elif service_number == 7:
            check_old_password = cs50.get_string("To change password, Please enter your old password: ")

            # If password isn't correct, exit immediatly
            if check_old_password != password:
                print("~" * 50)
                print("\nIncorrect password, You will be signed out...\n")
                print("~" * 50)
                sys.exit()
            else:
                new_password = cs50.get_string("\nCorrect password!\n\nEnter your new password: ")
                # Set the original password to be the new password!
                db.execute(
                    """
                    UPDATE "users"
                    SET "password" = ?
                    WHERE "id" = ?;
                    """,
                    new_password, user_id
                )
                print("~" * 70)
                print("\nPassword changed, To use new password You'll need to sign in again.\n")
                print("~" * 70)
                sys.exit()

        ###############################################################################################################
        # Change username [8] --> Same process as changing password but for username
        elif service_number == 8:
            check_old_password = cs50.get_string("To change username, Please enter your password: ")

            # If password isn't correct, exit immediatly
            if check_old_password != password:
                print("~" * 50)
                print("\nIncorrect password, Username was NOT changed.\n")
                print("~" * 50)
            else:
                new_username = cs50.get_string("\nCorrect password!\n\nEnter your new username: ")
                db.execute(
                    """
                    UPDATE "users"
                    SET "username" = ?
                    WHERE "id" = ?;
                    """,
                    new_username, user_id
                )
                print("~" * 50)
                print("\nUsername changed! You'll need to sign in again.\n")
                print("~" * 50)
                sys.exit()

        #########################################################################################################
        # DELETE account [9]
        elif service_number == 9:
            check_old_password = cs50.get_string("\nTo DELETE Account, Please enter your password: ")

            # If password isn't correct, exit immediatly
            if check_old_password != password:
                print("~" * 35)
                print("\nIncorrect password, You will be signed out.\n")
                print("~" * 35)
                sys.exit()

            user_confirm_delete = cs50.get_string("Are you sure you want to DELETE your Account? (Y/N): ")
            if user_confirm_delete.upper() == "Y":
                db.execute(
                    """
                    DELETE FROM "users"
                    WHERE "id" = ?;
                    """,
                    user_id
                )

                # No need to worry about their wallets, since deletes are cascaded by database design/schema.
                # \u2639\uFE0F'  --> Special value For frown emoji
                print("~" * 35)
                print("\nWe're sorry to see you go... \u2639\uFE0F \n\nAccount has been deleted.\n")
                print("~" * 35)
                sys.exit()
            else:
                print("~" * 35)
                print("\nAccount DELETE process has been cancelled, You'll be signed out.\n")
                print("~" * 35)
                sys.exit()

        ##########################################################################################################
        # Sign Out [10]
        elif service_number == 10:
            print("~" * 35)
            print("\nSigning Out.\n")
            print("~" * 35)
            sys.exit()
        ###########################################################################################################
        # Any other numbers outside of these services: Use program correctly, and now we're at the end of these conditions
        else:
            print("\nUse Program Correctly..\n")
        ###########################################################################################################


        # See if user wishes to continue, to avoid logging in again
        user_choice = cs50.get_string("Do you wish to continue? (Y/N): ")

    # If we're outside of the while loop, exit program
    print("~" * 35)
    print("\nExiting Program.\n")
    print("~" * 35)

#-------------------------------------------------------------------------------------------------------------------
# Create an account (2)
# Duplicates are allowed since accounts are identified with id (may run into problems)
elif process_number == 2:
    username = cs50.get_string("Create username: ")
    password = cs50.get_string("Create password: ")
    db.execute(
    """
    INSERT INTO "users"("username", "password")
    VALUES (?, ?);
    """,
    username, password
    )
    print("~" * 35)
    print("\nAccount has been Created.\n")
    print("~" * 35)

#----------------------------------------------------------------------------------------------------------------------
# Exit Program (3)
elif process_number == 3:
    print("~" * 35)
    print("\nExiting Program.\n")
    print("~" * 35)
    sys.exit()
