from model import BisectionMethod
from view import MainView
from controller import BisectionController
import tkinter as tk

def main():
    root = tk.Tk()
    
    model = BisectionMethod()
    view = MainView(root)
    controller = BisectionController(model, view)
    
    controller.run()

if __name__ == "__main__":
    main()