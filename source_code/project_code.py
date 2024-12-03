import subprocess as sp
import pymysql
import pymysql.cursors
from datetime import datetime,timedelta

def insert_data():
    """
    Function to insert data, where user can choose what data to insert.
    """
    try:
        print("Choose what data you want to insert:")
        print("1. Insert Show")
        print("2. Insert Subscription")
        print("3. Insert Actor")
        print("4. Insert Movie")
        print("5. Insert Account")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            insert_show()  # Function to insert a new Show
        elif choice == 2:
            insert_subscription()  # Function to insert a new Subscription
        elif choice == 3:
            insert_actor()
        elif choice == 4:
            insert_movie()
        elif choice == 5:
            insert_account_with_bank_details()
        else:
            print("Invalid choice. Please choose a valid option.")
    except Exception as e:
        print("Error occurred while inserting data:", e)

def update_data():
    """
    Function to update data, where user can choose what data to update.
    """
    try:
        print("Choose what data you want to update:")
        print("1. Update Email of the user")
        print("2. Update ACCount type of an account")

        print("3. Update Bank Account Details")
        print("4. Update Subscription Price in a Country")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            updateemail()  # Function to update a Show
        elif choice == 2:
            update_account_type()  # Function to update Subscription Price
        elif choice == 3:
            updateBankAccountDetailsByEmail()
        elif choice == 4 :
            updateMobileSubscriptionPrice() # Function to update Bank Account Details
        else:
            print("Invalid choice. Please choose a valid option.")
    except Exception as e:
        print("Error occurred while updating data:", e)

def delete_data():
    """
    Function to delete data, where user can choose what data to delete.
    """
    try:
        print("Choose what data you want to delete:")
        print("1. Delete Account")
        print("2. Delete Subscription")
        print("3. Delete a Show")
        print("4. Delete a Movie")
        print("5. Delete a account following")
        print("--------------------------------------")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            deleteAccount()  # Function to delete a Show
        elif choice == 2:
            delete_subscription()  # Function to delete a Subscription
        elif choice == 3:
            delete_show()
        elif choice == 4:
            delete_movie()
        elif choice == 5:
            delete_account_following()
          # Function to delete a Season
        else:
            print("Invalid choice. Please choose a valid option.")
    except Exception as e:
        print("Error occurred while deleting data:", e)

def retrieve_data():
    """
    Function to retrieve data, where user can choose what data to retrieve.
    """
    try:
        print("Selection queries")
        print("1. Subscription Status Report(Number of users with subscriptions that are either inactive or ending soon)")
        print("2. Get Actors and Languages worked in")
        print("3. Get all the movies of a particular genre")
        print("--------------------------------------")
        print("Projection queries")
        print("4. Account who has watched more than 3 movies or shows")
        print("5. Get Content whose avg rating > 8.5")
        print("--------------------------------------")
        print("Agregate queries")
        print("6. Get number of actors for  a particular content")
        print("7. Get account with most followers")
        print("8. Get total hours watched by an account")
        print("--------------------------------------")
        print("Search queries")
        print("9. Get accounts between  birth year 2000 and 2010")
        print("10. Get accounts with name containing 'REDDY'")
        print("--------------------------------------")
        print("Analysis queries")
        print("11. Get USER WRAPPED SUMMARY")
        print("12. Get average rating by country and genre")
        print("--------------------------------------")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            subscription_status_report()
        elif choice == 2:
           get_actors_languages_worked_in()
        elif choice == 3:
            get_movies_by_genre()
        elif choice == 4:
            account_watched_three()
        elif choice == 5:
            get_highly_rated_content()
        elif choice == 6:
            get_number_of_actors_for_content()
        elif choice == 7:
            get_account_with_most_followers()
        elif choice == 8:
            get_total_hours_watched()
        elif choice == 9:
            get_accounts_by_birth_year()
        elif choice == 10:
            get_accounts_by_name()
        elif choice == 11:
            get_user_wrapped_summary()
        elif choice == 12:
            get_average_rating_by_country_and_genre()
        else:
            print("Invalid choice. Please choose a valid option.")
    except Exception as e:
        print("Error occurred while retrieving data:", e)

# -------------------------------------- Helper Functions for Insert --------------------------------------

def insert_show():
    """
    Inserts a new show into the Shows table while also ensuring that the Content table is updated.
    """
    try:
        # Taking inputs for Content details
        title = input("Enter Show Title: ")
        description = input("Enter Show Description: ")
        country_of_origin = input("Enter Country of Origin: ")
        avg_rating = input("Enter Rating (0 to 10): ")  # This rating will be used in both tables

        # Insert query for Content table
        content_query = """
        INSERT INTO Content
            (Title, Description, Country_of_Origin,Avg_Rating)
        VALUES (%s, %s, %s , %s);
        """
        content_values = (
            title,
            description or None,
            country_of_origin or None,
            float(avg_rating) if avg_rating else None
        )

        # Execute insert for Content table
        cur.execute(content_query, content_values)
        con.commit()

        # Get the newly inserted Content_ID (used as Show_ID in Shows table)
        content_id = cur.lastrowid

        # Taking input for the number of seasons
        no_of_seasons = input("Enter Number of Seasons: ")

        # Insert query for Shows table
        show_query = """
        INSERT INTO Shows
            (Show_ID, Ratings, No_of_Seasons)
        VALUES (%s, %s, %s);
        """
        show_values = (
            content_id,
            float(avg_rating) if avg_rating else None,  # Use the same rating as Content table
            int(no_of_seasons) if no_of_seasons else None
        )

        # Execute insert for Shows table
        cur.execute(show_query, show_values)
        con.commit()

        print(f"Show '{title}' inserted successfully with Show_ID: {content_id}.")

    except Exception as e:
        con.rollback()
        print("Error occurred while inserting show data:", e)


