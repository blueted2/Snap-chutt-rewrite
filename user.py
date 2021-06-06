


class User:
    """! The user class.
    This class holds all the attributs which make up a user, as well as some useful methods.
    
    """

    ## A tuple containing the differents interests a user can have.
    ALL_INTERESTS = ("sport", "cinema", "art", "health", "technology", "diy", "cooking", "travel")

    def __init__(self, fullName: str = "Test User", age: int = 18, studyYear: int = 2021, studyField: str = "Testing", residence: str = "My Computer", interests: set = set([1, 3, 6]),id = -1,following = set(),followers = set()):
        """!
        The User class initializer.
        @param fullName The user's full name, which automatically be converted to a title string.
        @param age The user's age.
        @param studyYear The user's year of study.
        @param studyField The user's field of study.
        @param residence The user's residence.
        @param interests The user's intersts, represented by the indices of interests which can be found in \link ALL_INTERESTS \endlink. 
        @param id The user's id. <i>Used when loading a user from file.</i>
        @param following A set of user ids for the users this user is following. <i>Used when loading a user from file.</i>
        @param followers A set of user ids for the users following this user. <i>Used when loading a user from file.</i>

        @return An instance of the User class.
        """
    
        
        self.__fullName = fullName.title()
        ## The user's age.
        self.age = int(age)
        ## The user's year of study.
        self.studyYear = int(studyYear)
        ## The user's field of study.
        self.studyField = studyField
        ## The user's residence.
        self.residence = residence
        ## The user's intersts, represented by the indices of interests which can be found in \link ALL_INTERESTS \endlink
        self.interests = set(interests)
        ## The user's id
        self.id = id
        ## The set of ids for the users this user is following.
        self.following = following
        ## The set of ids for the users following this user.
        self.followers = followers
        ## A reference to the userDatabase.UserDatabase containing this user.
        self.database = None


    ## @return str The first letter of the user's name. 
    @property
    def firstLetter(self):
        return self.fullName[0]

    ## Add the supplied user's id to the this user's following set, and this user's id to the supplied user's followers set.
    #  @param followingUser The user to follow.
    #  @return True if the user was able to follow the supplied user, False if not.
    def follow(self, followingUser)->bool:
        if followingUser.id in self.following: return False
        if self == followingUser: return False
        
        self.following.add(followingUser.id)
        followingUser.followers.add(self.id)
        return True

    ## Does the opposite of follow().
    #  @param unfollowingUser The user to unfollow.
    #  @return True if the user was able to be unfollow, False if not.
    def unfollow(self, unfollowingUser)->bool:
        if unfollowingUser.id not in self.following: return False
        
        self.following.remove(unfollowingUser.id)
        unfollowingUser.followers.remove(self.id)
        return True

    ## A getter method for the user's fullName. 
    #  This is done to prevent the fullName from being directly modified, as this could mess up the dictionary storing the users by the first letter of their name.
    #  @return The user's full name.
    @property
    def fullName(self): return self.__fullName

    ## Get a list of users that this user if following.
    #  @return A list of users.
    def getFollowing(self):
        return [self.database.getUserFromId(id) for id in self.following]

    ## Get a list of users following this user.
    #  @return A list of users.
    def getFollowers(self):
        return [self.database.getUserFromId(id) for id in self.followers]
    
    ## A setter method for the user's fullname.
    #  We need to use a setter for the fullname, because if the first letter changes, we need to update the user's position within the database dictionary
    #  @param fullName The user's fullname.
    @fullName.setter
    def fullName(self, fullName: str):
        self.database.removeUserBeforeNameChange(self);
        self.__fullName = fullName
        self.database.addUserAfterNameChange(self)

    ## A simple string representation of the user.
    #  @return The representation of the user.
    def __repr__(self):
        return f"(id={self.id}, fullName={self.fullName}))"

    ## Convert the User object into a string which can be written to a file.
    #  @return The User object as a file string.
    def toFileString(self):
        result = ""
        result += str(self.id) + "\n"
        result += str(self.fullName) + "\n"
        result += str(self.age) + "\n"
        result += str(self.studyYear) + "\n"
        result += str(self.studyField) + "\n"
        result += str(self.residence) + "\n"
        result += str(list(self.interests)) + "\n"
        result += str(list(self.following)) + "\n"
        result += str(list(self.followers)) + "\n"

        return result

    ## Convert the supplied list of lines (probably obtained from a file) into a new User object.
    #  @param lines A list of lines containing a user's information.
    #  @return A new User object.
    def fileStringListToUser(lines: list):
        id         =  int(lines[0])
        fullName   =      lines[1]
        age        =  int(lines[2])
        studyYear  =  int(lines[3])
        studyField =      lines[4]
        residence  =      lines[5]
        
        interests  = set( [int(i) for i in lines[6][1:-1].split(",") if i!=""] )
        following  = set( [int(i) for i in lines[7][1:-1].split(",") if i!=""] )
        followers  = set( [int(i) for i in lines[8][1:-1].split(",") if i!=""] )

        return User(fullName, age, studyYear, studyField, residence, interests, id, following, followers)
        
