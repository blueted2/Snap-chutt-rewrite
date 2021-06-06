"""
This module contains various functions for displaying to and reading from the console.
"""

from user import User
import logo, os


## Clear the console and display the logo. Used when going into a menu.
def clearAndLogo():
  clearConsole()
  logo.printLogo()

## Clear the console. Works on unix and windows. 
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

## Create a string for display a user's id and name. 
#  @param user The user
#  @return A string containing the user's id and name.
def userToIdAndNameStr(user: User):
    return f"{user.id}.{user.fullName}"

## Create a list of strings containing the users' ids and names. This basically does what userToIdAndNameStr() does but for multiple users.
#  @param userList A list of users
#  @return A list of strings containing the users' ids and names.
def userListToIdsAndNamesList(userList: list):
    return [userToIdAndNameStr(user) for user in userList]

## Create one big string of users' ids and names. In essence this takes what userListToIdsAndNamesList() does and joins it together.
#  @param userList A list of users
#  @param seperator An optional parameter to specify what will be used to join the strings together.
#  @return A big with users' ids and names.
def userListToIdsAndNamesStr(userList: list, seperator = "\n"):
    return seperator.join(userListToIdsAndNamesList(userList))

## Create a string representation of the "first letter" dictionary used in userDatabase.UserDatabase. 
#  @param userDict The FL dictionary
#  @return The string representation of the dictionary.
def FLDictToStr(userDict: dict):
    result = ""
    for letter, userList in userDict.items():
        result += f"{letter}: {userListToIdsAndNamesStr(userList, seperator=' ')}\n"
        
    return result

## Create a string representation/ "info card" for a given user.
#  @param user A user.
#  @return The user's info card.
def userToInfoCardString(user: User):
    result = ""
    result += f"Full name  : {user.fullName}\n"
    result += f"Age        : {user.age}\n"
    result += f"Study Year : {user.studyYear}\n"
    result += f"Study Field: {user.studyField}\n"
    result += f"Residence  : {user.residence}\n"
    interstsString = "Interests  : "
    for n in user.interests:
        interstsString += f"{n}.{User.ALL_INTERESTS[n]} "
    result += interstsString + "\n"

    followingString = "Following  : "
    for u in user.following:
        followingString += f"{userToIdAndNameStr(user.database.getUserFromId(u))} "
    result += followingString + "\n"

    followersString = "Followers  : "
    for u in user.followers:
        followersString += f"{userToIdAndNameStr(user.database.getUserFromId(u))} "
    result += followersString + "\n"

    return result
    

## A utility function for getting and integer from the user. This function will first prompt the user for a choice, and won't return until a valid choice is made.
#  @param start The lowest valid value (more than or equal)
#  @param end The highest valid value + 1 (strictly less than)
#  @param prompt Change the default prompt message
#  @param error Change the default error message
def inputIntInRange(start, end, prompt="Choice: ", error="ERROR: Invalid choice"):
    while True:
        choiceStr = input(prompt)
        if choiceStr.isnumeric():
            choice = int(choiceStr)
            if choice >= start and choice < end:
                return choice
        
        print(error)