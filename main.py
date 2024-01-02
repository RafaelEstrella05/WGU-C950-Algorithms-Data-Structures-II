# main.py
from Model.Model import Model
from View.View import View
from Controller.Controller import Controller

def main():

    '''
        model = Model() # create Model
        controller = Controller(model, None), # create Controller, pass reference to Model
        view = View(controller) # create View
        controller.set_view(view) # pass reference to View to Controller

        view.mainloop()  # start application
    '''


if __name__ == "__main__":  
    main()
