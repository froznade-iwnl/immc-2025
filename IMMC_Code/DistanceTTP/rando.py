import pulp as lp


def solve_ttp_corrected(n_teams, distances):
    teams = list(range(1, n_teams + 1))
    slots = list(range(1, 2 * (n_teams - 1) + 1))
    prob = lp.LpProblem("TTP_Corrected", lp.LpMinimize)

    # Variables
    x = lp.LpVariable.dicts("x", [(i, j, t) for i in teams for j in teams for t in slots], cat='Binary')
    w = lp.LpVariable.dicts("w", [(i, j, t) for i in teams for j in teams for t in slots[:-1]], cat='Binary')
    aux = lp.LpVariable.dicts("aux", [(i, j, k, t) for i in teams for j in teams for k in teams for t in slots[:-1]],
                              cat='Binary')

    # Objective (fully linearized)
    prob += lp.lpSum([distances[j - 1][k - 1] * aux[i, j, k, t]
                    for i in teams for j in teams for k in teams for t in slots[:-1]])

    # Constraints
    for i in teams:
        for t in slots:
            prob += lp.lpSum([x[i, j, t] for j in teams]) == 1  # One game per slot
            prob += x[i, i, t] == 0  # No self-play

    for i in teams:
        for j in teams:
            if i != j:
                prob += lp.lpSum([x[i, j, t] + x[j, i, t] for t in slots]) == 2  # Double round-robin
                for t in slots[:-1]:
                    prob += x[i, j, t] + x[j, i, t + 1] <= 1  # No repeat matchups

    for i in teams:
        for t in slots[:-1]:
            prob += lp.lpSum([w[i, j, t] for j in teams]) == 1  # Must be at one venue
            for j in teams:
                prob += w[i, j, t] >= x[i, j, t]  # If playing at j, must be at j
                prob += lp.lpSum([x[i, k, t + 1] for k in teams]) <= 1 + (1 - w[i, j, t])  # Next game reachable

    # Linearization constraints
    for i in teams:
        for j in teams:
            for k in teams:
                for t in slots[:-1]:
                    prob += aux[i, j, k, t] <= w[i, j, t]
                    prob += aux[i, j, k, t] <= x[i, k, t + 1]
                    prob += aux[i, j, k, t] >= w[i, j, t] + x[i, k, t + 1] - 1


    # Solve
    prob.solve()

    # Extract schedule
    schedule = []
    for t in slots:
        matches = [(i, j) for i in teams for j in teams if lp.value(x[i, j, t]) == 1]
        schedule.append((t, matches))

    return schedule


# Example usage
n = 4
distances = [
    [0, 500, 300, 200],
    [500, 0, 600, 400],
    [300, 600, 0, 700],
    [200, 400, 700, 0]
]

schedule = solve_ttp_corrected(n, distances)
for t, matches in schedule:
    print(f"Slot {t}: {', '.join(f'{i} vs {j}' for i, j in matches)}")