from customtkinter import CTk, CTkToplevel, BOTH, X, RIGHT, LEFT, StringVar
from view.components.button import Button
from view.components.frame import Frame, ScrollableFrame
from view.components.label import Label
from.components.entry import Entry
from view.components.combobox import ComboBox
from controller.controller_factory import ControllerFactory
from utils.event_manager import EventManager
from view.matches_registration import MatchesRegistration

class RoundRegistration:
    """Janela para cadastro de rodadas do campeonato."""
    
    def __init__(self, round_number : int, parent_windown: CTk, controller_factory : ControllerFactory):

        self.windown = self._setup_window(round_number, parent_windown)

        self.controller_factory = controller_factory
        self.controller = controller_factory.create_round_registration_controller(round_number, self.windown)
        
        self._setup_event_handlers()
        
        self._round_registration_interface()
        
    def _setup_window(self, round_number: int, parent_windown: CTk) -> CTkToplevel:
        
        """Configura a janela de cadastro."""
        windown = CTkToplevel(parent_windown)
        windown.transient(parent_windown)
        windown.geometry('800x800')
        windown.title(f"Rodada {round_number}")
        
        return windown
        
    def _setup_event_handlers(self) -> None:
        """Configura todos os event handlers da janela principal."""
        EventManager.subscribe("ROUND_REGISTERED", self.handle_round_registered)
    
    def _round_registration_interface(self) -> None:
        
        frame = ScrollableFrame(master=self.windown)
        frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

        for i in range(1, 11, 2):
            
            matches_frame = Frame(frame)
            matches_frame.pack(fill=X, expand=True, padx=10, pady=10)
            
            self._create_match_input_fields(matches_frame, i)
            
            self._create_match_input_fields(matches_frame, i+1)

        Button(self.windown, text="   Cadastrar Rodada   ", command= lambda: self.controller.register_matches()
               ).pack(padx=10, pady=15)
    
    def _create_match_input_fields(self, parent_frame: Frame, match_num: int) -> None:

        teams = [""] + self.controller.get_teams()

        match_frame = Frame(parent_frame)
        match_frame.pack(side=RIGHT if match_num % 2 == 0 else LEFT, padx=10, pady=0)
        
        home_frame =  Frame(match_frame)
        home_frame.pack(padx=10, pady=3)

        home_team = self._create_team_selection(home_frame, "Mandante:   ", teams)
        
        away_frame = Frame(match_frame)
        away_frame.pack(padx=10, pady=3)
        
        away_team = self._create_team_selection(away_frame, "Visitante:     ", teams)

        date_frame = Frame(match_frame)
        date_frame.pack(padx=10, pady=3)

        Label(date_frame, text="Data:       ", font_size=15
              ).pack(side=LEFT)

        date = Entry(date_frame)
        date.pack(side=LEFT)

        time_frame = Frame(match_frame)
        time_frame.pack(padx=10, pady=3)

        Label(time_frame, text="Horario:       ", font_size=15
              ).pack(side=LEFT)

        time = Entry(time_frame)
        time.pack(side=LEFT)

        self.controller.add_match_to_list(home_team, away_team, date, time)
    
    def _create_team_selection(self, parent: Frame, label: str, teams: list) -> StringVar:
        """Cria o selecionador de times e retorna uma variavel com referencia ao valor selecionado"""
        Label(parent, text=label, font_size=15
              ).pack(side=LEFT)

        team = StringVar()
        
        ComboBox(parent, values=teams, variable=team).pack(side=LEFT)

        return team

    def handle_round_registered(self, data):
        
        for widget in self.windown.winfo_children():
                widget.destroy()
        
        MatchesRegistration(data['windown'])
        
        
        
        