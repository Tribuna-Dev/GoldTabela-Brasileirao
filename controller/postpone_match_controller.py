from service.round_service import RoundService
from service.team_service import TeamService
from service.match_service import MatchService
from customtkinter import StringVar, CTkToplevel
from tkinter import messagebox
from utils.event_manager import EventManager

class PostponeMatchController:
    
    def __init__(self, round_service : RoundService, team_service : TeamService, match_service : MatchService, round_number : int, window : CTkToplevel):
        self.round_service = round_service
        self.team_service = team_service
        self.match_service = match_service
        self.round_number = round_number
        self.window = window
        self.select_match = StringVar()
    
    def get_matches_list(self):
        
        matches = self.round_service.get_matches_by_round_number(self.round_number)
        
        matches_list = []
        
        for match_number in matches.keys():
            home_team_name = self.team_service.get_team_name_by_id(self.round_service.get_home_team_id(self.round_number, match_number))
            away_team_name = self.team_service.get_team_name_by_id(self.round_service.get_away_team_id(self.round_number, match_number))
            row = str(match_number) + " - " + home_team_name + " x " + away_team_name
            matches_list.append(row)
        
        return matches_list
    
    def postpone_matche(self):
        
        select_match = self.select_match.get()
        
        
        if select_match != "":
            
            match_number = int(select_match.split()[0])
            
            match_has_occurred = self.round_service.get_match_has_occurred(self.round_number, match_number)
            
            if not match_has_occurred:
                self.round_service.postpone_match(self.round_number, match_number)
                self.match_service.persist_is_postponed(self.round_number, match_number, True)
                self.window.destroy()
                EventManager.publish("REFRESH_MATCH_INTERFACE", None)
            
            else:
                messagebox.showinfo("Aviso!", "Não é possível adiar uma partida que já ocorreu.")
             
        else:
            messagebox.showinfo("Aviso!", "Você precisa escolher uma partida.")