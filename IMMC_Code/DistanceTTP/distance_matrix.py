import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance (in km) between two points
    on Earth using their latitude/longitude.
    """
    R = 6371.0  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# Read CSV data
df = pd.read_csv('team_locations.csv')  # Replace with your file path
teams = df['Teams'].tolist()
n = len(teams)

# Initialize distance matrix
distance_matrix = np.zeros((n, n))

# Fill matrix with Haversine distances
for i in range(n):
    for j in range(n):
        if i != j:
            lat1, lon1 = df.loc[i, 'Latitude'], df.loc[i, 'Longitude']
            lat2, lon2 = df.loc[j, 'Latitude'], df.loc[j, 'Longitude']
            distance_matrix[i][j] = haversine(lat1, lon1, lat2, lon2)

# Convert to DataFrame for readability
distance_df = pd.DataFrame(distance_matrix, index=teams, columns=teams)
print(distance_df)

# Save to CSV
distance_df.to_csv('team_distances.csv')