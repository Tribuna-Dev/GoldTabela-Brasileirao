from typing import Dict, Any
from customtkinter import CTk, set_appearance_mode, CTkImage, BOTH, LEFT
from PIL import Image
from view.components.button import Button
from view.components.frame import Frame, MainFrame
from view.components.label import Label
from view.components.combobox import ComboBox
from controller.controller_factory import ControllerFactory
from utils.event_manager import EventManager
from view.round_registration import RoundRegistration
from view.matches_registration import MatchesRegistration

class MainWindow(CTk):
    
    def __init__(self, controller_factory : ControllerFactory):
        
        super().__init__()
        
        self._setup_appearance()

        self.controller_factory = controller_factory 
        self.controller = controller_factory.create_main_controller()

        self._setup_event_handlers()
         
        self._create_interface()
        
    def _setup_appearance(self) -> None: 
        """Configura o tema visual da aplicação."""
        set_appearance_mode("dark")
        self.title("Brasileirão Assaí - Série A 2024")
        self.geometry('600x700')

    def _setup_event_handlers(self) -> None:
        """Configura todos os event handlers da janela principal."""
        EventManager.subscribe("ROUND_SELECTED", self.handle_selected_round)
    
    def _create_interface(self) -> None:
            
        self._create_logo()

        frame = MainFrame(master=self)
        frame.pack(fill=BOTH, expand=True, pady=70, padx=90)

        self._create_round_selector(frame)

        self._create_buttons(frame)
        
    def _create_logo(self):
        
        logo = CTkImage(dark_image=Image.open("assets/img/logo.png"), size=(200,200))
        Label(self, image=logo, text="", font_size=15
              ).pack(padx=10, pady=0)

        logo = CTkImage(dark_image=Image.open("assets/img/logo_brasileirao.png"), size=(127, 150))
        Label(self, image=logo, text="", font_size=15
              ).pack(padx=10, pady=0)
    
    def _create_round_selector(self, frame : MainFrame):

        frame_select_round = Frame(frame)
        frame_select_round.pack(padx=10, pady=10)

        Label(frame_select_round,  text="Escolha a rodada:", font_size=19).pack(padx=10, pady=20, side=LEFT)

        ComboBox(frame_select_round, values=[str(numero) for numero in range(1,39)], variable = self.controller.round_select_number
                 ).pack(padx=10, pady=10, side=LEFT)
        
    def _create_buttons(self, frame : MainFrame):

        Button(frame, text="Acessar", command= lambda : self.controller.handle_round_selection()
               ).pack(padx=10, pady=10)

        Button(frame, text="Gerar Tabela", command= lambda : self.controller.export_championship_table()
               ).pack(padx=10, pady=10)

    
    def main_loop(self):
        self.mainloop()
    
    def handle_selected_round(self, data : Dict[str, Any]):
        if data['are_matches_registered']:
            pass
            MatchesRegistration(None, self, data['round_number'], self.controller_factory, data['current_round_number'])
        else:
            RoundRegistration(data['round_number'], self, self.controller_factory)
