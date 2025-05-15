from model.team_dao import TeamDAO
from model.team import Team
from typing import Dict, List

class TeamService:
    
    def __init__(self, team_dao : TeamDAO):
        self.team_dao = team_dao
        self.teams: Dict[int, Team] = {}  # Dicionário: {nome_time: instância_Team}
        self._load_all_teams()
    
    def _load_all_teams(self):
        """Carrega todos os times do banco de dados para memória"""
        teams_data = self.team_dao.get_all_teams_data()
        
        for team_data in teams_data:
            team = Team(
                id = team_data['id'],
                name=team_data['name'],
                stadium=team_data['stadium'],
                points=team_data['points'],
                matches_played=team_data['matches_played'],
                wins=team_data['wins'],
                draws=team_data['draws'],
                losses=team_data['losses'],
                goals_for=team_data['goals_for'],
                goals_against=team_data['goals_against'],
                goal_difference=team_data['goal_difference']
            )
            self.teams[team_data['id']] = team
    
    def get_team_names_list(self) -> List[str]:
        """
        Retorna uma lista ordenada alfabeticamente com os nomes de todos os times
        """
        return sorted([team.name for team in self.teams.values()])
    
    def get_team_id_by_name(self, team_name: str) -> int:
        """
        Retorna o ID do time com base no nome fornecido.
        
        Args:
            team_name: Nome do time a ser buscado
            
        Returns:
            O ID do time correspondente
            
        Raises:
            ValueError: Se nenhum time com o nome fornecido for encontrado
        """
        for team_id, team in self.teams.items():
            if team.name.lower() == team_name.lower():
                return team_id
        
        raise ValueError(f"Time com nome '{team_name}' não encontrado")
    
    def get_team_name_by_id(self, team_id: int) -> str:
        """
        Retorna o nome do time com base no ID fornecido.
        
        Args:
            team_id: ID do time a ser buscado
            
        Returns:
            O nome do time correspondente
            
        Raises:
            ValueError: Se nenhum time com o ID fornecido for encontrado
        """
        if team_id in self.teams:
            return self.teams[team_id].name
        
        raise ValueError(f"Time com ID '{team_id}' não encontrado")
    
    def update_team_stats(self, home_team_id : int, away_team_id : int, home_team_goals : int, away_team_goals : int):
        
        home_team = self.teams[home_team_id]
        away_team = self.teams[away_team_id]
        
        result = 0
        result_dict = {1: ">vitoria<", 0: ">empate<", -1: ">derrota<"}
        
        if home_team_goals > away_team_goals:
            home_team.increment_points(3)
            home_team.increment_wins()
            away_team.increment_losses()
            result = 1
        
        elif home_team_goals < away_team_goals:
            away_team.increment_points(3)
            away_team.increment_wins()
            home_team.increment_losses()
            result = -1
        
        else:
            home_team.increment_points(1)
            away_team.increment_points(1)
            home_team.increment_draws()
            away_team.increment_draws()
            
            
        home_team.increment_matches_played()
        away_team.increment_matches_played()
        
        home_team.increment_goals_for(home_team_goals)
        away_team.increment_goals_for(away_team_goals)
        home_team.increment_goals_against(away_team_goals)
        away_team.increment_goals_against(home_team_goals)
        home_team.update_goal_difference()
        away_team.update_goal_difference()
               
    def persist_team_stats(self):
        """Envia as estatísticas atualizadas de todos os times para o TeamDAO."""
        with TeamDAO() as team_dao: 
            for team in self.teams.values():
                team_dao.update_team_stats(
                    team_id=team.id,
                    points=team.points,
                    matches_played=team.matches_played,
                    wins=team.wins,
                    draws=team.draws,
                    losses=team.losses,
                    goals_for=team.goals_for,
                    goals_against=team.goals_against,
                    goal_difference=team.goal_difference
                )

    def get_teams_ranking(self) -> List[Team]:
        """
        Retorna uma lista de times ordenados pelos critérios:
        1. Pontos (decrescente)
        2. Vitórias (decrescente)
        3. Saldo de gols (decrescente)
        4. Gols marcados (decrescente)
        
        Returns:
            List[Team]: Lista de times ordenados
        """
        # Obtém todos os times como uma lista
        teams_list = list(self.teams.values())
        
        # Ordena usando os critérios especificados
        sorted_teams = sorted(
            teams_list,
            key=lambda team: (
                -team.points,          # Ordem decrescente
                -team.wins,            # Ordem decrescente
                -team.goal_difference, # Ordem decrescente
                -team.goals_for        # Ordem decrescente
            )
        )
        
        return sorted_teams
    
    def get_team_by_id(self, team_id: int) -> Team:
        """
        Retorna o time com base no ID fornecido.
        
        Args:
            team_id: ID do time a ser buscado
            
        Returns:
            O time correspondente
            
        Raises:
            ValueError: Se nenhum time com o ID fornecido for encontrado
        """
        if team_id in self.teams:
            return self.teams[team_id]
        
        raise ValueError(f"Time com ID '{team_id}' não encontrado")