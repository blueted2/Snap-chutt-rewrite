"""
This module contains the different menu and sub-menu functions.
"""

from user import User
from userDatabase import UserDatabase
from interface import FLDictToStr, clearAndLogo, clearConsole, inputIntInRange, userListToIdsAndNamesStr, userToIdAndNameStr, userToInfoCardString


## The main menu
#  This function will call other sub-menus based off of what the user enters.
#  @param database The userDatabase.UserDatabase the menu will be running on.
def main_menu(database):
    while True:
        clearAndLogo()

        print(
            "Welcome to the Snapch-UTT!\n"
            "Please choose the function you want to execute:\n"
            "1 - Connect to an existent account\n" # change infos, follow someone, diplay followers, delete the account
            "2 - Search engine\n"  # filters: name, field, year, interests
            "3 - Create an account  \n" 
            "4 - View all users \n"
            "5 - Exit "
            )

        choice = inputIntInRange(1, 6)
        if choice == 1:
            login_menu(database)
        elif choice == 2:
            search_menu(database)
        elif choice == 3:
            new_user_menu(database)
            database.writeFile()
        elif choice == 4:
            view_all_users_menu(database)
        elif choice == 5:
            return

#----LOGGED IN SUB-MENU FUNCTIONS--------------------------------------------------------------
## Menu to ask the user to enter their user id. This will then call loggedIn_menu().
#  @param database The userDatabase.UserDatabase the menu will be running on.
def login_menu(database: UserDatabase):
    clearAndLogo()
    
    print("----USER CONNECT----")
    id = int(input("Enter your accound account ID: "))

    while not id in database.usersById:
        id = int(input("ERROR: User does not exist: "))
    loggedIn_menu(database.getUserFromId(id))

## Sub-menu for functions that require the user to be logged in.
#  @param user The user that is currently logged in.
def loggedIn_menu(user: User):
    while True:
        user.database.writeFile()
        clearAndLogo()
        print("Hello {} (user id: {})".format(user.fullName, user.id))
        print()
        print("----ACCOUNT FUNCTIONS----")
        print(
        "1 - View account information\n"
        "2 - Modify user informations\n"
        "3 - Follow a user\n"
        "4 - Unfollow a user\n"
        "5 - Display all followers\n"
        "6 - Delete your account\n"
        "7 - Log out"
        )

        choice = inputIntInRange(1, 8)

        if choice == 1:
            user_information_menu(user)
        elif choice == 2:
            update_user_menu(user)
            user.database.writeFile()
        elif choice == 3:
            follow_menu(user)
            user.database.writeFile()
        elif choice == 4:
            unfollow_menu(user)
            user.database.writeFile()
        elif choice == 5:
            display_followers_menu(user)
        elif choice == 6:
            delete_account_menu(user)
            user.database.writeFile()
            return
        elif choice == 7:
            return
        

## Display a user's information
#  @param user A user.
def user_information_menu(user: User):
    clearAndLogo()
    print("----USER INFORMATION----")
    print(userToInfoCardString(user))
    input("Press enter to continue")

## Allow the user to update their information.
#  @param user The user whose information will be updated.
def update_user_menu(user: User):
    clearAndLogo()
    print("----UPDATE USER PROFILE----")

    oldFullName     = user.fullName
    oldAge          = user.age
    oldStudyYear    = user.studyYear
    oldStudyField   = user.studyField
    oldResidence    = user.residence
    oldInterestsSet = user.interests

    newFullName        = input(f"Full Name ({oldFullName}): ").title()
    newAgeString       = input(f"Age ({oldAge}): ")
    newStudyYearString = input(f"Study Year ({oldStudyYear}): ")
    newStudyField      = input(f"Study Field ({oldStudyField}): ")
    newResidence       = input(f"Residence ({oldResidence}): ")

    print("  Possible interests: ")
    for i, interest in enumerate(User.ALL_INTERESTS):
        print(f"    {i}. {interest} ")

    interestsString = input(f"Interests ({' '.join([str(i+1) for i in oldInterestsSet])}): ")

    newInterestsSet = set()
    for i in interestsString.split(" "):
        if(i.isnumeric()):
            newInterestsSet.add(int(i))
        
    if newFullName != "":
        user.fullName = newFullName
    if newAgeString != "" and newAgeString.isnumeric():
        user.age = int(newAgeString)
    if newStudyYearString != "" and newStudyYearString.isnumeric():
        user.studyYear = int(newStudyYearString)
    if newStudyField != "":
        user.studyField = newStudyField
    if newResidence != "":
        user.residence = newResidence
    if len(newInterestsSet) != 0:
        user.interests = newInterestsSet
    
## Allow a user to follow another
#  @param user The current user.
def follow_menu(user: User):
    while True:
        clearAndLogo()
        print("----FOLLOW MENU----")
        print("You are currently following: ")
        for u in user.getFollowing():
            print("    ", userToIdAndNameStr(u))

        recomendations = user.database.getRecomendations(user)
        print("Users with lots in common: ")
        for r in recomendations:
            print("    ", userToIdAndNameStr(r))


        choiceString = input("Enter a user's id to follow(empty to exit): ")
        if not choiceString.isnumeric(): return

        choice = int(choiceString)
        followUser = user.database.getUserFromId(choice)

        if followUser is None:
            print("User does not exist")
        else:
            if user.follow(followUser):
                print(f"You have followed {userToIdAndNameStr(followUser)}")    
            else:
                print("Couldn't follow user")
            

        input()

