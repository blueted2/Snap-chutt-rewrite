import string
from sortedcontainers import SortedList
from sortedcollections import ValueSortedDict

# Check if a string contains any numbers. Used to avoid throwing exceptions when using int(string)
def hasNumbers(inputString):
  return any(char.isdigit() for char in inputString)

def accountExists(userId):
  return userId in allUsersById
  

def generateNewId():
  global currentLastId
  currentLastId += 1
  return currentLastId-1

def addUserToIdCorrespondance(user, id):
  global allUsersById
  allUsersById[id] = user

def addUserToAllUsers(user):
  firstLetter = user['fullName'][0]
  allUsersDict[firstLetter].add(user)


def addNewUser(fullName = "Test User", age = 18, studyYear = 2021, studyField = "Testing", residence = "My Computer", interests = set([1, 3, 6])):

  id = generateNewId()
  user = {
    "id"        : id,
    "fullName"  : fullName,
    "age"       : age,
    "studyYear" : studyYear,
    "studyField": studyField,
    "residence" : residence,
    "interests" : interests,
    "following" : set(),
    "followers" : set()
  }

  addUserToAllUsers(user)
  addUserToIdCorrespondance(user, id)

def removeUserFromAllUsersDict(user):
  firstLetter = user['fullName'][0]
  allUsersDict[firstLetter].remove(user)

def removeUserFromFollowersAndFollowing(removeId):
  removedUser = allUsersById[removeId]
  # We need to copy the set of followers / following, because removeFollow will modify that set. 
  for followingId in removedUser["following"].copy():
    removeFollow(removeId, followingId)

  for followerId in removedUser["followers"].copy():
    removeFollow(followerId, removeId)

def removeUser(id):
  removeUserFromAllUsersDict(allUsersById[id])
  removeUserFromFollowersAndFollowing(id)
  allUsersById.pop(id)

# If the newValue is an empty string, return the old value, else return the new value
def sameIfEmptyString(oldValue, newValue):
  if newValue == "": return oldValue
  return newValue



# Returns False if the user if there is already a follow/followed relationship, True if not.
def addFollow(followerId, followingId):
  follower = allUsersById[followerId]
  following = allUsersById[followingId]

  if followingId in follower['following']:
    return False

  follower['following'].add(followingId)
  following['followers'].add(followerId)
  return True

def removeFollow(followerId, followingId):
  follower = allUsersById[followerId]
  following = allUsersById[followingId]

  if followingId not in follower['following']:
    return False

  follower['following'].remove(followingId)
  following['followers'].remove(followerId)
  return True

def searchUsers(name = None, studyYear = None, studyField = None, interests = None):
  matches = []
  for id, user in allUsersById.items():
    if name != None and name.lower() not in user["fullName"].lower():
      continue
    if studyYear != None and studyYear != user["studyYear"]:
      continue
    if studyField != None and studyField != user["studyField"]:
      continue
    if interests != None and not set(interests).issubset(user["interests"]):
      continue
    
    matches.append(id)

  return matches

# This function should be symetrical
def getRecommendationScore(userId1, userId2):
  user1 = allUsersById[userId1]
  user2 = allUsersById[userId2]

  follows_score = 1 + len(user1["following"].intersection(user2["following"]))

  interests_score = 1+ len(user1["interests"].intersection(user2["interests"]))

  return interests_score * follows_score


def getRecommendations(userId, n=5):
  # recommendations = ValueSortedDict(lambda score: -score)
  recommendations = ValueSortedDict()
  
  for id in allUsersById.keys():
    if id == userId: continue # Don't want to add self
    recommendations[id] = getRecommendationScore(userId, id)
    if len(recommendations) > n:
      recommendations.popitem[0] # Remove the first one
  
  return list(recommendations.keys())[::-1]

def createTestUsers():
  addNewUser()
  addNewUser(fullName = "Alex")
  addNewUser(fullName = "Dylan", interests = [2, 5, 3])
  addNewUser(fullName = "Bob", interests = [])
  addNewUser(fullName = "Bobby", interests = [])
  addNewUser(fullName = "Rick Asley", interests = [2])

  addFollow(0, 2)
  addFollow(1, 2)

def main():
  pass


ALL_INTERESTS = ["sport", "cinema", "art", "health", "technology", "DIY", "cooking", "travel"]

allUsersById = {}
currentLastId = 0 # Will be incremented as new user ids are taken

#Initialize the allUsersDict dictionary, with keys from A to Z, and filled with empty SortedLists, all set-up to sort by the 'fullName' key. 
allUsersDict = {}
for letter in string.ascii_uppercase:
  allUsersDict[letter] = SortedList(key=lambda u: u['fullName'])

if __name__ == "__main__":
  # execute only if run as a script
  main()

