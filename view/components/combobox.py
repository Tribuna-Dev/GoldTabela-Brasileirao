from customtkinter import CTkComboBox

class ComboBox(CTkComboBox):

    def __init__(self, master, **kwargs):

        defaults = {
            'fg_color': "#D2B48C",
            'border_color': "#D2B48C",
            'button_color': "#D2B48C",
            'button_hover_color': "#F5DEB3",
            'dropdown_fg_color': "#D2B48C",
            'dropdown_hover_color': "#F5DEB3",
            'dropdown_text_color': "#5c4100",
            'text_color': "#5c4100",
            'corner_radius': 8,
            'font': ("Arial", 12),
            'state': "readonly",
        }
        
        defaults.update(kwargs)
        
        super().__init__(master, **defaults)