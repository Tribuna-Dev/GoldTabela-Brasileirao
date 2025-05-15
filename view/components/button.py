from customtkinter import CTkButton

class Button(CTkButton):
    
    def __init__(self , master, **kwargs):
        
        defaults = {
            'fg_color': "#8D6F3A",
            'hover_color': "#B8860B",
            'text_color': "white",
            'corner_radius': 8,
            'font': ('Arial', 12),
        }

        defaults.update(kwargs)
        super().__init__(master, **defaults)
        