class Team:
    def __init__(self, id : int, name, stadium, points, matches_played, wins, draws, losses, goals_for, goals_against, goal_difference):
        self.id = id
        self.name = name
        self.stadium = stadium
        self.points = points
        self.matches_played = matches_played
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.goal_difference = goal_difference
    
    def increment_points(self, points : int):
        self.points += points
    
    def increment_wins(self):
        self.wins += 1
    
    def increment_losses(self):
        self.losses += 1 
    
    def increment_draws(self):
        self.draws += 1
    
    def increment_matches_played(self):
        self.matches_played += 1
    
    def increment_goals_for(self, goals : int):
        self.goals_for += goals
    
    def increment_goals_against(self, goals : int):
        self.goals_against += goals
    
    def update_goal_difference(self):
        self.goal_difference = self.goals_for - self.goals_against
    
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_stadium(self):
        return self.stadium

    def get_points(self):
        return self.points

    def get_matches_played(self):
        return self.matches_played

    def get_wins(self):
        return self.wins

    def get_draws(self):
        return self.draws

    def get_losses(self):
        return self.losses

    def get_goals_for(self):
        return self.goals_for

    def get_goals_against(self):
        return self.goals_against

    def get_goal_difference(self):
        return self.goal_difference