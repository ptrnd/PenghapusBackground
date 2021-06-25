from Gui import Gui
from Backend import Backend

class Main:
    @staticmethod
    def main():
        bcEnd = Backend()
        main_window = Gui(bcEnd)
        bcEnd.window = main_window
        main_window.show()


Main.main()