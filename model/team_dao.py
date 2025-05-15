from typing import List, Dict, Any
from model.database import Database

class TeamDAO:
    
    def __init__(self):
        self.db = Database()
    
    def __enter__(self):
        """Abre a conexão quando usado em um context manager"""
        self.conn = self.db.create_connection()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fecha a conexão ao sair do context manager"""
        if self.conn:
            self.conn.close()
    
    def _ensure_connection(self):
        """Garante que a conexão está aberta"""
        if self.conn is None:
            self.conn = self.db.create_connection()
        # Verifica se a conexão ainda está válida
        try:
            self.conn.ping(reconnect=True)  # Testa e reconecta se necessário
        except:
            self.conn = self.db.create_connection()
    
    def get_all_teams_data(self) -> List[Dict[str, Any]]:
        """
        Busca todos os times cadastrados no banco de dados
        Retorna uma lista de dicionários com todos os campos da tabela team
        """
        conn = self.db.create_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT 
                    id,
                    name,
                    stadium,
                    points,
                    matches_played,
                    wins,
                    draws,
                    losses,
                    goals_for,
                    goals_against,
                    goal_difference
                FROM team
                ORDER BY name
            """)
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Erro ao buscar todos os times: {str(e)}")
            return []
        finally:
            cursor.close()
            self.db.close_connection()
    
    def update_team_stats(
        self,
        team_id: int,
        points: int,
        matches_played: int,
        wins: int,
        draws: int,
        losses: int,
        goals_for: int,
        goals_against: int,
        goal_difference: int
    ) -> bool:
        """Atualiza as estatísticas de um time no banco de dados"""
        self._ensure_connection()
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE team
                SET 
                    points = %s,
                    matches_played = %s,
                    wins = %s,
                    draws = %s,
                    losses = %s,
                    goals_for = %s,
                    goals_against = %s,
                    goal_difference = %s
                WHERE id = %s
            """, (
                points,
                matches_played,
                wins,
                draws,
                losses,
                goals_for,
                goals_against,
                goal_difference,
                team_id
            ))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar time {team_id}: {str(e)}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
    
    