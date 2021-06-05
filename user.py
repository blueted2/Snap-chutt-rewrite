ALL_INTERESTS = ["sport", "cinema", "art", "health", "technology", "diy", "cooking", "travel"]


class User:
    def __init__(self, 
    fullName: str = "Test User", 
    age: int = 18, 
    studyYear: int = 2021, 
    studyField: str = "Testing", 
    residence: str = "My Computer", 
    interests: set = set([1, 3, 6]),
    id = -1,
    following = set(),
    followers = set()):
        self.__fullName = fullName.title()
        self.age = int(age)
        self.studyYear = int(studyYear)
        self.studyField = studyField
        self.residence = residence
        self.interests = set(interests)
        self.id = id
        self.following = following
        self.followers = followers

        self.database = None


    # Quickly get the first letter of the user's name
    @property
    def firstLetter(self):
        return self.fullName[0]

    def follow(self, followingUser):
        if followingUser.id in self.following: return False
        if self == followingUser: return False
        
        self.following.add(followingUser.id)
        followingUser.followers.add(self.id)
        return True

    def unfollow(self, unfollowingUser):
        if unfollowingUser.id not in self.following: return False
        
        self.following.remove(unfollowingUser.id)
        unfollowingUser.followers.remove(self.id)
        return True

    @property
    def fullName(self): return self.__fullName

    def getFollowing(self):
        return [self.database.getUserFromId(id) for id in self.following]

    def getFollowers(self):
        return [self.database.getUserFromId(id) for id in self.followers]
    
    # We need to use a setter for the fullname, because if the first letter changes, we need to update the user's position within the database dictionary
    @fullName.setter
    def fullName(self, fullName):
        self.database.updateUserDictPositionForNameChange(self, fullName)
        self.__fullName = fullName

    def __repr__(self):
        return f"(id={self.id}, fullName={self.fullName}))"

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
        
