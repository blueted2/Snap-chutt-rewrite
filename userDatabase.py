from user import User
from sortedcontainers import SortedList
from sortedcollections import ValueSortedDict
from os import path

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class UserDatabase:
    """!
    This class holds a collection of user.User, and has methods for manipulating these objects.
    """
    ## The UserDatabase initializer.
    #  @param file The file path for the database file.
    #  @return A new UserDatabase instance.
    def __init__(self, file = None):
        
        ## A dictionary of all users in the database, where the keys are the users' ids.
        # 
        self.usersById = dict()

        ## A dictionary of SortedList. The keys are the 26 letters of the alphabet. 
        #  Each SortedList contains all users whose names begin with the corresponding letter, and these lists are setup to sort by the users' full name.
        #  
        self.usersByFL = dict()

        for letter in letters:
            # We are using a SortedList as this will automatically sort list entries using a key when they are added.
            # We do need to be carefull if said key changes, as the list will not automaticaly be resorted. 
            # We have to remove the the user whose name if about to change from the list, change the name, 
            # then re-add it to the appropriate list (which may not be the same one if the first letter changes)
            self.usersByFL[letter] = SortedList(key = lambda user: user.fullName)

        ## The location of the file from which the database will load and/or save its data.
        self.file = file

        ## The id that will be assigned to next added user. This is incremented evertime a new user is added.
        self.currentUserId = 0

        self.loadFile()

    ## Get a user.User reference from a user id.
    #  @param userId A user id.
    #  @return The user corresponding to the user id.
    def getUserFromId(self, userId: int) -> User:
        return self.usersById.get(userId)

    # Private function for directly adding the user, without giving it a new id.
    def __addUser(self, user: User):
        user.database = self
        self.usersById[user.id] = user
        self.usersByFL[user.firstLetter].add(user)

    ## Takes a newly created user, asigns it an id, sets it's database reference to this UserDatabase, and adds it to the required collections.
    #  @param user A newly created user.
    def addNewUser(self, user: User):
        newId = self.currentUserId
        self.currentUserId += 1
        user.id = newId
        self.__addUser(user)
        
        
    
    ## Remove a user from the database.
    #  @param user The user.User to remove.
    #  @return True if the user could be removed, False if not.
    def removeUser(self, user: User) -> bool:
        userId = user.id
        if userId not in self.usersById: return False

        for id in set(user.following):
            user.unfollow(self.getUserFromId(id))
            

        for id in set(user.followers):
            self.getUserFromId(id).unfollow(user)

        self.usersById.pop(userId)
        self.usersByFL[user.firstLetter].remove(user)

        return True

    
    ## Search all the users, using the supplied search parameters, all of which are optionnal.
    #  @param name Name search (partial match).
    #  @param studyYear Year of study search.
    #  @param studyField Field of study search (partial match).
    #  @param interests Set of interests to search for (matches with supersets).
    
    #  @return A list of users matching the supplied search terms.
    def searchUsers(self, name = None, studyYear = None, studyField = None, interests = None):

        matches = []
        for id, user in self.usersById.items():
            if name != None and name.lower() not in user.fullName.lower():
                continue
            if studyYear != None and studyYear != user.studyYear:
                continue
            if studyField != None and studyField.lower() not in user.studyField.lower():
                continue
            if interests != None and not set(interests).issubset(user.interests):
                continue
            
            matches.append(user)

        return matches

    # This function should be symetrical
    def __getRecommendationScore(user1, user2):

        follows_score = 1 + len(user1.following.intersection(user2.following))

        interests_score = 1+ len(user1.interests.intersection(user2.interests))

        return interests_score * follows_score

    ## Get friends/people with common interests for a given user.
    #  @param currentUser The user for whom we are looking for recomendations.
    #  @param n Optionaly number of recomendations to find.
    #  @return A list of recomended users.
    def getRecomendations(self, currentUser, n=5):
        recommendations = ValueSortedDict()
  
        for id, user in self.usersById.items():
            if currentUser == user: continue # Don't want to add self
            if user in currentUser.getFollowing(): continue # Ingnore people already following.

            recommendations[user] = UserDatabase.__getRecommendationScore(currentUser, user)

            if len(recommendations) > n:
                recommendations.popitem[0] # Remove the first one
        
        return list(recommendations.keys())[::-1] # Reverse the list before returning.

    ## Used for when a user wants to change their name. This will remove the user from the "first letter" dictionary. addUserAfterNameChange() MUST be called after the name change.
    #  @param user The user that will have their name changed.
    def removeUserBeforeNameChange(self, user: User):
        self.usersByFL[user.firstLetter].remove(user)


    ## To be used after removeUserBeforeNameChange(). 
    #  @param user The user whose name has just been changed, and who had previously been temporarily removed from the "FL" dictionary.
    def addUserAfterNameChange(self, user: User):
        self.usersByFL[user.firstLetter].add(user)
        
    ## Convert the database into a string which can be written to a file.
    #  @return The database's file string representation.
    def toFileString(self):
        result = ""
        result += str(self.currentUserId) + "\n"
        for user in self.usersById.values():
            result += user.toFileString()
            result += "\n"

        return result
    
    ## Load the contents of the file(supplied during initialization).
    #
    def loadFile(self):
        if not path.isfile(self.file):
            self.writeFile()
        else:
            with open(self.file, "r") as f:
                lines = [ l.strip() for l in f.readlines()]
            
            self.currentUserId = int(lines.pop(0))

            while len(lines) >=9:
                userLines = lines[0:9]
                self.__addUser(User.fileStringListToUser(userLines))
                lines = lines[10:]

    ## Write the current database state to file.
    #
    def writeFile(self):
        with open(self.file, "w") as f:
            f.write(self.toFileString())
        

        