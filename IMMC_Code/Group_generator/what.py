from itertools import permutations
import pandas as pd
import matplotlib.pyplot as plt
# from Group_generator.calculate_cost import distance_matrix


class TeamGroupOptimizer:
    def __init__(self, csv_path, combi_path):
        """
        Initialize optimizer with predefined distance matrix

        :param csv_path: Path to CSV file containing distance matrix
        """
        # Read the CSV file
        df = pd.read_csv(csv_path, index_col=0)
        # print(df)

        # Convert to numpy array
        self.distance_matrix = df.to_numpy()
        self.team_names = df.index.tolist()
        self.leader_teams = df.columns.tolist()

        perms = permutations([0, 1, 2, 3])
        self.group_combi = [[[num] for num in perm] for perm in perms]
        # print(self.group_combi)


    def calculate_group_metrics(self, group_members):
        """
        Calculate metrics for groups using predefined distances

        :param group_leaders: Names of group leader teams
        :param group_members: List of team names for each group
        :return: Detailed group metrics
        """

        # Calculate group distances
        final_group_cost = 0
        for leader_idx, group in enumerate(group_members):
            # Calculate group distance using predefined matrix
            group_cost = 0

            for i, team in enumerate(group):
                group_cost += self.distance_matrix[team, leader_idx]

            final_group_cost += group_cost


            # for i, team1 in enumerate(group):
            #     for j, team2 in enumerate(group):
            #         if i < j:
            #             # Use the predefined distance matrix
            #             dist_idx1 = self.team_names.index(team1)
            #             dist_idx2 = self.team_names.index(team2)
            #             group_dist += self.distance_matrix[dist_idx1, dist_idx2]
            # print(final_group_cost)

        return {
            'named_groups': group_members,
            'group_cost':final_group_cost,
            # 'distance_range': max(group_distances) - min(group_distances),
            # 'distance_variance': np.var(group_distances),
            # 'avg_group_distance': np.mean(group_distances)
        }

    def optimize_groups(self):
        """
        Optimize team grouping with predetermined group leaders

        :return: Optimal groups and their metrics
        """

        # Find best group configuration
        best_result = None
        min_cost = float('inf')
        costs = []

        for combi in self.group_combi:
            # Calculate metrics
            print(combi)
            result = self.calculate_group_metrics(combi)
            costs.append(result['group_cost'])

            # Update best result if variance is lower
            if result['group_cost'] < min_cost:
                min_cost = result['group_cost']
                best_result = result

            # print(result['group_cost'])
        groups = [[self.leader_teams[leader]] + [self.team_names[index] for index in group] for leader, group in enumerate(best_result['named_groups'])]
        best_result['named_groups'] = groups
        best_result['costs'] = costs

        return best_result


def main():
    # Path to the CSV file
    csv_path = 'P4_T8.csv'
    combi_path = 'combination.csv'

    # Create optimizer
    optimizer = TeamGroupOptimizer(csv_path, combi_path)

    # Run optimization
    results = optimizer.optimize_groups()
    # results = 0

    #Print results
    print("Optimal Team Groups:")
    for i, group in enumerate(results['named_groups'], 1):
        print(f"Group {i}: {group}")

    print("\nOptimization Metrics:")
    print(f"Group Cost: {results['group_cost']}")
    # print(f"Distance Range: {results['distance_range']}")
    # print(f"Distance Variance: {results['distance_variance']}")
    # print(f"Average Group Distance: {results['avg_group_distance']}")

    plt.figure(figsize=(8, 4))  # Set figure size
    x_values = range(len(results['costs']))
    plt.scatter(x_values, results['costs'], marker='o', color='blue', s=10)  # Line plot with markers
    plt.title("Incompatibility Scatter Plot")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()