def insert_subscription():
    """
    Inserts a subscription entry into the Subscription table and the respective subscription type table,
    ensuring the Account table is properly referenced.
    """
    try:
        # Taking input for Account ID
        email = input("Enter Account email: ").strip()
        account_id = query_account_id_by_email(email)

        # Check if the Account ID exists in the Account table
        account_check_query = "SELECT 1 FROM Account WHERE Account_ID = %s LIMIT 1;"
        cur.execute(account_check_query, (account_id,))
        account_exists = cur.fetchone()

        if not account_exists:
            print(f"Account ID {account_id} does not exist in the Account table.")
            return  # Exit the function if the account does not exist

        # Set the subscription dates using current date
        first_date_of_subscription = datetime.now().strftime("%Y-%m-%d")
        end_of_subscription = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        last_billing_cycle = datetime.now().strftime("%Y-%m-%d")

        # Get subscription status
        status = "Active"

        # Insert into Subscription table without providing SubscriptionID
        subscription_query = """
        INSERT INTO Subscription
            (AccountID, First_Date_of_Subscription, End_of_Subscription, Last_Billing_Cycle, Status)
        VALUES (%s, %s, %s, %s, %s);
        """
        subscription_values = (
            int(account_id),
            first_date_of_subscription,
            end_of_subscription,
            last_billing_cycle,
            status,
        )
        cur.execute(subscription_query, subscription_values)
        con.commit()

        # Get the auto-generated SubscriptionID
        subscription_id = cur.lastrowid  # Get the last inserted ID from the Subscription table

        # Ask for subscription type
        subscription_type = input("Enter Subscription Type (Mobile, Basic, Standard, Premium): ").strip().lower()

        # Insert into the corresponding subscription type table
        if subscription_type == "mobile":
            no_of_devices = 1
            resolution = "480p"
            price = 149.00
        elif subscription_type == "basic":
            no_of_devices = 1
            resolution = "720p"
            price = 199.00
        elif subscription_type == "standard":
            no_of_devices = 2
            resolution = "1080p"
            price = 499.00
        elif subscription_type == "premium":
            no_of_devices = 4
            resolution = "4K"
            price = 599.00
        else:
            print("Invalid subscription type entered.")
            return

        # Insert query for the specific subscription type
        specific_subscription_query = f"""
        INSERT INTO {subscription_type.capitalize()}
            (SubscriptionID, No_of_Devices, Resolution, Price)
        VALUES (%s, %s, %s, %s);
        """
        specific_subscription_values = (
            int(subscription_id),
            no_of_devices,
            resolution,
            price,
        )
        cur.execute(specific_subscription_query, specific_subscription_values)
        con.commit()

        print(f"Subscription with ID {subscription_id} inserted successfully as {subscription_type.capitalize()} subscription.")

    except Exception as e:
        con.rollback()
        print("Error occurred while inserting subscription data:", e)


def insert_movie():
    """
    Inserts new movie details into the Movies table, first ensuring that the Content table is updated.
    """
    try:
        # Taking inputs for Content details
        title = input("Enter Movie Title: ")
        description = input("Enter Movie Description: ")
        country_of_origin = input("Enter Country of Origin: ")
        trailer = input("Enter Movie Trailer path (BLOB data): ")  # Placeholder for BLOB input
        avg_rating = input("Enter Average Rating (0 to 10): ")

        # Insert query for Content table
        content_query = """
        INSERT INTO Content
            (Title, Description, Country_of_Origin, Trailer, Avg_Rating)
        VALUES (%s, %s, %s, %s, %s);
        """
        content_values = (
            title, description, country_of_origin, trailer, float(avg_rating) if avg_rating else None
        )

        # Execute insert for Content table
        cur.execute(content_query, content_values)
        con.commit()

        # Get the newly inserted Content_ID
        content_id = cur.lastrowid  # The last inserted ID in the Content table

        # Taking inputs for Movie details
        release_year = input("Enter Release Year (YYYY): ")
        duration = input("Enter Duration (HH:MM:SS): ")
        movie_file = input("Enter Movie File path (BLOB data): ")  # Placeholder for BLOB input
        ratings = input("Enter Ratings (0 to 10): ")

        # Insert query for Movies table
        movie_query = """
        INSERT INTO Movies
            (Movie_ID, Release_Year, Duration, Movie_File, Ratings)
        VALUES (%s, %s, %s, %s, %s);
        """
        movie_values = (
            content_id, release_year, duration, movie_file, float(ratings) if ratings else None
        )

        # Execute insert for Movies table
        cur.execute(movie_query, movie_values)
        con.commit()

        print("Movie inserted successfully.")

    except Exception as e:
        con.rollback()
        print("Error occurred while inserting movie details:", e)

