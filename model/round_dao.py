from model.database import Database

class RoundDAO:
    
    def __init__(self):
        self.db = Database()
    
    def get_round_basic_info(self, round_number: int):
        """
        Busca apenas os dados básicos de uma rodada, sem as partidas
        
        Args:
            round_number: Número da rodada desejada
            
        Returns:
            Dicionário com os dados básicos da rodada no formato:
            {
                'round_number': int,
                'is_round_over': bool,
                'are_matches_registered': bool
            }
            Retorna None se a rodada não for encontrada
        """
        conn = self.db.create_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(
                "SELECT id, round_number, is_round_over, are_matches_registered "
                "FROM round WHERE round_number = %s",
                (round_number,)
            )
            
            return cursor.fetchone()
            
        except Exception as e:
            print(f"Erro ao buscar dados da rodada {round_number}: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()

    def set_matches_as_registered(self, round_number: int) -> bool:
        """
        Atualiza o status are_matches_registered para True (1) na rodada especificada
        
        Args:
            round_number: Número da rodada a ser atualizada
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário
        """
        conn = self.db.create_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "UPDATE round SET are_matches_registered = 1 "
                "WHERE round_number = %s",
                (round_number,))
            
            conn.commit()
            return cursor.rowcount > 0  # Retorna True se alguma linha foi afetada
            
        except Exception as e:
            print(f"Erro ao atualizar status da rodada {round_number}: {str(e)}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def get_first_unfinished_round_number(self) -> int | None:
        """
        Retorna apenas o número da primeira rodada não encerrada
        
        Returns:
            int: Número da primeira rodada não encerrada
            None: Se todas as rodadas estiverem encerradas ou não houver rodadas
        """
        conn = self.db.create_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT round_number FROM round "
                "WHERE is_round_over = False "
                "ORDER BY round_number ASC "
                "LIMIT 1"
            )
            
            result = cursor.fetchone()
            return result[0] if result else None
            
        except Exception as e:
            print(f"Erro ao buscar número da rodada não encerrada: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def update_is_round_over(self, round_number: int) -> bool:
        """
        Updates the is_round_over status to True (1) for the specified round
        
        Args:
            round_number: Number of the round to be updated
            
        Returns:
            bool: True if the update was successful, False otherwise
        """
        conn = self.db.create_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "UPDATE round SET is_round_over = 1 "
                "WHERE round_number = %s",
                (round_number,)
            )
            
            conn.commit()
            return cursor.rowcount > 0  # Returns True if any row was affected
            
        except Exception as e:
            print(f"Error updating round status for round {round_number}: {str(e)}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()