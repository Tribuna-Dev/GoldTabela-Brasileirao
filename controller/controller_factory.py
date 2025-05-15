from controller.main_window_controller import MainWindowController
from service.round_service import RoundService
from model.round_dao import RoundDAO
from model.team_dao import TeamDAO
from service.team_service import TeamService
from model.match_dao import MatchDAO
from service.match_service import MatchService
from model.round_position_dao import RoundPositionDAO
from service.round_position_service import RoundPositionService

class ControllerFactory:
    
    def __init__(self):
        self.match_dao = MatchDAO()
        self.match_service = MatchService(self.match_dao)
        
        self.team_dao = TeamDAO()
        self.team_service = TeamService(self.team_dao)
        
        self.round_position_dao = RoundPositionDAO()
        self.round_position_service = RoundPositionService(self.round_position_dao, self.team_service)
        
        self.round_dao = RoundDAO()
        self.round_service = RoundService(self.round_dao, self.match_service, self.round_position_service)
        
        
    def create_main_controller(self):
        """Cria o controller da janela principal"""
        return MainWindowController(self.round_service, self.team_service, self.match_service, self.round_position_service)
    
    def create_round_registration_controller(self, round_number, windown):
        """Cria o controller para cadastro de rodada"""
        from controller.round_registration_controller import RoundRegistrationController
        return RoundRegistrationController(self.team_service, self.match_service, self.round_service, round_number, windown)
    
    def create_matches_registration_controller(self, round_number : int, current_round_number: int):
        from controller.matches_registration_controller import MatchesRegistrationController
        return MatchesRegistrationController(self.round_service, self.team_service, self.round_position_service, round_number, current_round_number)
    
    def create_unregister_match_controller(self, round_number : int):
        from controller.unregister_match_controller import UnregisterMatchController
        return UnregisterMatchController(self.round_service, self.team_service, round_number)
    
    def create_postpone_match_controller(self, round_number : int, window):
        from controller.postpone_match_controller import PostponeMatchController
        return PostponeMatchController(self.round_service, self.team_service, self.match_service, round_number, window)