## Allow a user to unfollow another
#  @param The current user.
def unfollow_menu(user: User):
    while True:
        clearAndLogo()
        print("----UNFOLLOW MENU----")
        print("You are currently following: ")
        print("    ", userListToIdsAndNamesStr(user.getFollowing(), seperator= "\n   "))

        choiceString = input("Enter a user's id to unfollow(empty to exit): ")
        if not choiceString.isnumeric(): return

        choice = int(choiceString)
        unfollowUser = user.database.getUserFromId(choice)

        if unfollowUser is None:
            print("User does not exist")
        else:
            if user.unfollow(unfollowUser):
                print(f"You have followed {userToIdAndNameStr(unfollowUser)}")    
            else:
                print("Couldn't unfollow user")

        input()

## Display a given user their followers.
#  @param user The current user
def display_followers_menu(user: User):
    clearAndLogo()
    print("----FOLLOWERS----")
    print(f"You are currently being followed by {len(user.getFollowers())} people")
    for f in user.getFollowers():
        print("    ", userToIdAndNameStr(f))
    
    input("Press enter to continue")

## Allow a user to delete their account(with confirmation).
#  @param user The current user.
def delete_account_menu(user: User):
    clearAndLogo()
    print("----ACCOUNT DELETION----")
    print(f"{user.fullName}, you are about to delete your account.")
    print("This action cannot be undone.")
    answer = input("Enter 'confirm' to confirm that you wish to delete your account: ")
    if answer == "confirm":
        user.database.removeUser(user)
        print("Account deleted!")
    else:
        print("Invalid confirmation, aborting!")
    
    input("Press enter to continue")

#----------------------------------------------------------------------------------------------


## A menu to show the user a list of users. The user can then ask to see more details on a particular user.
#  @param database The database being used for the menu.
#  @param userList A list of users to display.
#  @param prompt Change the default message display before showing the user list.
def userList_menu(database: UserDatabase, userList: list, prompt="User list: "):
    while True:
        clearAndLogo()
        print(prompt)
        print("   ", userListToIdsAndNamesStr(userList, "\n    "))
        choice = input("Enter a user id to view more details, or leave blank to exit: ")
        if choice == "": return

        if choice.isnumeric():
            id = int(choice)
            user = database.getUserFromId(id)
            if user is None:
                print("User does not exist")
                input()
            else:
                user_information_menu(user)
         

## Allow the user to search for users using different fields. Leaving a certain field blank will not use that field for the search.
#  @param database The database being used for the menu.
def search_menu(database: UserDatabase):
    clearAndLogo()
    print("----USER SEARCH----")
    print("Fields can be left blank: ")
    
    name = input("Name: ")
    if (name == ""): name = None

    yearString = input("Study year: ")
    if (yearString == ""): 
        year = None
    else:
        year = int(yearString)

    field = input("Study field: ")
    if (field == ""): field = None

    print("  Possible interests: ")
    for i, interest in enumerate(User.ALL_INTERESTS):
        print(f"    {i}. {interest} ")

    interestsString = input("Intersts:")
    if (name == ""): name = None

    interestsSet = set()
    for i in interestsString.split(" "):
        if(i.isnumeric()):
            interestsSet.add(int(i))

    results = database.searchUsers(name, year, field, interestsSet)

    userList_menu(database, results, "Search results: ")

## Allow the user to input a new user.
#  @param database The database to which the new user will be added.
def new_user_menu(database: UserDatabase):
    clearAndLogo()
    print("----CREATE A NEW USER PROFILE----")
    fullName   =     input("Full Name   : ").title()
    age        = int(input("Age         : "))
    studyYear  = int(input("Study Year  : "))
    studyField =     input("Study Field : ").title()
    residence  =     input("Residence   : ")

    print("  Possible interests: ")
    for i, interest in enumerate(User.ALL_INTERESTS):
        print(f"    {i}. {interest} ")

    interestsString = input("List of interests(by index): ")

    interestsSet = set()
    for i in interestsString.split(" "):
        if i.isnumeric():
            interestsSet.add(int(i))
    
    newUser = User(fullName, age, studyYear, studyField, residence, interestsSet)
    database.addNewUser(newUser)
    print(f"Account created! Welcome to Snap-chutt, {newUser.fullName}")
    print(f"Your id number is: {newUser.id}")
    input()


## View all users by the first letter of their names.
#  @param database The database whose users we want to display.
def view_all_users_menu(database: UserDatabase):
    while True:
        clearConsole() # We don't want to show the logo because the this view already takes up a lot a space
        print("----ALL USERS----")

        print(FLDictToStr(database.usersByFL))

        choice = input("Enter a user id to view more details, or leave blank to exit: ")
        if choice == "": return

        if choice.isnumeric():
            id = int(choice)
            user = database.getUserFromId(id)
            if user is None:
                print("User does not exist")
                input()
            else:
                user_information_menu(user)
