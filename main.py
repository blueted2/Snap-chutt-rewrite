"""@package docstring
This is the main entrypoint for the program. It will create a database, give it the file from which it will load save save, then it will start the main menu.
"""

from menus import main_menu
from userDatabase import UserDatabase

main_menu(UserDatabase("database.txt"))
