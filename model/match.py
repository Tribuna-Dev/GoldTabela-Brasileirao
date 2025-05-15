class Match:
    
    def __init__(self, id : int, round_number :int, match_number : int, home_team_id : int, away_team_id : int, time, date, home_goals, away_goals, has_occurred, is_postponed):
        self.id = id
        self.round_number = round_number
        self.match_number = match_number
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.time = time
        self.date = date
        self.home_goals = home_goals
        self.away_goals = away_goals
        self.has_occurred = has_occurred
        self.is_postponed = is_postponed
    
    def set_home_goals(self, goals):
        self.home_goals = goals
    
    def set_away_goals(self, goals):
        self.away_goals = goals
        
    def set_is_postponed(self, is_postponed : bool):
        self.is_postponed = is_postponed
        
    def set_has_occurred(self, has_occurred : bool):
        self.has_occurred = has_occurred
    
    def get_match_number(self):
        return self.match_number
    
    def get_has_occurred(self):
        return self.has_occurred
    
    def get_time(self):
        return self.time
    
    def get_home_team_id(self):
        return self.home_team_id
    
    def get_away_team_id(self):
        return self.away_team_id
    
    def get_home_goals(self):
        return self.home_goals
    
    def get_away_goals(self):
        return self.away_goals
    
    
        