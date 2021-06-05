from menus import main_menu
from userDatabase import UserDatabase
from user import User
import interface

u1 = User()
u2 = User(fullName= "Rick Asley")

database = UserDatabase()

database.addNewUser(u1)
database.addNewUser(u2)

main_menu(database)
