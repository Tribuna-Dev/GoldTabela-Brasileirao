from model.database import Database
from typing import List, Dict

class MatchDAO:
    def __init__(self):
        self.db = Database()
    
    def register_round_matches(self, matches):
        """
        Registra todas as partidas de uma rodada no banco de dados.
        
        Args:
            round_number (int): Número da rodada
            matches (dict): Dicionário de partidas onde a chave é o match_number e o valor é o objeto Match
        """
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()
            
            for match in matches.values():

                query = """
                INSERT INTO `match` (
                    round_number, 
                    match_number, 
                    home_team_id, 
                    away_team_id, 
                    time, 
                    date, 
                    home_goals, 
                    away_goals, 
                    has_occurred, 
                    is_postponed
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                cursor.execute(query, (
                    match.round_number,
                    match.match_number,
                    match.home_team_id,
                    match.away_team_id,
                    match.time,
                    match.date,
                    None,
                    None,
                    0,
                    0
                ))
            
            connection.commit()
            return True
        except Exception as e:
            print(f"Error registering matches: {e}")
            connection.rollback()
            return False
        finally:
            if connection:
                connection.close()
    
    def get_matches_by_round(self, round_number: int) -> List[Dict]:
        """
        Busca os dados brutos das partidas de uma rodada específica no banco de dados.
        
        Args:
            round_number (int): Número da rodada desejada
            
        Returns:
            List[Dict]: Lista de dicionários com os dados das partidas
                       Retorna lista vazia se não encontrar partidas ou ocorrer erro
        """
        connection = None
        cursor = None
        
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    id,
                    round_number,
                    match_number,
                    home_team_id,
                    away_team_id,
                    time,
                    date,
                    home_goals,
                    away_goals,
                    has_occurred,
                    is_postponed
                FROM `match`
                WHERE round_number = %s
                ORDER BY match_number
            """
            
            cursor.execute(query, (round_number,))
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Error fetching matches for round {round_number}: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def register_matches_score(self, matches_data: List[Dict]):
        """
        Atualiza os placares das partidas no banco de dados.
        
        Args:
            matches_data (List[Dict]): Lista de dicionários com os dados das partidas a serem atualizadas
                                    Cada dicionário deve conter:
                                    - id: ID da partida
                                    - home_goals: Gols do time da casa
                                    - away_goals: Gols do time visitante
                                    - has_occurred: Se a partida ocorreu
                                    - is_postponed: Se a partida foi adiada
        
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário
        """
        connection = None
        cursor = None
        
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()
            
            for match in matches_data:
                query = """
                    UPDATE `match`
                    SET 
                        home_goals = %s,
                        away_goals = %s,
                        has_occurred = %s,
                        is_postponed = %s
                    WHERE id = %s
                """
                
                cursor.execute(query, (
                    match['home_goals'],
                    match['away_goals'],
                    match['has_occurred'],
                    match['is_postponed'],
                    match['id']
                ))
            
            connection.commit()
            return True
        except Exception as e:
            print(f"Error updating matches scores: {e}")
            if connection:
                connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def get_latest_results_for_team(self, team_id: int, current_round: int) -> List[Dict]:
        """
        Retorna os jogos já ocorridos (não adiados) de um time até a rodada atual, incluindo-a se aplicável.

        Args:
            team_id (int): ID do time
            current_round (int): Número da rodada atual

        Returns:
            List[Dict]: Lista de dicionários com os campos:
                        - home_team_id
                        - away_team_id
                        - home_goals
                        - away_goals
                        Ordenados da rodada mais recente para a mais antiga.
        """
        connection = None
        cursor = None

        try:
            connection = self.db.create_connection()
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    home_team_id,
                    away_team_id,
                    home_goals,
                    away_goals
                FROM `match`
                WHERE
                    round_number <= %s
                    AND (home_team_id = %s OR away_team_id = %s)
                    AND has_occurred = TRUE
                    AND is_postponed = FALSE
                ORDER BY round_number DESC
            """

            cursor.execute(query, (current_round, team_id, team_id))
            return cursor.fetchall()

        except Exception as e:
            print(f"Error fetching latest results for team {team_id}: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def persist_is_postpone(self, round_number: int, match_number: int, is_postponed: bool) -> bool:
        """
        Atualiza o status de adiamento (is_postponed) de uma partida específica.
        
        Args:
            round_number (int): Número da rodada da partida
            match_number (int): Número da partida na rodada
            is_postponed (bool): Novo status de adiamento (True/False)
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário
        """
        connection = None
        cursor = None
        
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()
            
            query = """
                UPDATE `match`
                SET is_postponed = %s
                WHERE round_number = %s AND match_number = %s
            """
            
            cursor.execute(query, (is_postponed, round_number, match_number))
            
            connection.commit()
            return True
        except Exception as e:
            print(f"Error updating is_postponed status for match {match_number} in round {round_number}: {e}")
            if connection:
                connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()