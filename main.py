from menus import main_menu
from userDatabase import UserDatabase
from user import User
import interface

u1 = User()
u2 = User(fullName= "Rick Asley")

database = UserDatabase()

database.addUser(u1)
database.addUser(u2)

main_menu(database)
