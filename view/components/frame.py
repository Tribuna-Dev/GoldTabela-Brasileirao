from customtkinter import CTkFrame
from customtkinter import CTkScrollableFrame

class MainFrame(CTkFrame):

    def __init__(self, master, **kwargs):

        defaults = {
            'border_width': 5,
            'fg_color': "white",
            'border_color': "#DAA520", 
            'corner_radius': 10
        }
        
        defaults.update(kwargs)
        
        super().__init__(master, **defaults)

class Frame(CTkFrame):

    def __init__(self, master, **kwargs):

        defaults = {
            'fg_color': "white",
        }
        
        defaults.update(kwargs)
        
        super().__init__(master, **defaults)

class ScrollableFrame(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        defaults = {
            'orientation': "vertical",
            'scrollbar_button_color': "#DAA520",
            'scrollbar_button_hover_color': "#8D6F3A",
            'fg_color': "white"
        }
        
        defaults.update(kwargs)
        
        super().__init__(master, **defaults)