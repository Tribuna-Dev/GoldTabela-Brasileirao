from model.round_position_dao import RoundPositionDAO
from service.team_service import TeamService
from model.round_position import RoundPosition
class RoundPositionService:
    def __init__(self, round_position_dao : RoundPositionDAO, team_service : TeamService):
        self.round_position_dao = round_position_dao
        self.team_service = team_service
        self. round_position = RoundPosition()
        
    def set_round_position(self, round_number: int) -> bool:
        """
        Calcula e salva as posições dos times para uma rodada
        
        Args:
            round_number: Número da rodada a ser processada
            
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        
        ranked_teams = self.team_service.get_teams_ranking()
       
        positions = [(team.get_id(), position) for position, team in enumerate(ranked_teams, start=1)]
        
        # Atualiza o cache antes de persistir no banco
        self.round_position.update_positions(round_number, positions)
        
        return self.round_position_dao.register_round_position(round_number, positions)
        
    def get_round_positions(self, round_number: int) -> list[dict]:
        """
        Obtém as posições de uma rodada (usa cache se disponível)
        
        Args:
            round_number: Número da rodada desejada
            
        Returns:
            Lista de dicionários no formato:
            [{'team_id': int, 'position': int}, ...]
        """
        # Se existir no cache, retorna do cache
        if self.round_position.has_round(round_number):
            return self.round_position.get_positions(round_number)
        
        # Se não existir no cache, busca do banco
        db_positions = self.round_position_dao.get_round_positions(round_number)
        if db_positions:
            # Atualiza o cache com os dados do banco
            positions = [(pos['team_id'], pos['position']) for pos in db_positions]
            self.round_position.update_positions(round_number, positions)
        
        return db_positions or []
    