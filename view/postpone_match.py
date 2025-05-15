from customtkinter import CTkToplevel, BOTH, LEFT
from.components.button import Button
from.components.frame import MainFrame, Frame
from.components.label import Label
from.components.combobox import ComboBox
from controller.controller_factory import ControllerFactory
class PostponeMatche:
    
    def __init__(self, parent_window, controller_factory : ControllerFactory, round_number : int):
        
        self.window = self._setup_window(parent_window)
        
        self.controller = controller_factory.create_postpone_match_controller(round_number, self.window)
        
        self._create_postpone_interface()
        
    
    def _setup_window(self, parent_windown: CTkToplevel) -> CTkToplevel:
        
        windown = CTkToplevel(parent_windown)
        windown.transient(parent_windown)
        windown.geometry('700x250')
        windown.title("Adiar partida!")
        
        return windown
    
    def _create_postpone_interface(self):
        
        frame = MainFrame(self.window)
        frame.pack(padx=50, pady=30, ipadx=10, ipady=20, fill=BOTH, expand=True)

        select_match_frame = Frame(frame)
        select_match_frame.pack(padx=10, pady=15)

        Label(select_match_frame, text="Escolha uma partida :",font_size=19).pack(padx=10, pady=10, side=LEFT)

        ComboBox(select_match_frame, values= self.controller.get_matches_list(), variable=self.controller.select_match).pack(padx=10, pady=10, side=LEFT)

        frame_botoes = Frame(frame)
        frame_botoes.pack(padx=10, pady=5)

        Button(frame_botoes, text="Adiar Jogo", command=lambda: self.controller.postpone_matche()).pack(padx=10, pady=10, side=LEFT)