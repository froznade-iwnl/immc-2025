import pandas as pd
import numpy as np
from haversine import haversine, Unit



def calculate_travel_cost(team1, team2):
    """
    Calculate travel cost based on ELO difference and geographic distance
    """
    # Calculate ELO difference
    elo_diff = abs(team1['Real ELO'] - team2['Real ELO'])
    print(team1.keys)

    # haversine formula
    point_1 = team1['Latitude'], team1['Longitude']
    point_2 = team2['Latitude'], team2['Longitude']
    geo_distance = haversine(point_1, point_2)

    return elo_diff*elo_diff + 4*geo_distance


def create_incompability_matrix(df):
    """
    Create a incompability matrix for double round-robin tournament
    """
    # Number of teams
    n = len(df)

    # Initialize incompability matrix with string indicators
    incompability_matrix = np.full((n, n), '-', dtype=object)
    np.fill_diagonal(incompability_matrix, 0)

    # Calculate costs for all pair combinations
    for i in range(n):
        for j in range(n):
            if i != j:
                incompability_matrix[i, j] = round(calculate_travel_cost(df.iloc[i], df.iloc[j]), 2)

    matrix_df = pd.DataFrame(
        incompability_matrix,
        columns=df['Teams'],
        index=df['Teams']
    )

    return matrix_df


# Read the CSV data
df = pd.read_csv('file.csv')
df = df.drop_duplicates(subset=['Teams'])

# Calculate and display the incompability matrix
incompability_matrix = create_incompability_matrix(df)

# Outputs
print(incompability_matrix)
incompability_matrix.to_csv('incompability.csv')