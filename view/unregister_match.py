from customtkinter import CTkToplevel, BOTH, LEFT
from.components.frame import MainFrame, Frame
from.components.label import Label
from.components.combobox import ComboBox
from.components.button import Button
from controller.controller_factory import ControllerFactory

class UnregisterMatch:
    
    def __init__(self, parent_window: CTkToplevel, controller_factory : ControllerFactory, round_number : int):
        
        self.window = self._setup_window(parent_window)
        
        self.controller = controller_factory.create_unregister_match_controller(round_number)
        
        #self.round_number = round_number
        
        self._create_interface_unregister_match()
        
    def _setup_window(self, parent_window: CTkToplevel) -> CTkToplevel:
        
        """Configura a janela de cadastro."""
        window = CTkToplevel(parent_window)
        window.transient(parent_window)
        window.geometry('700x250')
        window.title("Descadastro de Partidas")
        
        return window
    
    def _create_interface_unregister_match(self):
        
        frame = MainFrame(self.window)
        frame.pack(padx=50, pady=30, ipadx=10, ipady=20, fill=BOTH, expand=True)

        select_match_frame = Frame(frame)
        select_match_frame.pack(padx=10, pady=15)

        Label(select_match_frame, text="Escolha uma partida :",font_size=19).pack(padx=10, pady=10, side=LEFT)

        ComboBox(select_match_frame, values = self.controller.get_matches_list(), variable=None).pack(padx=10, pady=10, side=LEFT)

        button_frame = Frame(frame)
        button_frame.pack(padx=10, pady=5)

        Button(button_frame, text="Descadastrar Resultado", command=lambda: self.controller.unregister_match()).pack(padx=10, pady=10, side=LEFT)

        Button(button_frame, text="Alterar Times", command=lambda: None).pack(padx=10, pady=10, side=LEFT)