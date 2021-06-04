from BRGui import Visualize
from backend import Backend

class Main:
    @staticmethod
    def main():
        bcEnd = Backend()
        main_window = Visualize(bcEnd)
        bcEnd.window = main_window
        main_window.show()


Main.main()