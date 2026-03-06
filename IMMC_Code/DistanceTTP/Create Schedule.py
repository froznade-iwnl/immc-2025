import csv


def generate_schedule(team_names, matrix):
    num_teams = len(team_names)
    num_weeks = len(matrix[0])

    # Initialize schedule dictionary
    schedule = {team: [] for team in team_names}
    weeks = {week + 1: [] for week in range(num_weeks)}

    # Process each week
    for week in range(num_weeks):
        # Track matches to ensure no duplicates
        week_matches = set()

        for idx, team in enumerate(team_names):
            opponent_idx = matrix[idx][week]
            away = False

            if opponent_idx >= 0:
                away = True

            opponent = team_names[abs(opponent_idx) - 1]

            # Ensure we don't add duplicate matches
            match_key = tuple(sorted([team, opponent]))
            if match_key not in week_matches and opponent != 'Dummy':
                full_match_description = f'{team if away else team + " (H)"} vs {opponent if not away else opponent + " (H)"}'
                schedule[team].append(opponent + (' (Away)' if away else ''))
                weeks[week + 1].append(full_match_description)
                week_matches.add(match_key)

    return schedule, weeks


def print_schedule(schedule, team_names):
    # Print header
    print("Team | " + " | ".join(f"Week {i + 1}" for i in range(len(next(iter(schedule.values()))))))

    # Print each team's schedule
    for team in team_names:
        print(f"{team} | " + " | ".join(schedule[team]))


def save_to_csv(schedule, team_names, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        header = ['Team'] + [f'Week {i + 1}' for i in range(len(next(iter(schedule.values()))))]
        writer.writerow(header)

        # Write each team's schedule
        for team in team_names:
            row = [team] + schedule[team]
            writer.writerow(row)


def save_week(weeks, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Dynamically create header based on max matches in a week
        max_matches = max(len(matches) for matches in weeks.values())
        header = ['Week'] + [f'Match {i + 1}' for i in range(max_matches)]
        writer.writerow(header)

        # Write each week's matches
        for week, matches in weeks.items():
            row = [week] + matches + [''] * (max_matches - len(matches))
            writer.writerow(row)


# Example usage

# Team D
team_names = ["Real Madrid", 'Al-Hilal', 'Al Ahly',	'ES Tunis',	'Al Ain', 'Dummy']
matrix = [
  [6, 4, 5, -6, -5, 3, 2, -4, -2, -3],
  [-5, -6, 3, 4, 6, -4, -1, -3, 1, 5],
  [-4, -5, -2, 5, 4, -1, -6, 2, 6, 1],
  [3, -1, 6, -2, -3, 2, 5, 1, -5, -6],
  [2, 3, -1, -3, 1, 6, -4, -6, 4, -2],
  [-1, 2, -4, 1, -2, -5, 3, 5, -3, 4]
]

# Team C
# team_names = ["Atlético Mineiro", "Monterrey", "Mamelodi Sundowns", "Auckland City", "Pirae", "Dummy"]
# matrix = [
#     [2, -4, -5, 6, 4, -3, 5, -6, -2, 3],
#     [-1, -3, -4, 3, 6, 5, -6, 4, 1, -5],
#     [6, 2, -6, -2, -5, 1, -4, 5, 4, -1],
#     [5, 1, 2, -5, -1, -6, 3, -2, -3, 6],
#     [-4, -6, 1, 4, 3, -2, -1, -3, 6, 2],
#     [-3, 5, 3, -1, -2, 4, 2, 1, -5, -4]
# ]

#Team B
# team_names = ["Manchester City", "Bayern Munchen", "Borussia Dortmund", "Columbus Crew", "Yokohama F. Marinos", "Dummy"]
# matrix = [
#     [4, -2, 3, 2, -3, 6, -4, -5, -6, 5],
#     [-3, 1, -6, -1, 6, 4, -5, 3, 5, -4],
#     [2, 5, -1, -4, 1, -5, -6, -2, 4, 6],
#     [-1, -6, -5, 3, 5, -2, 1, 6, -3, 2],
#     [-6, -3, 4, 6, -4, 3, 2, 1, -2, -1],
#     [5, 4, 2, -5, -2, -1, 3, -4, 1, -3]
# ]

#Team A
# team_names = ["River Plate", "Botafogo", "Pachuca", "Peñarol", "América", "Dummy"]
# matrix = [
#     [-4, -5, 4, 2, -3, -6, -2, 3, 5, 6],
#     [5, -6, 3, -1, 6, -4, 1, 4, -3, -5],
#     [6, -4, -2, 5, 1, -5, -6, -1, 2, 4],
#     [1, 3, -1, -6, -5, 2, 5, -2, 6, -3],
#     [-2, 1, 6, -3, 4, 3, -4, -6, -1, 2],
#     [-3, 2, -5, 4, -2, 1, 3, 5, -4, -1]
# ]

schedule, weeks = generate_schedule(team_names, matrix)
# print_schedule(schedule, team_names)

# Save to CSV
save_to_csv(schedule, team_names, 'team_schedule_D.csv')
save_week(weeks, 'weekly_schedule_D.csv')
print("\nSchedule has been saved.")