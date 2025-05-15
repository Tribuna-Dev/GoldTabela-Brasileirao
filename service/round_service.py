from model.round_dao import RoundDAO
from typing import Dict
from model.round import Round
from model.match import Match
from service.match_service import MatchService
from service.round_position_service import RoundPositionService

class RoundService:
    
    def __init__(self, round_dao : RoundDAO, match_service : MatchService, round_position_service : RoundPositionService):
        self.round_dao = round_dao
        self.match_service = match_service
        self.round_position_service = round_position_service

        self.rounds: Dict[int, Round] = {}   # Dicionário vazio inicialmente.
    
    def _load_round(self, round_number : int) -> Round:

        round = self.round_dao.get_round_basic_info(round_number)

        matches = {}

        if round['are_matches_registered']:
            matches = self.match_service.get_matches_by_round(round_number)

        self.rounds[round_number] = Round(round['id'], round_number, matches, bool(round['is_round_over']), bool(round['are_matches_registered']))
    
    def get_round_by_number(self, round_number : int):
        
        if round_number not in self.rounds or self.rounds[round_number] is None:
            self._load_round(round_number)
        
        return self.rounds[round_number]
    
    def set_matches_to_round(self, round_number: int, matches_dict: Dict[int, Match]) -> None:

        round = self.rounds[round_number]

        round.set_matches(matches_dict)

        round.set_are_matches_registered(True)
        self.round_dao.set_matches_as_registered(round_number)
    
    def add_score_to_match(self, round_number, match_number, home_goals, away_goals):
        
        match = self.get_match(round_number, match_number)
        self.match_service.add_score_to_match(match, home_goals, away_goals)

    def get_matches_by_round_number(self, round_number):
        if round_number not in self.rounds or self.rounds[round_number] is None:
            self._load_round(round_number)
            
        return self.rounds[round_number].matches
    
    def get_first_unfinished_round_number(self) -> int:
        return self.round_dao.get_first_unfinished_round_number()
    
    
    def postpone_match(self, round_number, match_number):
        self.rounds[round_number].matches[match_number].set_is_postponed(True)
    
    def get_match(self, round_number : int, match_number : int):
        
        if round_number not in self.rounds or self.rounds[round_number] is None:
            self._load_round(round_number)
            
        return self.rounds[round_number].matches[match_number]
    
    def get_match_dict(self, round_number : int, match_number : int):
        match = self.get_match(round_number, match_number)
        return self.match_service.create_match_dict(match)
    
    def check_is_round_over(self, round_number: int):
        
        matches = self.get_matches_by_round_number(round_number)
        
        is_round_over = self.match_service.check_is_round_over(matches)
        
        if is_round_over:
            self.set_is_round_over(self.round_number)
            self.round_position_service.set_round_position(self.round_number)
        
    def set_is_round_over(self, round_number):
        self.rounds[round_number].set_is_round_over()
        self.round_dao.update_is_round_over(round_number)
    
    def persist_matches_score(self, round_number : int):
        
        matches = self.get_matches_by_round_number(round_number)
        
        self.match_service.register_matches_score(matches)