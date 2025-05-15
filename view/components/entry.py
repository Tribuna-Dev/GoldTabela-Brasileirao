from customtkinter import CTkEntry

class Entry(CTkEntry):

    def __init__(self, master, **kwargs):

        defaults = {
            'fg_color': "#D2B48C",
            'border_color': "#D2B48C",
            'text_color': "#5c4100",
            'corner_radius': 8,
            'border_width': 2,
            'font': ("Arial", 12),
        }
        
        defaults.update(kwargs)
        

        super().__init__(master, **defaults)


class EntryHora(CTkEntry):
    """Entry especializado para horários"""
    def __init__(self, master, **kwargs):
        defaults = {
            'fg_color': "#F5F5DC",
            'border_color': "#DAA520",
            'text_color': "#5c4100",
            'width': 80,
            'justify': "center",
            'placeholder_text': "HH:MM"
        }
        defaults.update(kwargs)
        super().__init__(master, **defaults)