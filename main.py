from menus import main_menu
from userDatabase import UserDatabase
from user import User

database = UserDatabase(file = "database.txt")

# u1 = User()
# u2 = User(fullName= "Rick Asley")

# database = UserDatabase()

# database.addNewUser(u1)
# database.addNewUser(u2)

# main_menu(database)
# print(u1.toFileString())

s = """2
0
Test User
18
2021
Testing
My Computer
[1, 3, 6]
[]
[]

1
Rick Asley
18
2021
Testing
My Computer
[1, 3, 6]
[]
[]"""

d = UserDatabase("database.txt")
d.loadFile()

main_menu(d)

# u3 = User.fileStringListToUser(s.split("\n"))

