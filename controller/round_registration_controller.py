from service.round_service import RoundService
from service.team_service import TeamService
from customtkinter import StringVar, CTkToplevel
from view.components.entry import Entry
from tkinter import messagebox
from model.match import Match
from service.match_service import MatchService
from utils.event_manager import EventManager

class RoundRegistrationController:
    
    def __init__(self, team_service : TeamService, match_service : MatchService, round_service : RoundService, round_number : int, windown : CTkToplevel):
        
        self.team_service = team_service
        self.match_service = match_service
        self.round_service = round_service
        self.teams = self.get_team_names_list()

        self.matches = []
        self.round_number = round_number
        self.windown = windown

    def get_teams(self):
        return self.teams
    
    def get_team_names_list(self):
        return self.team_service.get_team_names_list()
    

    def add_match_to_list(self, home_team : StringVar, away_team : StringVar, date : Entry, time : Entry) -> None:
        self.matches.append({"home_team": home_team, "away_team": away_team, "date": date, "time": time})
    
    def register_matches(self):
        
        matches_dict = {}
            
        for i, match in enumerate(self.matches, start=1):

            if match['home_team'].get() == "" or match['away_team'].get() == "" or match['time'].get() == "":
                messagebox.showinfo("Warning!", "All match fields must be filled!")
                return
            
            elif match['home_team'].get() == match['away_team'].get():
                messagebox.showinfo("Warning!", "The competing teams must be different!")
                return

            elif match['home_team'].get() not in self.teams:
                messagebox.showinfo("Warning!", "Invalid home team!")
                return
            
            elif match['away_team'].get() not in self.teams:
                messagebox.showinfo("Warning!", "Invalid away team!")
                return

            else:
                matches_dict[i] = Match(
                    id = None,
                    round_number=self.round_number,
                    match_number= i,
                    home_team_id= self.team_service.get_team_id_by_name(match['home_team'].get()),
                    away_team_id= self.team_service.get_team_id_by_name(match['away_team'].get()),
                    time=match['time'].get(),
                    date=match['date'].get(),
                    home_goals=None,
                    away_goals=None,
                    has_occurred=False,
                    is_postponed=False
                )
        
        self.round_service.set_matches_to_round(self.round_number, matches_dict)
        self.match_service.register_round_matches(matches_dict)
        
        EventManager.publish("ROUND_REGISTERED", {"windown": self.windown})