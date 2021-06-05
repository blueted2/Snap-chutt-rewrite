from menus import main_menu
from userDatabase import UserDatabase
from user import User

d = UserDatabase("database.txt")


main_menu(d)
