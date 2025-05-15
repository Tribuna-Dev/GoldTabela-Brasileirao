from model.match import Match
from model.match_dao import MatchDAO
from tkinter import messagebox
from typing import Dict

class MatchService:
    
    def __init__(self, match_dao : MatchDAO):
        
        self.match_dao = match_dao
    
    def register_round_matches(self, matches):
        success = self.match_dao.register_round_matches(matches)
        
        if success:
            messagebox.showinfo("Success", "Matches registered successfully!")
        else:
            messagebox.showerror("Error", "Failed to register matches!")
    
    def get_matches_by_round(self, round_number: int) -> Dict[int, Match]:
        """
        Obtém todas as partidas de uma rodada e transforma em objetos Match.
        
        Args:
            round_number (int): Número da rodada desejada
            
        Returns:
            Dict[int, Match]: Dicionário onde a chave é o número da partida
                            e o valor é o objeto Match correspondente
        """
        matches_data = self.match_dao.get_matches_by_round(round_number)
        matches = {}
        
        for match_data in matches_data:
            match = self._create_match_from_dict(match_data)
            matches[match.match_number] = match
            
        return matches
    
    def _create_match_from_dict(self, match_data: Dict) -> Match:
        """
        Cria um objeto Match a partir de um dicionário de dados.
        
        Args:
            match_data (Dict): Dicionário com os dados da partida
            
        Returns:
            Match: Objeto Match criado
        """
        return Match(
            id=match_data['id'],
            round_number=match_data['round_number'],
            match_number=match_data['match_number'],
            home_team_id=match_data['home_team_id'],
            away_team_id=match_data['away_team_id'],
            time=match_data['time'],
            date=match_data['date'],
            home_goals=match_data['home_goals'],
            away_goals=match_data['away_goals'],
            has_occurred=bool(match_data['has_occurred']),
            is_postponed=bool(match_data['is_postponed'])
        )

    def register_matches_score(self, matches: Dict[int, Match]):
        """
        Registra os placares das partidas no banco de dados.
        
        Args:
            matches (Dict[int, Match]): Dicionário de partidas onde a chave é o match_number
                                    e o valor é o objeto Match com os placares atualizados
        """
        try:
            # Preparar os dados para o DAO
            matches_data = []
            for match in matches.values():
                matches_data.append({
                    'id': match.id,
                    'home_goals': match.home_goals,
                    'away_goals': match.away_goals,
                    'has_occurred': match.has_occurred,
                    'is_postponed': match.is_postponed
                })
            
            # Chamar o DAO para persistir os dados
            success = self.match_dao.register_matches_score(matches_data)
            
            if success:
                messagebox.showinfo("Success", "Scores registered successfully!")
            else:
                messagebox.showerror("Error", "Failed to register scores!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def check_is_round_over(self, matches):
        
        for match in matches.values():
            if not match.has_occurred and not match.is_postponed:
                return False
    
        return True
    
    def get_finished_matches_in_round(self, matches):
        
        matches_list = []
        
        for match in matches.values():
            if match.get_has_occurred():
                matches_list.append({'home_team_id' : match.get_home_team_id(), 'away_team_id' : match.get_away_team_id(), 'home_team_goals' : match.get_home_goals(), 'away_team_goals' : match.get_away_goals(), 'time' : match.get_time()})
        
        return matches_list
    
    def get_upcoming_matches_in_round(self, matches):
        
        matches_list = []
        
        for match in matches.values():
            if not match.get_has_occurred():
                matches_list.append({'home_team_id' : match.get_home_team_id(), 'away_team_id' : match.get_away_team_id(), 'time' : match.get_time()})

        return matches_list
    
    def get_team_results_outcomes(self, team_id: int, current_round: int):
        """
        Retorna uma lista com os resultados de um time até a rodada atual.
        Cada item da lista será uma string indicando se o time venceu, empatou ou perdeu:
        ">vitoria<", ">empate<" ou ">derrota<"

        Args:
            team_id (int): ID do time
            current_round (int): Rodada atual

        Returns:
            List[str]: Lista com os resultados (como strings) em ordem da rodada mais recente para a mais antiga.
        """
        try:
            results = self.match_dao.get_latest_results_for_team(team_id, current_round)
            outcomes = []

            for match in results:
                home_id = match['home_team_id']
                away_id = match['away_team_id']
                home_goals = match['home_goals']
                away_goals = match['away_goals']

                if team_id == home_id:
                    if home_goals > away_goals:
                        outcomes.append(">vitoria<")
                    elif home_goals == away_goals:
                        outcomes.append(">empate<")
                    else:
                        outcomes.append(">derrota<")
                elif team_id == away_id:
                    if away_goals > home_goals:
                        outcomes.append(">vitoria<")
                    elif away_goals == home_goals:
                        outcomes.append(">empate<")
                    else:
                        outcomes.append(">derrota<")

            return outcomes

        except Exception as e:
            print(f"Error processing results for team {team_id}: {e}")
            return []
    
    def persist_is_postponed(self, round_number : int, match_number : int, is_postponed : bool):
        self.match_dao.persist_is_postpone(round_number, match_number, is_postponed)
        
    def create_match_dict(self, match : Match):
        return {
        'has_occurred': match.get_has_occurred(),
        'home_team_id': match.get_home_team_id(),
        'home_goals': match.get_home_goals(),
        'away_team_id': match.get_away_team_id(),
        'away_goals': match.get_away_goals(),
        'is_postponed': match.is_postponed,
        'date': match.date,
        'time': match.get_time(),
    }
    
    def add_score_to_match(self, match : Match, home_goals : int, away_goals : int):
        match.set_home_goals(home_goals)
        match.set_away_goals(away_goals)
        match.set_has_occurred(True)