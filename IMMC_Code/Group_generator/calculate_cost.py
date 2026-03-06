import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2
from haversine import haversine, Unit



def calculate_travel_cost(team1, team2):
    """
    Calculate travel cost based on ELO difference and geo dist
    """
    # Calculate ELO difference
    elo_diff = abs(team1['Real ELO'] - team2['Real ELO'])
    print(team1.keys)

    # haversine formula
    point_1 = team1['Latitude'], team1['Longitude']
    point_2 = team2['Latitude'], team2['Longitude']
    geo_distance = haversine(point_1, point_2)

    return elo_diff*elo_diff + 4*geo_distance


def create_distance_matrix(df):
    """
    Create distance matrix for 2 round robin tourney.
    """
    # Number of teams
    n = len(df)

    # Initialize distance matrix with string indicators
    distance_matrix = np.full((n, n), '-', dtype=object)
    np.fill_diagonal(distance_matrix, 0)

    # Calculate costs for all pair combinations
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i, j] = round(calculate_travel_cost(df.iloc[i], df.iloc[j]), 2)

    matrix_df = pd.DataFrame(
        distance_matrix,
        columns=df['Teams'],
        index=df['Teams']
    )

    return matrix_df


# Read the CSV data
df = pd.read_csv('ELO Rating Clubs - GSL Standing_plus_four.csv')
df = df.drop_duplicates(subset=['Teams'])

# Calculate and display the distance matrix
distance_matrix = create_distance_matrix(df)

# Outputs
print(distance_matrix)
distance_matrix.to_csv('tournament_distance_matrix_2.csv')