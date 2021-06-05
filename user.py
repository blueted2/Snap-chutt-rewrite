ALL_INTERESTS = ["sport", "cinema", "art", "health", "technology", "diy", "cooking", "travel"]


class User:
    def __init__(self, 
    fullName: str = "Test User", 
    age: int = 18, 
    studyYear: int = 2021, 
    studyField: str = "Testing", 
    residence: str = "My Computer", 
    interests: set = set([1, 3, 6])):
        self.__fullName = fullName.title()
        self.age = int(age)
        self.studyYear = int(studyYear)
        self.studyField = studyField
        self.residence = residence
        self.interests = set(interests)
        self.id = -1

        self.following = set()
        self.followers = set()

        self.database = None

    # Quickly get the first letter of the user's name
    @property
    def firstLetter(self):
        return self.fullName[0]

    def follow(self, followingUser):
        if followingUser in self.following: return False
        if self == followingUser: return False
        
        self.following.add(followingUser)
        followingUser.followers.add(self)
        return True

    def unfollow(self, unfollowingUser):
        if unfollowingUser not in self.following: return False
        
        self.following.remove(unfollowingUser)
        unfollowingUser.followers.remove(self)
        return True

    @property
    def fullName(self): return self.__fullName
    
    # We need to use a setter for the fullname, because if the first letter changes, we need to update the user's position within the database dictionary
    @fullName.setter
    def fullName(self, fullName):
        self.database.updateUserDictPositionForNameChange(self, fullName)
        self.__fullName = fullName

    def __repr__(self):
        return f"(id={self.id}, fullName={self.fullName}))"
