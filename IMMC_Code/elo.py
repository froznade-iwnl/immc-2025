class Team:
    def __init__(self, name, elo=800):
        self.name = name
        self.elo = elo

    def show(self):
        print(f"Team: {self.name}, Elo: {self.elo}")

    def update(self, new_elo, stage):
        if stage == 'playoffs':
            self.elo = max(self.elo, new_elo)
        else:
            self.elo = new_elo


class League:
    def __init__(self):
        self.teams = {}

    def get_or_create_team(self, team_name):
        """
        Retrieve an existing team or create a new one if it doesn't exist.
        Insert! yayyy
        """
        if team_name not in self.teams:
            new_team = Team(team_name)
            self.teams[team_name] = new_team

        return self.teams[team_name]

    def update(self, team1_name, team2_name, score, stage, penalty=-1):
        """
        Update Elo ratings for two teams based on match result.

        team1_name: Name of the first team
        team2_name: Name of the second team
        score: Match score in 'a-b' format
        stage: Stage of play (group stage or playoffs)
        penalty: Penalty shootout result! (-1 for no penalty, or 'a-b' format)
        """
        # Get or create teams
        team1 = self.get_or_create_team(team1_name)
        team2 = self.get_or_create_team(team2_name)

        # Determine K-factor based on stage
        k = 25 if stage == 'playoffs' else 15

        # Calculate Elo difference
        elo_diff = team2.elo - team1.elo

        # Calculate expected outcome (Wo)
        wo1 = 1 / (1 + 10 ** (elo_diff / 400))
        wo2 = 1 / (1 + 10 ** -(elo_diff / 400))

        # Parse the score
        a, b = map(int, score.split('-'))

        # Determine actual outcome (W)
        if penalty == -1:
            # Regular match
            if a > b:
                w = 1  # team1 wins
            elif a < b:
                w = 0  # team1 loses
            else:
                w = 0.5  # draw
        else:
            # Penalty shootout
            if '-' in str(penalty):
                penalty_a, penalty_b = map(int, str(penalty).split('-'))
                if penalty_a > penalty_b:
                    w1, w2 = 0.75, 0.5  # team1 wins penalty shootout
                elif penalty_a < penalty_b:
                    w1, w2 = 0.5, 0.75  # team2 wins penalty shootout
                else:
                    w1, w2 = 0.5, 0.5  # draw in penalty shootout

                # Update Elo for both teams during penalty shootout
                team1.update(team1.elo + k * (w1 - wo1), stage)
                team2.update(team2.elo + k * (w2 - wo2), stage)
                return

        # Update Elo for team1
        team1.update(team1.elo + k * (w - wo1), stage)

        # Update Elo for team2
        team2.update(team2.elo + k * ((1-w) - wo2), stage)


#Test Cases
def main():
    league = League()

    league.update("Team A", "Team B", "3-1", "group stage")

    league.teams["Team A"].show()
    league.teams["Team B"].show()


    league.update("Team B", "Team A", "2-2", "group stage")

    league.teams["Team A"].show()
    league.teams["Team B"].show()

    league.update("Team A", "Team B", "2-2", "playoffs", "4-3")

    league.teams["Team A"].show()
    league.teams["Team B"].show()


if __name__ == "__main__":
    main()