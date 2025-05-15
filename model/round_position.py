class RoundPosition:
    def __init__(self):
        self.round_position_dict = {}  # {round_number: {team_id: position}}
    
    def update_positions(self, round_number: int, positions: list[tuple[int, int]]) -> None:
        """
        Atualiza o cache com as posições de uma rodada
        
        Args:
            round_number: Número da rodada
            positions: Lista de tuplas (team_id, position)
        """
        self.round_position_dict[round_number] = {team_id: position for team_id, position in positions}
    
    def get_positions(self, round_number: int) -> list[dict]:
        """Obtém as posições de uma rodada do cache"""
        if not self.has_round(round_number):
            return []
            
        positions = self.round_position_dict[round_number]
        return [
            {'team_id': team_id, 'position': pos}
            for team_id, pos in sorted(positions.items(), key=lambda x: x[1])
        ]
    
    def has_round(self, round_number: int) -> bool:
        """Verifica se uma rodada existe no cache"""
        return round_number in self.round_position_dict