import pandas as pd
from elo import Team, League
import os


def export_league_standings(league, league_name, output_dir='standings'):
    """
    Export league standings to a CSV file.

    league: League object
    league_name: Name of the league
    output_dir: Directory to save standings files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create a list of dictionaries with team standings
    standings = []
    for rank, team in enumerate(
            sorted(league.teams.values(), key=lambda t: t.elo, reverse=True),
            1
    ):
        standings.append({
            'Rank': rank,
            'Team': team.name,
            'Elo Rating': round(team.elo, 2)
        })

    # Convert to DataFrame
    standings_df = pd.DataFrame(standings)

    # Create output filename
    output_file = os.path.join(output_dir, f'{league_name}_standings.csv')

    # Export to CSV
    standings_df.to_csv(output_file, index=False)

    print(f"{league_name} League standings exported to {output_file}")

    # Also print to console
    print(f"\n{league_name} League Standings:")
    print(standings_df.to_string(index=False))

def get_league_files():
    """
    Identify league files based on the naming convention.

    returns Dictionary of leagues with their group and playoff files
    """
    leagues = ['CONCACAF', 'CONMEBOL', 'AFC', 'OFC', 'CAF', 'UEFA']
    league_files = {}

    # Find matching files in the current directory
    files = os.listdir('.')

    for league in leagues:
        # Find group and playoff files for each league
        group_files = [f for f in files if f.startswith(f'{league}_') and 'Groups' in f]
        playoff_files = [f for f in files if f.startswith(f'{league}_') and 'Playoffs' in f]

        # Ensure exactly onb  e group and one playoff file for each league
        if len(group_files) == 1 and len(playoff_files) == 1:
            league_files[league] = {
                'group_stage': group_files[0],
                'playoffs': playoff_files[0]
            }
        elif len(group_files) > 1 or len(playoff_files) > 1:
            print(f"Warning: Multiple files found for {league}. Skipping.")

    return league_files

def merge_match_data(group_stage_file, playoffs_file):
    """
    Merge match data from two CSV files.

    group_stage_file: Path to the group stage CSV file
    playoffs_file: Path to the playoffs CSV file
    returns DataFrame with merged match data
    """
    try:
        # Read group stage CSV
        group_stage_df = pd.read_csv(group_stage_file)
        group_stage_df['stage'] = 'group stage'
        group_stage_df['Penalty'] = -1

        # Select and rename columns
        group_stage_df = group_stage_df[['Team 1', 'Team 2', 'Score', 'stage', 'Penalty']]

        # Read playoffs CSV
        playoffs_df = pd.read_csv(playoffs_file)
        playoffs_df['stage'] = 'playoffs'

        # Handle missing or default penalties
        playoffs_df['Penalty'] = playoffs_df['Penalty'].fillna('-')
        playoffs_df.loc[playoffs_df['Penalty'] == '-', 'Penalty'] = -1

        # Select and rename columns
        playoffs_df = playoffs_df[['Team 1', 'Team 2', 'Score', 'stage', 'Penalty']]

        # Concatenate the two DataFrames
        merged_df = pd.concat([group_stage_df, playoffs_df], ignore_index=True)
        print(merged_df)
        return merged_df

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()


def merge_match_data_to_list(group_stage_file, playoffs_file):
    """
    Merge match data from two CSV files into a list.

    group_stage_file: Path to the group stage CSV file
    playoffs_file: Path to the playoffs CSV file
    returns List of matches
    """
    # Get merged DataFrame
    merged_df = merge_match_data(group_stage_file, playoffs_file)

    # Convert to list of lists
    matches = merged_df.values.tolist()

    return matches


def calculate_league_elo(group_stage_file, playoffs_file):
    """
    Calculate Elo ratings for teams based on match data.

    group_stage_file: Path to the group stage CSV file
    playoffs_file: Path to the playoffs CSV file
    returns League object with updated Elo ratings
    """
    # Merge match data
    matches_df = merge_match_data(group_stage_file, playoffs_file)

    # Create a League instance
    league = League()

    # Process each match
    for _, match in matches_df.iterrows():
        # Update Elo ratings for the match
        league.update(
            team1_name=match['Team 1'],
            team2_name=match['Team 2'],
            score=match['Score'],
            stage=match['stage'],
            penalty=match['Penalty']
        )

    return league


def print_league_standings(league):
    """
    Print league standings sorted by Elo rating.

     league: League object
    """
    # Sort teams by Elo rating in descending order
    sorted_teams = sorted(
        league.teams.values(),
        key=lambda team: team.elo,
        reverse=True
    )

    print("\nLeague Standings:")
    print("Rank | Team | Elo Rating")
    print("-" * 30)

    for rank, team in enumerate(sorted_teams, 1):
        print(f"{rank:4d} | {team.name:20s} | {team.elo:.2f}")

# Example usage
def main():
    # Get league files
    league_files = get_league_files()

    # Process each league
    for league_name, files in league_files.items():
        print(f"\nProcessing {league_name} League:")

        # Calculate Elo ratings
        league = calculate_league_elo(
            files['group_stage'],
            files['playoffs']
        )

        # Export league standings
        export_league_standings(league, league_name)

if __name__ == "__main__":
    main()