def insert_account_with_bank_details():
    """
    Inserts a new account into the Account table and ensures Bank Details are inserted or updated.
    """
    try:
        # Taking inputs in the correct order
        name = input("Enter Name (e.g., Charlie Brown): ")
        email = input("Enter Email: ")
        password = input("Enter Password (hashed or plain for demo): ")
        dob = input("Enter Date of Birth (YYYY-MM-DD, optional; leave blank if not applicable): ")
        account_type = input("Enter Account Type (General or Kids): ")
        country = input("Enter Country: ")
        bank_account_no = input("Enter Bank Account Number (leave blank if not linked): ")

        # Automatically get the current date for 'Date_of_First_Access'
        date_of_first_access = datetime.now().strftime('%Y-%m-%d')

        # If bank details are provided, insert into Bank_Details
        if bank_account_no:
            bank_name = input("Enter Bank Name: ")
            bank_branch_code = input("Enter Bank Branch Code: ")

            # Insert/Update query for Bank_Details
            bank_query = """
            INSERT INTO Bank_Details (Bank_Account_No, Bank_Name, Bank_Branch_Code)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE Bank_Name = %s, Bank_Branch_Code = %s;
            """
            bank_values = (bank_account_no, bank_name, bank_branch_code, bank_name, bank_branch_code)
            cur.execute(bank_query, bank_values)

        # Prepare the query for Account table
        account_query = """
        INSERT INTO Account
            (Name, Email, Password, Date_of_Birth, Account_Type, Date_of_First_Access,
            Country,  Bank_Account_No)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        account_values = (
            name, email, password, dob or None, account_type, date_of_first_access,
            country, bank_account_no or None
        )

        # Executing the insert statement for Account table
        cur.execute(account_query, account_values)
        con.commit()

        print("Account inserted successfully.")

    except Exception as e:
        con.rollback()
        print("Error occurred while inserting account data:",e)

def insert_actor():
    """
    Inserts a new actor into the Actor table.
    Actor_ID is auto-incremented and not required as input.
    """
    try:
        # Taking inputs for Actor details
        name = input("Enter Actor Name: ")
        age = input("Enter Actor Age: ")
        country = input("Enter Actor Country: ")

        # Insert query for Actor table
        actor_query = """
        INSERT INTO Actor
            (Name, Age, Country)
        VALUES (%s, %s, %s);
        """
        actor_values = (name, int(age), country)

        # Execute insert for Actor table
        cur.execute(actor_query, actor_values)
        con.commit()

        print("Actor inserted successfully.")

    except Exception as e:
        con.rollback()
        print("Error occurred while inserting actor data:", e)

# -------------------------------------- Helper Functions for Update --------------------------------------

def update_account_type():
    """
    Function to update the email address of a user in the Account table
    """
    try:
        # Get the details for the update
        print("Update account type for an account")
        name = input("Enter Name (e.g., Charlie Brown): ")
        ll = input("new type {General or kids}: ")


        query = """
            UPDATE Account
            SET Account_Type = %s
            WHERE Name = %s ;
        """
        values = (ll, name)

        cur.execute(query, values)
        con.commit()

        if cur.rowcount == 0:
            print("No records updated. Please check the Name .")
        else:
            print(f"Account Type updated successfully for {name}.")

    except Exception as e:
        con.rollback()
        print("Failed to update Account type in the database")
        print(">>>>>>>>>>>>>", e)

    return

def updateemail():
    """
    Function to update the email address of a user in the Account table
    """
    try:
        # Get the details for the update
        print("Update email for an account")
        name = input("Enter Name (e.g., Charlie Brown): ")
        old_email = input("Enter Old Email: ")
        new_email = input("Enter New Email: ")

        query = """
            UPDATE Account
            SET Email = %s
            WHERE Name = %s AND Email = %s;
        """
        values = (new_email, name, old_email)

        cur.execute(query, values)
        con.commit()

        if cur.rowcount == 0:
            print("No records updated. Please check the Name and Old Email.")
        else:
            print(f"Email updated successfully for {name}.")

    except Exception as e:
        con.rollback()
        print("Failed to update email in the database")
        print(">>>>>>>>>>>>>", e)

    return

def updateMobileSubscriptionPrice():
    """
    Function to update the Mobile subscription price for a given country and subscription type.
    """
    try:
        # Taking dynamic input for country and subscription type
        country = input("Enter the country (e.g., India, USA, etc.): ")
        subscription_type = input("Enter the subscription type (Mobile, Standard, Premium): ")
        price = float(input("Enter the new subscription price: "))
        print(f"Updating {subscription_type} subscription price to {price} for country: {country}...")

        # Query with dynamic parameters
        query = f"""
            UPDATE {subscription_type} M
            INNER JOIN Subscription S ON M.SubscriptionID = S.SubscriptionID
            INNER JOIN Account A ON S.AccountID = A.Account_ID
            SET M.Price = %s
            WHERE A.Country LIKE %s;
        """

        # Execute the query with the country parameter
        cur.execute(query, (price, f'{country}%',))  # Using LIKE operator with wildcard

        con.commit()

        if cur.rowcount == 0:
            print("No records updated. Please check the country and subscription type.")
        else:
            print(f"{subscription_type} subscription price updated successfully for country {country}.")

    except Exception as e:
        con.rollback()
        print("Failed to update subscription price in the database")
        print(">>>>>>>>>>>>>", e)

    return


def updateBankAccountDetailsByEmail():
    """
    Function to update the bank account details of a user based on their email.
    """
    try:
        # Input for user email and new bank details
        email = input("Enter the email of the user: ")
        new_bank_account_no = input("Enter the new Bank Account Number: ")
        new_bank_name = input("Enter the new Bank Name: ")
        new_bank_branch_code = input("Enter the new Bank Branch Code: ")

        # print(f"Updating bank account details for user with email {email}...")

        # Step 1: Insert new bank details
        insert_new_bank_details_query = """
            INSERT INTO Bank_Details (Bank_Account_No, Bank_Name, Bank_Branch_Code)
            VALUES (%s, %s, %s);
        """
        cur.execute(insert_new_bank_details_query, (new_bank_account_no, new_bank_name, new_bank_branch_code))
        # print("New bank account details inserted.")

        # Step 2: Get the old bank account number linked to the user
        get_old_bank_account_query = """
            SELECT Bank_Account_No FROM Account WHERE Email = %s;
        """
        cur.execute(get_old_bank_account_query, (email,))
        old_bank_account = cur.fetchone()

        if not old_bank_account or not old_bank_account['Bank_Account_No']:
            print("No existing bank account found for the given email.")
            return
        old_bank_account_no = old_bank_account['Bank_Account_No']

        # Step 3: Update the user's bank account to the new one
        update_account_query = """
            UPDATE Account
            SET Bank_Account_No = %s
            WHERE Email = %s;
        """
        cur.execute(update_account_query, (new_bank_account_no, email))
        # print("Account table updated with the new bank account number.")

        # Step 4: Delete the old bank details
        delete_old_bank_details_query = """
            DELETE FROM Bank_Details
            WHERE Bank_Account_No = %s;
        """
        cur.execute(delete_old_bank_details_query, (old_bank_account_no,))
        # print("Old bank account details deleted successfully.")

        # Commit the transaction
        con.commit()
        print("Bank account details updated successfully.")

    except Exception as e:
        con.rollback()
        print("Failed to update bank account details.")
        print(">>>>>>>>>>>>>", e)

# -------------------------------------- Helper Functions for Delete --------------------------------------
def deleteAccount():
    """
    Function to delete an account based on the provided email ID
    """
    try:
        # Get the email ID for the account to be deleted
        email_id = input("Enter the email ID of the account to delete: ")


        # SQL query to delete the account
        query = "DELETE FROM Account WHERE Email = %s;"
        values = (email_id,)

        # Execute the query
        cur.execute(query, values)
        con.commit()  # Commit the changes to the database

        if cur.rowcount > 0:
            print(f"Account with email ID '{email_id}' has been successfully deleted.")
        else:
            print(f"No account found with email ID '{email_id}'.")

    except Exception as e:
        print("Failed to delete the account.")
        print(">>>>>>>>>>>>>", e)
        con.rollback()  # Rollback changes in case of an error




def delete_subscription():
    """
    Function to delete a subscription based on the provided email ID.
    """
    try:
        # Get the email ID for the account whose subscription is to be deleted
        email_id = input("Enter the email ID of the account to delete the subscription: ")

        # Step 1: Retrieve the Account_ID for the provided email ID
        query_get_account_id = "SELECT Account_ID FROM Account WHERE Email = %s;"
        cur.execute(query_get_account_id, (email_id,))
        account_id = cur.fetchone()
        

        if account_id is None:
            print(f"No account found with email ID '{email_id}'.")
            return
        
        account_id = account_id['Account_ID']  # Extract the Account_ID from the result tuple
        
        

        # Step 2: Delete the subscription for the retrieved Account_ID
        query_delete_subscription = "DELETE FROM Subscription WHERE AccountID = %s;"
        cur.execute(query_delete_subscription, (account_id,))
        con.commit()  # Commit the changes to the database

        if cur.rowcount > 0:
            print(f"Subscription for account with email ID '{email_id}' has been successfully deleted.")
        else:
            print(f"No subscription found for account with email ID '{email_id}'.")

    except Exception as e:
        print("Failed to delete the subscription.")
        print(">>>>>>>>>>>>>", e)
        con.rollback()  # Rollback changes in case of an error

def delete_movie():
    
    """
    Function to delete a movie based on the provided title.
    """
    try:
        # Get the title of the movie to be deleted
        movie_title = input("Enter the title of the movie to delete: ")

        # SQL query to delete the movie
        delete_query = "DELETE FROM Content WHERE Title = %s;"
        cur.execute(delete_query, (movie_title,))
        con.commit()  # Commit the changes to the database

        if cur.rowcount > 0:
            print(f"Movie titled '{movie_title}' has been successfully deleted.")
        else:
            print(f"No movie found with title '{movie_title}'.")

    except Exception as e:
        print("Failed to delete the movie.")
        print(">>>>>>>>>>>>>", e)
        con.rollback()  # Rollback changes in case of an error

def delete_show():
    
    """
    Function to delete a show based on the provided title.
    """
    try:
        # Get the title of the movie to be deleted
        show_title = input("Enter the title of the show to delete: ")

        # SQL query to delete the movie
        delete_query = "DELETE FROM Content WHERE Title = %s;"
        cur.execute(delete_query, (show_title,))
        con.commit()  # Commit the changes to the database

        if cur.rowcount > 0:
            print(f"Movie titled '{show_title}' has been successfully deleted.")
        else:
            print(f"No movie found with title '{show_title}'.")

    except Exception as e:
        print("Failed to delete the movie.")
        print(">>>>>>>>>>>>>", e)
        con.rollback()  # Rollback changes in case of an error


def delete_account_following():
    """
    Function to delete a following relationship based on the email of the following account.
    """
    try:
        account_email = input("Enter your email: ")
        # Get the email of the following account to be deleted
        following_email = input("Enter the email of the following account to delete: ")

        # Fetch the Account_ID of the following account using the email
        fetch_query = "SELECT Account_ID FROM Account WHERE Email = %s;"
        cur.execute(fetch_query, (following_email,))
        result = cur.fetchone()
        # print(result)

        # If no account is found with that email
        if result is None:
            print(f"No account found with email '{following_email}'.")
            return

        following_account_id = result['Account_ID']

        # Get the email of the account performing the deletion (to ensure they have the right to delete the following relationship)
        

        # Fetch the Account_ID of the account performing the deletion
        fetch_query = "SELECT Account_ID FROM Account WHERE Email = %s;"
        cur.execute(fetch_query, (account_email,))
        result = cur.fetchone()

        # If no account is found with that email
        if result is None:
            print(f"No account found with email '{account_email}'.")
            return

        account_id = result['Account_ID']

        # SQL query to delete the following relationship from Account_Following
        delete_query = "DELETE FROM Account_Following WHERE Account_ID = %s AND Following_ID = %s;"
        cur.execute(delete_query, (account_id, following_account_id))
        con.commit()  # Commit the changes to the database

        if cur.rowcount > 0:
            print(f"Following relationship with account '{following_email}' has been successfully deleted.")
        else:
            print(f"No following relationship found for account '{following_email}'.")

    except Exception as e:
        print("Failed to delete the following relationship.")
        print(">>>>>>>>>>>>>", e)
        con.rollback()  # Rollback changes in case of an error



# -------------------------------------- Retrieve section--------------------------------------
def get_accounts_by_name():
    """
    Function to retrieve accounts where the name contains 'REDDY'.
    """
    try:
        # SQL query to get accounts where the name contains 'REDDY'
        query = """
            SELECT 
                Account_ID,
                Name
            FROM 
                Account
            WHERE 
                Name LIKE %s;
        """

        # User input for the name filter
        name_filter = '%REDDY%'  # This can be made dynamic by allowing user input if needed

        # Execute the query with the filter parameter
        cur.execute(query, (name_filter,))
        results = cur.fetchall()

        # Check if any accounts were found
        if results:
            print("Accounts with 'REDDY' in the name:")
            print("-" * 40)
            for row in results:
                print(f"Account ID: {row['Account_ID']}, Name: {row['Name']}")
        else:
            print("No accounts found with 'REDDY' in the name.")
    except Exception as e:
        print("Error occurred while retrieving accounts by name:", e)

def get_accounts_by_birth_year():
    """
    Function to retrieve accounts whose Date_of_Birth is between 2000 and 2010.
    """
    try:
        # SQL query to get accounts where Date_of_Birth is between 2000 and 2010
        query = """
            SELECT 
                Account_ID,
                Name,
                Date_of_Birth
            FROM 
                Account
            WHERE 
                YEAR(Date_of_Birth) BETWEEN 2000 AND 2010;
        """

        # Execute the query
        cur.execute(query)
        results = cur.fetchall()

        # Check if any accounts were found
        if results:
            print("Accounts with Date_of_Birth between 2000 and 2010:")
            print("-" * 40)
            for row in results:
                print(f"Account ID: {row['Account_ID']}, Name: {row['Name']}, Date of Birth: {row['Date_of_Birth']}")
        else:
            print("No accounts found with Date_of_Birth between 2000 and 2010.")
    except Exception as e:
        print("Error occurred while retrieving accounts by birth year:", e)
def get_total_hours_watched():
    """
    Function to get the total number of hours watched by a specific account.
    """
    try:
        # Get the account ID input from the user
        email = input("Enter the Account email to get total hours watched: ")
        account_id=query_account_id_by_email(email)
        # SQL query to sum the hours of movies watched by the specified account
        query = """
        SELECT SUM(HOUR(Duration_Watched)) AS Total_Hours_Watched
        FROM Account_Watch_History
        WHERE Account_ID = %s;
        """
        
        # Execute the query with the user input (account_id)
        cur.execute(query, (account_id,))

        # Fetch the result
        result = cur.fetchone()

        if result and result['Total_Hours_Watched'] is not None:
            print(f"Total hours watched by Account ID {account_id}: {result['Total_Hours_Watched']} hours")
        else:
            print(f"No data found for Account ID {account_id} or no hours watched.")
        print("-" * 40)
    except Exception as e:
        print("An error occurred while retrieving the total hours watched.")
        print(">>>>>>>>>>>>>", e)
def get_movies_by_genre():
    """
    Function to get all the movies based on the provided genre.
    """
    try:
        # Get the genre input from the user
        genre = input("Enter the genre of movies you want to search: ")

        # SQL query to get the movies of the specified genre
        query = """
        SELECT c.Title, c.Description, c.Country_of_Origin, m.Release_Year, m.Duration, m.Ratings
        FROM Content c
        JOIN Movies m ON c.Content_ID = m.Movie_ID
        JOIN Content_Genre cg ON c.Content_ID = cg.Content_ID
        WHERE cg.Content_Genre = %s;
        """
        
        # Execute the query with the user input
        cur.execute(query, (genre,))

        # Fetch all results
        movies = cur.fetchall()
        #print(movies)

        if movies:
            print(f"Movies in the genre '{genre}':")
            for movie in movies:
                print(f"Title: {movie['Title']}, Description: {movie['Description']}, Country: {movie['Country_of_Origin']}, Year: {movie['Release_Year']}, Duration: {movie['Duration']}, Rating: {movie['Ratings']}")
        else:
            print(f"No movies found in the genre '{genre}'.")

    except Exception as e:
        print("An error occurred while retrieving movies.")
        print(">>>>>>>>>>>>>", e)
def subscription_status_report():
    """
    Function to get the number of users with subscriptions that are either inactive or ending soon (within 10 days)
    and print the subscription status along with the number of users in each status.
    """
    try:
        # SQL query to get the subscription status and number of users
        query = """
        SELECT 
            CASE
                WHEN S.Status = 'Inactive' THEN 'Inactive'
                WHEN S.End_of_Subscription <= DATE_ADD(CURDATE(), INTERVAL 10 DAY) THEN 'Ending Soon'
            END AS Subscription_Status,
            COUNT(DISTINCT A.Account_ID) AS No_of_Users
        FROM Account A
        JOIN Subscription S ON A.Account_ID = S.AccountID
        WHERE S.Status = 'Inactive'
           OR S.End_of_Subscription <= DATE_ADD(CURDATE(), INTERVAL 10 DAY)
        GROUP BY Subscription_Status
        """
        
        # Execute the query
        cur.execute(query)

        # Fetch all the results
        results = cur.fetchall()

        if results:
            print("Subscription Status Report:")
            print("-" * 40)
            for row in results:
                print(f"Subscription Status: {row['Subscription_Status']}, Number of Users: {row['No_of_Users']}")
            print("-" * 40)
        else:
            print("No data found for the given criteria.")
    
    except Exception as e:
        print("Failed to retrieve the data.")
        print(">>>>>>>>>>>>>", e)
def get_account_with_most_followers():
    """
    Function to retrieve the account with the highest number of followers.
    """
    try:
        # SQL query to get the account with the most followers
        query = """
            SELECT 
                a.Account_ID,
                a.Name,
                COUNT(af.Follower_ID) AS Number_of_Followers
            FROM 
                Account a
            JOIN 
                Account_Followers af ON a.Account_ID = af.Account_ID
            GROUP BY 
                a.Account_ID
            ORDER BY 
                Number_of_Followers DESC
            LIMIT 1;
        """

        # Execute the query
        cur.execute(query)
        result = cur.fetchone()

        # Check if a result was returned
        if result:
            print(f"Account with Most Followers:")
            print(f"Account ID: {result['Account_ID']}")
            print(f"Name: {result['Name']}")
            print(f"Number of Followers: {result['Number_of_Followers']}")
        else:
            print("No accounts found with followers.")
    except Exception as e:
        print("Error occurred while retrieving account with most followers:", e)
def query_account_id_by_email(email):
  
    query = "SELECT Account_ID FROM Account WHERE Email = %s;"
    cur.execute(query, (email,))
    result = cur.fetchone()
    # print(result)
    return result['Account_ID'] if result else None
def query_user_name_by_email(email):
   
    query = "SELECT Name FROM Account WHERE Email = %s;"
    cur.execute(query, (email,))
    result = cur.fetchone()
    # print(result)
    return result['Name'] if result else None
def query_total_watch_time(account_id):
    query = """
        SELECT SUM(Duration_Watched) AS Total_Time_Watched
        FROM Account_Watch_History
        WHERE Account_ID = %s;
    """
    cur.execute(query, (account_id,))
    result = cur.fetchone()
    # print(result)
    return float(result['Total_Time_Watched']) if result else 0
def query_most_watched_content(account_id):
    query = """
        SELECT c.Title, SUM(wh.Duration_Watched) AS Total_Watch_Time
        FROM Account_Watch_History wh
        JOIN Content c ON wh.Watched_Content_ID = c.Content_ID
        WHERE wh.Account_ID = %s
        GROUP BY c.Title
        ORDER BY Total_Watch_Time DESC
        LIMIT 5;
    """
    cur.execute(query, (account_id,))
    results = cur.fetchall()
    # print(results)
    return [{"title": row['Title'], "time_watched": row['Total_Watch_Time']} for row in results]
def query_top_genres(account_id):
    query = """
        SELECT cg.Content_Genre, COUNT(*) AS Genre_Count
        FROM Account_Watch_History wh
        JOIN Content_Genre cg ON wh.Watched_Content_ID = cg.Content_ID
        WHERE wh.Account_ID = %s
        GROUP BY cg.Content_Genre
        ORDER BY Genre_Count DESC
        LIMIT 5;
    """
    cur.execute(query, (account_id,))
    results = cur.fetchall()
    return [{"genre": row['Content_Genre'], "count": row['Genre_Count']} for row in results]
def query_total_reviews(account_id):
    query = """
        SELECT COUNT(Review_ID) AS Number_of_Reviews
        FROM Review
        WHERE Account_ID = %s;
    """
    cur.execute(query, (account_id,))
    result = cur.fetchone()
  
    return result['Number_of_Reviews'] if result else 0
def query_most_liked_content(account_id):
    query = """
        SELECT c.Title, COUNT(al.Liked_Content_ID) AS Liked_Count
        FROM Account_Likes al
        JOIN Content c ON al.Liked_Content_ID = c.Content_ID
        WHERE al.Account_ID = %s
        GROUP BY c.Title
        ORDER BY Liked_Count DESC
        LIMIT 5;
    """
    cur.execute(query, (account_id,))
    results = cur.fetchall()

    return [{"title": row['Title'], "likes_count": row['Liked_Count']} for row in results]

def query_watch_history_over_time(account_id):
    query = """
        SELECT MONTH(wh.Date_of_Watch_Start) AS Watch_Month,
               YEAR(wh.Date_of_Watch_Start) AS Watch_Year,
               SUM(wh.Duration_Watched) AS Total_Monthly_Watch_Time
        FROM Account_Watch_History wh
        WHERE wh.Account_ID = %s
        GROUP BY Watch_Year, Watch_Month
        ORDER BY Watch_Year DESC, Watch_Month DESC;
    """
    cur.execute(query, (account_id,))
    results = cur.fetchall()
    # print(results)
    return [{"year": row['Watch_Month'], "month": row['Watch_Year'], "watch_time": row['Total_Monthly_Watch_Time']} for row in results]
def get_user_wrapped_summary():
    """
    Function to retrieve a detailed summary of a user's activity using their email.
    The summary includes total watch time, most watched content, favorite genres,
    reviews given, liked content, and watch history over time.
    """
    try:
        email=(input("Enter email: "))

        # Step 1: Retrieve Account_ID using the provided email
        account_id = query_account_id_by_email(email)
        user_name = query_user_name_by_email(email)
        if not account_id:
            print("Account with this email does not exist.")
            return
        
        # Step 2: Retrieve additional information using the Account_ID
    # Replace with logic to fetch the user's name if needed
        total_watch_time = query_total_watch_time(account_id)
        most_watched_content = query_most_watched_content(account_id)
        favorite_genres = query_top_genres(account_id)
        total_reviews = query_total_reviews(account_id)
        most_liked_content = query_most_liked_content(account_id)
        watch_history = query_watch_history_over_time(account_id)

        # Step 3: Organize and display the summary
        print("\nUser Wrapped Summary:")
        print("-" * 40)
        print(f"User: {user_name}")
        print(f"Total Watch Time: {total_watch_time} minutes")
        print("\nMost Watched Content:")
        for content in most_watched_content:
            print(f"Title: {content['title']}, Time Watched: {content['time_watched']} minutes")
        
        print("\nTop 5 Favorite Genres:")
        for genre in favorite_genres:
            print(f"Genre: {genre['genre']} , Watched Count: {genre['count']}")
        
        print(f"\nTotal Reviews Given: {total_reviews}")
        
        print("\nMost Liked Content:")
        for content in most_liked_content:
            print(f"Title: {content['title']}, Likes: {content['likes_count']}")
        
        print("\nWatch History Over Time (Past Year):")
        for history in watch_history:
            print(f"Month: {history['year']}, Year: {history['month']}, Total Watch Time: {history['watch_time']} minutes")
        print("-" * 40)
    except Exception as e:
        print("Error occurred while retrieving user wrapped summary:", e)

 #No of account that have watched more than 3 movies
def account_watched_three():
    """
    Function to get the number of accounts that have watched more than 3 movies
    and print the account IDs.
    """
    try:
        # SQL query to get the account IDs that have watched more than 3 movies
        query = """
        SELECT Account_ID
        FROM Account_Watch_History
        GROUP BY Account_ID
        HAVING COUNT(Watched_Content_ID) > 3
        """
        
        # Execute the query
        cur.execute(query)

        # Fetch all the results
        results = cur.fetchall()

        if results:
            print(f"Number of accounts that have watched more than 3 movies: {len(results)}")
            print("Account IDs are as follows:")
            for account in results:
                print(account['Account_ID'])  # Each account is a tuple, so we access the first element
        else:
            print("No accounts have watched more than 3 movies.")
    
    except Exception as e:
        print("Failed to retrieve the data.")
        print(">>>>>>>>>>>>>",e)
def get_average_rating_by_country_and_genre():
    """
    Function to retrieve the average ratings of content grouped by country of origin and genre.
    The result is ordered by country of origin and average rating in descending order.
    """
    try:
        # SQL query to retrieve country, genre, and average rating
        query = """
            SELECT 
                c.Country_of_Origin AS Country,
                cg.Content_Genre AS Genre,
                ROUND(AVG(r.Rating), 2) AS Average_Rating
            FROM 
                Content c
            JOIN 
                Review r ON c.Content_ID = r.Content_ID
            JOIN 
                Content_Genre cg ON c.Content_ID = cg.Content_ID
            GROUP BY 
                c.Country_of_Origin, cg.Content_Genre
            ORDER BY 
                c.Country_of_Origin, Average_Rating DESC;
        """
        
        # Execute the query
        cur.execute(query)
        results = cur.fetchall()

        if results:
            print("\nAverage Ratings by Country and Genre:")
            print("-" * 50)
            for row in results:
                country = row['Country']
                genre = row['Genre']
                avg_rating = row['Average_Rating']
                print(f"Country: {country}, Genre: {genre}, Average Rating: {avg_rating}")
        else:
            print("No results found.")
    except Exception as e:
        print("Error occurred while retrieving average ratings by country and genre:", e)

def get_number_of_actors_for_content():
    """
    Function to retrieve the number of actors associated with a given content title.
    The content title is taken as input from the user.
    """
    try:
        # Ask user for the content title
        content_title = input("Enter the title of the content: ")

        # SQL query to get the number of actors for the given content title
        query = """
            SELECT 
                c.Title,
                COUNT(ca.Actor_ID) AS Number_of_Actors
            FROM 
                Content c
            JOIN 
                Content_Actor ca ON c.Content_ID = ca.Content_ID
            WHERE 
                c.Title = %s
            GROUP BY 
                c.Content_ID;
        """
        # Execute the query with the user input as parameter
        cur.execute(query, (content_title,))
        result = cur.fetchone()

        # Check if a result was returned
        if result:
            print(f"Content: {result['Title']}")
            print(f"Number of Actors: {result['Number_of_Actors']}")
        else:
            print(f"No actors found for content titled '{content_title}'. Please check the title and try again.")
    except Exception as e:
        print("Error occurred while retrieving the number of actors for the content:", e)

def get_highly_rated_content():
    """
    Function to retrieve the titles of content with average ratings greater than 8.5.
    The result is ordered by average rating in descending order.
    """
    try:
        # SQL query to retrieve content titles and average ratings where the average rating is > 8.5
        query = """
            SELECT 
                c.Title,
                ROUND(AVG(r.Rating), 2) AS Avg_Rating
            FROM 
                Content c
            JOIN 
                Review r ON c.Content_ID = r.Content_ID
            GROUP BY 
                c.Content_ID
            HAVING 
                AVG(r.Rating) > 8.5
            ORDER BY 
                Avg_Rating DESC;
        """

        # Execute the query
        cur.execute(query)
        results = cur.fetchall()

        if results:
            print("\nHighly Rated Content (Avg Rating > 8.5):")
            print("-" * 50)
            for row in results:
                title = row['Title']
                avg_rating = row['Avg_Rating']
                print(f"Title: {title}, Average Rating: {avg_rating}")
        else:
            print("No highly rated content found.")
    except Exception as e:
        print("Error occurred while retrieving highly rated content:", e)
    
def get_actors_languages_worked_in():
    """
    Function to retrieve the actor names along with the languages they have worked in.
    """
    try:
        # Query to retrieve actor names and the languages they have worked in
        query = """
            SELECT 
                A.Name AS Actor_Name,
                GROUP_CONCAT(DISTINCT C.Content_Language ORDER BY C.Content_Language) AS Languages_Worked_In
            FROM Actor A
            JOIN Content_Actor CA ON A.Actor_ID = CA.Actor_ID
            JOIN Content_Languages C ON CA.Content_ID = C.Content_ID
            GROUP BY A.Actor_ID;
        """

        # Execute the query
        cur.execute(query)
        results = cur.fetchall()

        if results:
            print("\nActors and the Languages they have worked in:")
            print("-" * 50)
            for row in results:
                actor_name = row['Actor_Name']
                languages_worked_in = row['Languages_Worked_In']
                print(f"Actor: {actor_name}, Languages Worked In: {languages_worked_in}")
        else:
            print("No data found.")
    except Exception as e:
        print("Error occurred while retrieving actor and language data:", e)

def getTop10ShowsWatchedByFollowed():
    """
    Function to list the top 10 shows watched by the people you follow
    """
    try:
        # Get the details for the query
        print("Top 10 Shows Watched by the People You Follow")
        account_id = (input("Enter your Email: "))

        query = """
            SELECT 
                S.Show_ID, 
                C.Title, 
                COUNT(W.Content_ID) AS WatchCount
            FROM 
                Account_Following AF
            JOIN 
                WatchList W ON AF.Following_ID = W.AccountID
            JOIN 
                Content C ON W.Content_ID = C.Content_ID
            JOIN 
                Shows S ON C.Content_ID = S.Show_ID
            WHERE 
                AF.Email = %s
            GROUP BY 
                S.Show_ID, C.Title
            ORDER BY 
                WatchCount DESC
            LIMIT 10;
        """
        values = (account_id,)

        cur.execute(query, values)
        results = cur.fetchall()

        if not results:
            print("No shows found for the people you follow.")
        else:
            print("\nTop 10 Shows:")
            print("-" * 40)
            for row in results:
                show_id, title, watch_count = row
                print(f"Show ID: {show_id}, Title: {title}, Watch Count: {watch_count}")

    except Exception as e:
        print("Failed to retrieve the top 10 shows.")
        print(">>>>>>>>>>>>>", e)

    return
# -------------------------------------- Main Menu --------------------------------------

def dispatch(ch):
    """
    Function that maps helper functions to options entered
    """
    if ch == 1:
        insert_data()  # Let the user choose what data to insert
    elif ch == 2:
        update_data()  # Let the user choose what data to update
    elif ch == 3:
        delete_data() 
    elif ch == 4:
        retrieve_data() # Let the user choose what data to delete
    elif ch == 5:
        exit()

# Global
while True:
    tmp = sp.call('cls', shell=True)

    # Hardcoded username and password
    username = "root"
    password = "#R08032005r"

    try:
        # Set db name and credentials accordingly
        con = pymysql.connect(host='localhost',
                              port=3306,
                              user=username,
                              password=password,
                              db='project',
                              cursorclass=pymysql.cursors.DictCursor)
        tmp = sp.call('cls', shell=True)

        if con.open:
            print("Connected")
        else:
            print("Failed to connect")

        tmp = input("Enter any key to CONTINUE>")

        with con.cursor() as cur:
            while True:
                tmp = sp.call('cls', shell=True)
                # Options for Moviefy database
                print("1. Insert Data")
                print("2. Update Data")
                print("3. Delete Data")
                print("4. Retrieve data")  # Placeholder for another operation
                print("5. Logout")
                ch = int(input("Enter choice> "))
                tmp = sp.call('cls', shell=True)
                if ch == 5:
                    exit()
                else:
                    dispatch(ch)
                    tmp = input("Enter any key to CONTINUE>")

    except Exception as e:
        tmp = sp.call('cls', shell=True)
        print(e)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")