from user import User
from sortedcontainers import SortedList
from sortedcollections import ValueSortedDict

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class UserDatabase:
    def __init__(self):
        self.usersById = dict()
        self.usersByFL = dict()

        for letter in letters:
            self.usersByFL[letter] = SortedList(key = lambda user: user.fullName)

        self.currentUserId = 0

    def getUserFromId(self, userId: int) -> User:
        return self.usersById.get(userId)

    def addUser(self, user: User):
        newId = self.currentUserId
        self.currentUserId += 1

        user.id = newId
        user.database = self
        self.usersById[newId] = user
        self.usersByFL[user.firstLetter].add(user)
        
    
    def removeUser(self, user: User) -> bool:
        userId = user.id
        if userId not in self.usersById: return False

        for id in set(user.following):
            user.unfollow(self.usersById[id])
            

        for id in set(user.followers):
            self.usersById[id].unfollow(user)

        self.usersById.pop(userId)
        self.usersByFL[user.firstLetter].remove(user)
        return True

    def searchUsers(self, name = None, studyYear = None, studyField = None, interests = None):
        matches = []
        for id, user in self.usersById.items():
            if name != None and name.lower() not in user.fullName.lower():
                continue
            if studyYear != None and studyYear != user.studyYear:
                continue
            if studyField != None and studyField != user.studyField:
                continue
            if interests != None and not set(interests).issubset(user.interests):
                continue
            
            matches.append(user)

        return matches

    # This function should be symetrical
    def getRecommendationScore(user1, user2):

        follows_score = 1 + len(user1.following.intersection(user2.following))

        interests_score = 1+ len(user1.interests.intersection(user2.interests))

        return interests_score * follows_score

    def getRecomendations(self, currentUser, n=5):
        recommendations = ValueSortedDict()
  
        for id, user in self.usersById.items():
            if currentUser == user: continue # Don't want to add self
            if user in currentUser.following: continue

            recommendations[user] = UserDatabase.getRecommendationScore(currentUser, user)

            if len(recommendations) > n:
                recommendations.popitem[0] # Remove the first one
        
        return list(recommendations.keys())[::-1]

    def updateUserDictPositionForNameChange(self, user: User, newName: str):
        self.usersByFL[user.firstLetter].remove(user)
        self.usersByFL[newName[0]].add(user)
        