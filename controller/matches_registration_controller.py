from service.round_service import RoundService
from service.team_service import TeamService
from service.round_position_service import RoundPositionService
from utils.event_manager import EventManager

class MatchesRegistrationController:
    
    def __init__(self, round_service : RoundService, team_service : TeamService, round_position_service: RoundPositionService, round_number : int, current_round_number : int):
        self.round_service = round_service
        self.team_service = team_service
        self.round_position_service = round_position_service
        self.round_number = round_number
        self.current_round_number = current_round_number
        self.match_score_list = []
    
    def get_match_dict(self, match_number : int):
        
        match_dict = self.round_service.get_match_dict(self.round_number, match_number)
        
        match_dict['home_team_name'] = self.team_service.get_team_name_by_id(match_dict['home_team_id'])
        match_dict['away_team_name'] = self.team_service.get_team_name_by_id(match_dict['away_team_id'])
        
        return match_dict
    
    def add_match_score(self, match_number : int, has_occurred : bool, home_gols_entry, away_gols_entry, home_team_id, away_team_id):
        if not has_occurred:
            self.match_score_list.append({'match_number' : match_number, 'home_gols_entry' : home_gols_entry, 'away_gols_entry' : away_gols_entry, 'home_team_id' : home_team_id, 'away_team_id' : away_team_id})
    
    def register_matches_score(self):
        for match in self.match_score_list:
            if match['home_gols_entry'].get() != "" and match['away_gols_entry'].get() != "":
                home_team_goals = int(match['home_gols_entry'].get())
                away_team_goals = int(match['away_gols_entry'].get())
                self.round_service.add_score_to_match(self.round_number, match['match_number'], home_team_goals, away_team_goals)
                self.team_service.update_team_stats(match['home_team_id'], match['away_team_id'], home_team_goals, away_team_goals)
        
        self.round_service.persist_matches_score(self.round_number)    
        self.team_service.persist_team_stats()
        
        self.round_service.check_is_round_over(self.round_number)
            
        EventManager.publish("REFRESH_MATCH_INTERFACE", None)
    
    def call_event_unregister_match(self):
        EventManager.publish("UNREGISTER_MATCH", {'round_number' : self.round_number})
    
    def call_event_postpone_match(self):
        EventManager.publish("POSTPONE_MATCH", {'round_number' : self.round_number})

    def get_current_round_number(self) -> int:
        return self.current_round_number
    
    def get_round_number(self) -> int:
        return self.round_number 