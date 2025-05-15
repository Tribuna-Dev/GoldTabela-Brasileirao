from service.round_service import RoundService
from service.team_service import TeamService
from customtkinter import StringVar
from tkinter import messagebox

class UnregisterMatchController:
    def __init__(self, round_service : RoundService, team_service : TeamService, round_number : int):
        
        self.round_service = round_service
        self.team_service = team_service
        self.round_number = round_number
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
    
    def unregister_match(self):
        
        select_match = self.select_match.get()
        
        match_number = int(select_match.split()[0])
        
        if select_match != "":
            
            match_has_occurred = self.round_service.get_match_has_occurred(self.round_number, match_number)
            
            if match_has_occurred:
                pass
            
            else:
                messagebox.showinfo("Aviso!", "Essa partida ainda não tem resultados cadastrados.")
             
        else:
            messagebox.showinfo("Aviso!", "Você precisa escolher uma partida.")