# main.py
from Model.Model import Model
from View.View import View
from Controller.Controller import Controller

def main():
    model = Model()
    controller = Controller(model, None)
    view = View(controller)
    controller.view = view  # set view in controller

    view.mainloop()

if __name__ == "__main__":
    main()
