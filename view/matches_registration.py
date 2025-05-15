
from view.components.frame import MainFrame, Frame
from view.components.button import Button
from customtkinter import BOTH, X, LEFT, RIGHT, CTk, CTkToplevel
from view.components.label import Label
from controller.controller_factory import ControllerFactory
from.components.entry import Entry
from utils.event_manager import EventManager
from view.unregister_match import UnregisterMatch
from view.postpone_match import PostponeMatche

class MatchesRegistration:
    def __init__(self, window : CTkToplevel, parent_window : CTk, round_number : int, controller_factory : ControllerFactory, current_round_number : int):
        
        self.window = self._setup_window(window, parent_window, round_number)
        
        self._setup_event_handlers()
        
        self.controller_factory = controller_factory
        self.controller = controller_factory.create_matches_registration_controller(round_number, current_round_number)
        
        self._matches_registration_interface()


    def _setup_window(self, window : CTkToplevel, parent_window: CTk, round_number :int) -> CTkToplevel:
        
        new_window = None
        
        if window is None:
            new_window = CTkToplevel(parent_window)
            new_window.transient(parent_window)
            new_window.title(f"Rodada {round_number}")
            new_window.geometry('800x800')
        else:
            new_window = window
        
        return new_window
    
    def _setup_event_handlers(self) -> None:
        """Configura todos os event handlers da janela principal."""
        EventManager.subscribe("REFRESH_MATCH_INTERFACE", self.refresh_match_interface)
        EventManager.subscribe("UNREGISTER_MATCH", self.create_unregister_match_interface)
        EventManager.subscribe("POSTPONE_MATCH", self.create_postpone_match_interface)
        
    def _matches_registration_interface(self):
        
        frame = MainFrame(self.window)
        frame.pack(fill=BOTH, expand=True, padx=50, pady=50)
        
        for i in range(1, 11, 2):
            
            matches_frame = Frame(frame)
            matches_frame.pack(fill=X, expand=True, padx=10, pady=0)
            
            self._matche_interface(matches_frame, i)
            self._matche_interface(matches_frame, i+1)
        
        
        self._create_buttons()
    
    def _create_buttons(self):
        
        button_frame = Frame(self.window)
        button_frame.pack(padx=10, pady=30)

        if self.controller.get_round_number() < self.controller.get_current_round_number():
            Button(button_frame, text="Descadastrar Partida", command= lambda: self.controller.call_event_unregister_match()).pack(side=LEFT, padx=10, pady=10)
            Button(button_frame, text="Adiar Partida", command= lambda: self.controller.call_event_postpone_match()).pack(side=LEFT, padx=10, pady=10)
            
        elif self.controller.get_round_number() > self.controller.get_current_round_number():
            Label(button_frame, text=f'Para cadastrar jogos dessa rodada todas as anteriores devem estar finalizadas!  Rodada atual: {self.controller.get_current_round_number()}'  ,font_size=15).pack()
        
        else:
            Button(button_frame, text="Cadastrar Resultados", command= lambda: self.controller.register_matches_score()).pack(side=LEFT, padx=10, pady=10)
            Button(button_frame, text="Descadastrar Partida", command= lambda: self.controller.call_event_unregister_match()).pack(side=LEFT, padx=10, pady=10)
            Button(button_frame, text="Adiar Partida", command= lambda: self.controller.call_event_postpone_match()).pack(side=LEFT, padx=10, pady=10)
        
    def _matche_interface(self, frame : Frame, match_number : int):
        
        match_frame = Frame(frame)

        if match_number % 2 == 0:
            match_frame.pack(side=RIGHT, padx=10, pady=0)
        else:
            match_frame.pack(side=LEFT, padx=10, pady=0)
        
        match_dict = self.controller.get_match_dict(match_number) 
            
        home_gols_entry = self._team_interface(match_frame, match_dict['has_occurred'], match_dict['home_team_name'], match_dict['home_goals'])
         
        away_gols_entry = self._team_interface(match_frame, match_dict['has_occurred'], match_dict['away_team_name'], match_dict['away_goals'])

        self._date_and_time_interface(match_frame, match_dict['is_postponed'], match_dict['date'], match_dict['time'])
        
        self.controller.add_match_score(match_number, match_dict['has_occurred'], home_gols_entry, away_gols_entry, match_dict['home_team_id'], match_dict['away_team_id'])
        
    def _team_interface(self, match_frame, has_occurred, team_name, team_gols):
        
        frame =  Frame(match_frame)
        frame.pack(padx=10, pady=3)

        Label(frame, text=team_name +": ", font_size=15).pack(side=LEFT)

        gols_entry = None
        
        if has_occurred:
            Label(frame, text=team_gols, font_size=15).pack(side=LEFT)
        else:
            gols_entry = Entry(frame)
            gols_entry.pack(side=LEFT)
        
        return gols_entry
    
    def _date_and_time_interface(self, frame, is_postponed, date, time):
        
        if is_postponed:
            Label(frame, text="Partida Adiada", font_size=15).pack(side=LEFT, padx=10, pady=3)
        else:
            Label(frame, text= date + " " + time, font_size=15).pack(side=LEFT, padx=10, pady=3)
    
    def refresh_match_interface(self, data):
        
        for widget in self.window.winfo_children():
                widget.destroy()

        self._matches_registration_interface()
    
    def create_unregister_match_interface(self, data):
        UnregisterMatch(self.window, self.controller_factory, data['round_number'])
    
    def create_postpone_match_interface(self, data):
        PostponeMatche(self.window, self.controller_factory, data['round_number'])
        