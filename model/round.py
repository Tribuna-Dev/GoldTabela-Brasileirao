class Round:
    
    def __init__(self, id : int, round_number : int, matches : dict, is_round_over : bool, are_matches_registered: bool):
        
        self.id = id
        self.round_number = round_number
        self.matches = matches 
        self.is_round_over = is_round_over
        self.are_matches_registered = are_matches_registered
    
    def get_are_matches_registered(self):
        return self.are_matches_registered
    
    def get_round_number(self):
        return self.round_number
    
    def set_matches(self, matches):
        self.matches = matches
    
    def set_are_matches_registered(self, are_matches_registered : bool):
        self.are_matches_registered = are_matches_registered
    
    def set_is_round_over(self):
        self.is_round_over = True