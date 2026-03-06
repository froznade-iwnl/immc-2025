import numpy as np
import pandas as pd
import itertools

class TeamGroupOptimizer:
    def __init__(self, csv_path):
        """
        Initialize optimizer with predefined distance matrix

        :param csv_path: Path to CSV file containing distance matrix
        """
        # Read the CSV file
        df = pd.read_csv(csv_path, index_col=0)

        # Convert to numpy array
        self.distance_matrix = df.to_numpy()
        self.team_names = df.index.tolist()
        self.leader_teams = df.columns.tolist()
        print(self.team_names)
        print(self.leader_teams)

    def split_into_equal_groups(self, lst, group_size):
        if len(lst) % group_size != 0:
            return []
        if len(lst) == 0:
            return [[]]

        first_element = lst[0]
        remaining_elements = lst[1:]
        groups = []

        # Generate all possible groups that include the first element
        for combo in itertools.combinations(remaining_elements, group_size - 1):
            current_group = [first_element] + list(combo)
            new_remaining = [x for x in remaining_elements if x not in combo]

            for subgroup in self.split_into_equal_groups(new_remaining, group_size):
                grouping = [sorted(current_group)] + subgroup
                # Sort the grouping to avoid order-dependent duplicates
                sorted_grouping = sorted([sorted(group) for group in grouping])
                # Convert to a tuple of tuples for hashing
                tuple_grouping = tuple(tuple(group) for group in sorted_grouping)
                if tuple_grouping not in groups:
                    groups.append(tuple_grouping)

        # Convert back to a list of lists
        return [list(map(list, grouping)) for grouping in groups]

    def optimize_groups(self):
        """
        Optimize team grouping with predetermined group leaders

        :return: Optimal groups and their metrics
        """
        # Remaining teams (excluding leaders)
        remaining_teams = [
            team for team in self.team_names
            if team not in self.leader_teams
        ]

        # Find best group configuration
        best_result = None
        best_variance = float('inf')

        group_size = 4  # Split into 4 groups of 2
        groups = self.split_into_equal_groups(remaining_teams, group_size)

        return groups



csv_path = 'data.csv'

# Create optimizer
optimizer = TeamGroupOptimizer(csv_path)
# groups = optimizer.optimize_groups()