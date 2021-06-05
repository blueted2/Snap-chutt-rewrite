from os import dup
from userDatabase import UserDatabase
from user import User, ALL_INTERESTS
import logo, os

def clearAndLogo():
  clearConsole()
  logo.printLogo()

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def userToIdAndNameStr(user: User):
    return f"{user.id}.{user.fullName}"

def userListToIdsAndNamesStr(userList: list, seperator = "\n"):
    return seperator.join([userToIdAndNameStr(user) for user in userList])

def FLDictToStr(userDict: dict):
    result = ""
    for letter, userList in userDict.items():
        result += f"{letter}: {userListToIdsAndNamesStr(userList, seperator=' ')}\n"
        
    return result

def userToInfoCardString(user: User):
    result = ""
    result += f"Full name  : {user.fullName}\n"
    result += f"Age        : {user.age}\n"
    result += f"Study Year : {user.studyYear}\n"
    result += f"Study Field: {user.studyField}\n"
    result += f"Residence  : {user.residence}\n"
    interstsString = "Interests  : "
    for n in user.interests:
        interstsString += f"{n}.{ALL_INTERESTS[n]} "
    result += interstsString + "\n"

    followingString = "Following  : "
    for u in user.following:
        followingString += f"{userToIdAndNameStr(u)} "
    result += followingString + "\n"

    followersString = "Followers  : "
    for u in user.followers:
        followersString += f"{userToIdAndNameStr(u)} "
    result += followersString + "\n"

    return result
    

def inputIntInRange(start, end, prompt="Choice: ", error="ERROR: Invalid choice"):
    while True:
        choiceStr = input(prompt)
        if choiceStr.isnumeric():
            choice = int(choiceStr)
            if choice >= start and choice < end:
                return choice
        
        print(error)