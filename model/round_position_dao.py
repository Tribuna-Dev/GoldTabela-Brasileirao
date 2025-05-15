from model.database import Database

class RoundPositionDAO:
    def __init__(self):
        self.db = Database()

    def register_round_position(self, round_number: int, positions: list[tuple[int, int]]) -> bool:
        """
        Registra as posições dos times para uma rodada específica
        
        Args:
            round_number: Número da rodada
            positions: Lista de tuplas contendo (team_id, position)
            
        Returns:
            bool: True se todas as inserções foram bem-sucedidas, False caso contrário
        """
        conn = self.db.create_connection()
        cursor = conn.cursor()
        
        try:
            # Primeiro remove posições existentes para esta rodada (caso seja uma reclassificação)
            cursor.execute(
                "DELETE FROM round_position WHERE round_number = %s",
                (round_number,)
            )
            
            # Insere as novas posições
            cursor.executemany(
                "INSERT INTO round_position (round_number, team_id, position) "
                "VALUES (%s, %s, %s)",
                [(round_number, team_id, position) for team_id, position in positions]
            )
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Erro ao registrar posições da rodada {round_number}: {str(e)}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def get_round_positions(self, round_number: int) -> list[dict]:
        """
        Obtém as posições dos times para uma rodada específica
        
        Args:
            round_number: Número da rodada desejada
            
        Returns:
            Lista de dicionários com as posições no formato:
            [
                {'team_id': int, 'position': int, 'team_name': str},
                ...
            ]
            Retorna lista vazia se não encontrar dados ou em caso de erro
        """
        conn = self.db.create_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(
                "SELECT rp.team_id, rp.position, t.name as team_name "
                "FROM round_position rp "
                "JOIN team t ON rp.team_id = t.id "
                "WHERE rp.round_number = %s "
                "ORDER BY rp.position ASC",
                (round_number,)
            )
            
            return cursor.fetchall() or []
            
        except Exception as e:
            print(f"Erro ao buscar posições da rodada {round_number}: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()