from customtkinter import StringVar
from tkinter import messagebox, filedialog
from utils.event_manager import EventManager
from service.round_service import RoundService
from service.team_service import TeamService 
from service.match_service import MatchService
from service.round_position_service import RoundPositionService

class MainWindowController:
    
    def __init__(self, round_service : RoundService, team_sevice : TeamService, match_service : MatchService, round_position_service : RoundPositionService):
        
        self._round_select_number = None
        self.round_service = round_service
        self.team_service = team_sevice
        self.match_service = match_service
        self.round_position_service = round_position_service
        self.current_round_number = round_service.get_first_unfinished_round_number()
    
    @property
    def round_select_number(self):

        if self._round_select_number is None:
            self._round_select_number = StringVar()
        
        return self._round_select_number
    
    def handle_round_selection(self):
        """Gerencia a seleção de rodada e publica o evento correspondente.
        
        Verifica:
        - Se uma rodada foi selecionada
        - Se a rodada está cadastrada no sistema
        Caso válido, publica um evento com os dados necessários para a view.
        """
        try:
            round_number = int(self.round_select_number.get().strip())
            
            if not round_number:
                messagebox.showinfo("Aviso", "Selecione uma rodada válida.")
                return
            
            current_round = self.round_service.get_round_by_number(round_number)
            
            EventManager.publish(
                "ROUND_SELECTED", 
                {
                    'are_matches_registered': current_round.get_are_matches_registered(),
                    'round_number': current_round.get_round_number(),
                    'current_round_number' : self.current_round_number
                }
            )
            
        except ValueError:
            messagebox.showerror("Erro", "Número de rodada inválido.")
    
    def export_championship_table(self):
        
        standings = {
        1: ">libertadores<1º",
        2: ">libertadores<2º",
        3: ">libertadores<3º",
        4: ">libertadores<4º",
        5: ">libertadores<5º",
        6: ">libertadores<6º",
        7: ">intermediaria<7º",
        8: ">intermediaria<8º",
        9: ">intermediaria<9º",
        10: ">intermediaria<10º",
        11: ">intermediaria<11º",
        12: ">intermediaria<12º",
        13: ">intermediaria<13º",
        14: ">intermediaria<14º",
        15: ">intermediaria<15º",
        16: ">intermediaria<16º",
        17: ">rebaixamento<17º",
        18: ">rebaixamento<18º",
        19: ">rebaixamento<19º",
        20: ">rebaixamento<20º"}

        destination_directory = filedialog.askdirectory()
    
        path_file = f"{destination_directory}/brasileirao_2025.txt"
    
        try:

            with open(path_file, 'w') as file:

                file.write(">t 16pt,,,,,,<>t 59.106pt,,,,,,<>t 16.896pt,,,,,,<>t 16pt,,,,,,<>t 16pt,,,,,,<>t 16pt,,,,,,<>t 16pt,,,,,,<>t 16pt,,,,,,<>t 16pt,,,,,,<>t 16pt,,,,,,<>t 16pt,,,,,,<>t 48pt,,,,,,<>tab2Cop1<$	TIME		PG	J	V	E	D	GP	GC	SG	Últ. jogos\r\n\r\n")

                ranked_teams = self.team_service.get_teams_ranking()

                for position, team in enumerate(ranked_teams, start=1):
                             
                    change_indicator, positions_changed = self.get_position_change(team.get_id(), self.current_round_number, position, None)
                    team_line = (
                        f"{standings[position]}\t{team.get_name()}"
                        f"\t{change_indicator}{positions_changed}"
                        f"\t{team.get_points()}"
                        f"\t{team.get_matches_played()}"
                        f"\t{team.get_wins()}"
                        f"\t{team.get_draws()}"
                        f"\t{team.get_losses()}"
                        f"\t{team.get_goals_for()}"
                        f"\t{team.get_goals_against()}"
                        f"\t{team.get_goal_difference()}\t"
                    )
                    
                    file.write(team_line)
                    
                    last_matches_result_list = self.match_service.get_team_results_outcomes(team.get_id(), self.current_round_number)
                    
                    for match_result in last_matches_result_list:
                        file.write(match_result)
                    file.write("\r\n")

                file.write(">endtab<\r\n\r\n")
                
                self._write_last_matches_in_file(file)
                
                self._write_upcoming_matches(file)

            file.close()

            messagebox.showinfo("Aviso!", "O arquivo foi gerado com sucesso.")
            
        except Exception as e:
            print(f"Erro ao criar ou escrever no arquivo principal: {e}")
    
    def _write_last_matches_in_file(self, file):
         
        matches =  self.round_service.get_matches_by_round_number(self.current_round_number)
        
        matches_list = self.match_service.get_finished_matches_in_round(matches)
        
        file.write(">na<>tarjamenor1<RESULTADOS\r\n")
        file.write(">na<>tab1Cop1 BOX<>t 115<\r\n")
        
        for match in matches_list:
            home_team = self.team_service.get_team_by_id(match['home_team_id'])
            away_team = self.team_service.get_team_by_id(match['away_team_id'])
            
            file.write(home_team.get_name()	+ "	" + str(match['home_team_goals']) +" x " + str(match['away_team_goals']) + "	" + away_team.get_name() + "\r\n")
            file.write(">main2<" + match['time'] + "Hs - " + home_team.get_stadium() + "\r\n")
    
    def _write_upcoming_matches(self, file):
 
        matches =  self.round_service.get_matches_by_round_number(self.current_round_number)
        
        match_list =  self.match_service.get_upcoming_matches_in_round(matches)
        
        file.write(">na<>tarjamenor1<PRÓXIMOS JOGOS\r\n")
        file.write(">na<>headcinza<\r\n")

        for match in match_list:
            home_team = self.team_service.get_team_by_id(match['home_team_id'])
            away_team = self.team_service.get_team_by_id(match['away_team_id'])
                
            file.write(">time<" + home_team.get_name() + " X " + away_team.get_name() + "\r\n")
            file.write(">main2<" + match['time'] + "Hs - " + home_team.get_stadium() + "\r\n")

    def get_position_change(self, team_id: int, round_number: int, current_position: int, team_name: str) -> list[str]:
        """
        Determines the position change of a team between rounds
        
        Args:
            team_id: ID of the team
            round_number: Current round number
            current_position: Team's current position
            team_name: Team name (only used for round 1)
            
        Returns:
            List with two elements:
            [0]: Change indicator (">up<", ">kept<", ">down<")
            [1]: Number of positions changed (as string)
        """
        position_change_options = {
            1: ">sobe<", 
            0: ">manteve<", 
            -1: ">desce<"
        }
        
        # For round 1, compare with initial championship positions
        if round_number == 1:
            initial_positions = {
                "Atlético-MG":1, "Bahia":2, "Botafogo":3, "Ceará":4, "Corinthians":5,
                "Cruzeiro":6, "Flamengo":7, "Fluminense":8, "Fortaleza":9, "Grêmio":10,
                "Internacional":11, "Juventude":12, "Mirassol":13, "Palmeiras":14,
                "Bragantino":15, "Santos":16, "Sport":17, "São Paulo":18,
                "Vasco":19, "Vitória":20
            }
            
            initial_position = initial_positions.get(team_name, 20)
            change = self._calculate_position_change(current_position, initial_position)
            
            return [
                position_change_options[change],
                str(abs(current_position - initial_position))
            ]
        
        # For other rounds, get previous round position from service
        previous_positions = self.round_position_service.get_round_positions(round_number - 1)
        previous_position = next(
            (pos['position'] for pos in previous_positions if pos['team_id'] == team_id),
            current_position  # Default to current if not found
        )
        
        change = self._calculate_position_change(current_position, previous_position)
        
        return [
            position_change_options[change],
            str(abs(current_position - previous_position))
        ]

    def _calculate_position_change(self, current_pos: int, previous_pos: int) -> int:
        """Helper method to determine position change direction"""
        if current_pos < previous_pos:
            return 1  
        elif current_pos > previous_pos:
            return -1  
        return 0  

