import psycopg2
import time



def f(query):
    global currentUser
    if query[0] == 'createUser':     #first, last name, email address, password, and date of birth,
        if len(query) != 6:
            print("Please enter a First Name, Last Name, email, password, and DOB to create a user")
        else:
            first_name = query[1]
            last_name = query[2]
            email = query[3]
            password = query[4]
            dob = query[5]
            userid = first_name + dob.split('/')[2]
            lastlogin = time.strftime('%Y-%m-%d %H:%M:%S')
            print("Your userid is: " )
            print("User created!")
            insert_query = "insert into profile values ('" + userid + "','" + first_name + "','" + last_name + "','" + email + "','" + password + "','" + dob + "','" + lastlogin + "');"
            cur.execute(insert_query)
            conn.commit()
    elif query[0] == 'login': #userID and password login else make an error message
        if len(query) != 3:
            print("Please enter your userID and password")
        else:
            userID = query[1]
            password = query[2]
            # email = query[3]
            search_query = "select userid, password from profile where LOWER(userid)=LOWER('" + userID + "');"
            cur.execute(search_query)
            rows = cur.fetchall()
            if rows[0][1] == password:
                print("Correct userID and password! Logged in!")
                currentUser = rows[0][0]
            else:
                print("User name or password incorrect.")
            # print(rows[0][1])
            # for row in rows:
            #     print(row)
            # return
    elif query[0] == 'searchForUser': #searchForUser userid fname lname email for substring
        if len(query) != 2:
            print("Please enter the substring you want to search")
        else:
            substring = query[1]

            search_query = "select userid, fname, lname, email from profile where LOWER(userid) LIKE LOWER('%" + substring + "%') OR LOWER(email) LIKE LOWER('%"+ substring +"%') OR LOWER(fname) LIKE LOWER('%" + substring + "%') OR LOWER(lname) LIKE LOWER('%" + substring + "%');"
            cur.execute(search_query)
            rows = cur.fetchall()
            for row in rows:
                print("USERID: " + row[0] + " FULL NAME: " + row[1] + " " + row[2] + " EMAIL: " + row[3])
            # if rows[0][1] == password:
            #     print("Correct userID and password! Logged in!")
            #     currentUser = rows[0][0]
            # else:
            #     print("User name or password incorrect.")
            # print(rows[0][1])
            # for row in rows:
            #     print(row)
            # return
    elif query[0] == 'initiateFriendship': #initiateFriendship userID
        if len(query) != 2:
            print("Please enter the userID of the friend you would like to add")
        else:
            if currentUser is None or currentUser == '':
                print("Please login in first using the \"login\" command")
            else:
                userid = query[1]


                search_query = "select fname, lname from profile where LOWER(userid) LIKE LOWER('%" + userid + "%');"
                cur.execute(search_query)
                rows = cur.fetchall()
                for row in rows:
                    print(" FULL NAME: " + row[0] + " " + row[1])

                message = raw_input("What would you like to say in your request?\n[If you want a default message simply press enter to continue]\n: ")
                if message is None or message == '':
                    message = 'NULL'

                insert_query = "insert into pendingfriends values ('" + currentUser + "','" + userid + "','" + message + "');"
                # print(insert_query)
                try:
                    cur.execute(insert_query)
                    conn.commit()
                    print("Request sent successfully!")
                except Exception,e:
                    print("Request not sent. Error has occurred, please try again.")
                    print(e)



    elif query[0] == 'confirmFriendship':
        # formatted number list of all friend and group requests along with the messages
        # prompt to have # of requests confirmed or denied and any not selected are declined and removed from pendingfriends pendinggroupmemebers
        # give option to confirm or deny all
        # after this move pendingfriends to friends and pendinggroupmemebrs to groupmembers
        if len(query) != 1:
            print("Please enter only the command name \"confirmFriendship\" to see your pending friend requests")
        else:
            if currentUser is None or currentUser == '':
                print("Please login in first using the \"login\" command")
            else:
                print("PENDING FRIEND REQUESTS:\n")
                search_query = "select userid1, message from pendingfriends where LOWER(userid2)=LOWER('" + currentUser + "');"
                cur.execute(search_query)
                rows = cur.fetchall()
                x = 1
                for row in rows:
                    print(str(x) + ". \n")
                    print(" REQUEST FROM: " + row[0] + "\n  MESSAGE:" + row[1] + "\n")
                    x = x + 1

                confirmNumbers = raw_input("What would you like to say in your request?\n[If you want a default message simply press enter to continue]\n: ")
                confirmNumbers = confirmNumbers.split(' ')
                print(str(len(confirmNumbers)) + " is how many you're confirming")
                if len(confirmNumbers) == 1 and confirmNumbers[0] == '':
                    print("Deny all")
                for x in confirmNumbers:
                    print(x + " confirmed")
                # if message is None or message == '':
                #     message = 'NULL'
                #
                # insert_query = "insert into pendingfriends values ('" + currentUser + "','" + userid + "','" + message + "');"
                # # print(insert_query)
                # try:
                #     cur.execute(insert_query)
                #     conn.commit()
                #     print("Request sent successfully!")
                # except:
                #     print("Request not sent. Error has occurred, please try again.")




    else:
        print('Please use a proper command')

try:
    # conn = psycopg2.connect("dbname='Nick_Peter_Project2' user='postgres' ' password='MyPassword'");
    conn = psycopg2.connect(dbname="Nick_Peter_Project2", user="njw275", password="MyPassword", host="m-dclap-p302-csd.abudhabi.nyu.edu")
    print("Success")
    cur = conn.cursor()
    currentUser = ''

    while(1):


        command = raw_input("socnyuad> ")
        commandSplit = command.split(" ");
        # print(commandSplit)
        f(commandSplit)
        # print(query)
        #

except Exception, e:
    print(e)
