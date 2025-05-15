from customtkinter import CTkLabel

class Label(CTkLabel):

    def __init__(self, master, font_size, **kwargs):

        defaults = {
            'font': ("Times New Roman", font_size),
            'text_color': "#5c4100",  
            'anchor': "center",
            'compound': "left"
        }
        
        defaults.update(kwargs)
        
        super().__init__(master, **defaults)
