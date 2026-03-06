import csv

result = [[0, 1, 3, 8], [2, 5, 6, 14], [4, 9, 13, 15], [7, 10, 11, 12]]
teams = [
    "Real Madrid",
    "Manchester City",
    "Bayern Munchen",
    "Borussia Dortmund",
    "Al Ahly",
    "ES Tunis",
    "Mamelodi Sundowns",
    "Pachuca",
    "Al-Hilal",
    "América",
    "Monterrey",
    "Columbus Crew",
    "Al Ain",
    "Yokohama F. Marinos",
    "Auckland City",
    "Pirae"
]


def string_to_nested_list(s):
    # Remove parentheses and split into groups
    groups = s.strip()[1:-1].split(') (')
    # Split each group into numbers and convert to integers
    return [[int(num)-1 for num in group.split()] for group in groups]

# Example usage
result = []
with open('input.csv') as f:
    reader = csv.reader(f)
    for data in reader:
        my_data = data[0][data[0].find('('):]
        new_data = string_to_nested_list(my_data)
        
        result.append(new_data)

with open('../Group_generator/combination.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(result)  # Each sublist is a row


