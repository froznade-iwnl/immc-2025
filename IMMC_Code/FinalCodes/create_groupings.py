import csv
import pandas as pd
import ast
import matplotlib.pyplot as plt
# from Group_generator.calculate_cost import distance_matrix


class TeamGroupOptimizer:
    def __init__(self, csv_path, combi_path):

        # Read the CSV file
        df = pd.read_csv(csv_path, index_col=0)

        # Convert to numpy array
        self.distance_matrix = df.to_numpy()
        self.team_names = df.index.tolist()
        self.leader_teams = df.columns.tolist()
        self.group_combi = []

        #Extract all possible combination from file for brute forcing
        with open(combi_path) as f:
            reader = csv.reader(f)
            for data in reader:
                self.group_combi.append(list(map(lambda x: ast.literal_eval(x), data)))
        print(self.group_combi[:5])


    def calculate_group_metrics(self, group_members):
        """
        Calculate metrics for groups using predefined distances
        """

        # Calculate group distances
        final_group_cost = 0
        for leader_idx, group in enumerate(group_members):

            group_cost = 0

            # Calculate group distance using predefined matrix
            for i, team in enumerate(group):
                group_cost += self.distance_matrix[team, leader_idx]

            final_group_cost += group_cost

        return {
            'named_groups': group_members,
            'group_cost':final_group_cost,
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
            result = self.calculate_group_metrics(combi)
            costs.append(result['group_cost'])

            # Update best result if variance is lower
            if result['group_cost'] < min_cost:
                min_cost = result['group_cost']
                best_result = result

        groups = [[self.leader_teams[leader]] + [self.team_names[index] for index in group] for leader, group in enumerate(best_result['named_groups'])]
        best_result['named_groups'] = groups
        best_result['costs'] = costs

        return best_result


def main():
    # Path to the CSV file
    csv_path = 'P4_T16.csv'
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

    #Generate plot
    plt.figure(figsize=(8, 4))  # Set figure size
    x_values = range(len(results['costs']))
    plt.scatter(x_values, results['costs'], marker='o', color='blue', s=0.1)  # Line plot with markers
    plt.title("Incompatibility Scatter Plot")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()