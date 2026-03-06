import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment

# Read all CSV files
df_a = pd.read_csv('weekly_schedule_A.csv')
df_b = pd.read_csv('weekly_schedule_B.csv')
df_c = pd.read_csv('weekly_schedule_C.csv')
df_d = pd.read_csv('weekly_schedule_D.csv')

# Create a new Excel workbook
wb = Workbook()
ws = wb.active
ws.title = "Combined Schedule"

# Write headers
headers = ["Week", "Group A", "Group B", "Group C", "Group D"]
ws.append(headers)

# Merge data from all groups
max_weeks = max(len(df_a), len(df_b), len(df_c), len(df_d))

for week in range(1, max_weeks + 1):
    # Get matches for each group
    matches_a = df_a[df_a['Week'] == week].iloc[:, 1:].dropna(axis=1).values.flatten().tolist()
    matches_b = df_b[df_b['Week'] == week].iloc[:, 1:].dropna(axis=1).values.flatten().tolist()
    matches_c = df_c[df_c['Week'] == week].iloc[:, 1:].dropna(axis=1).values.flatten().tolist()
    matches_d = df_d[df_d['Week'] == week].iloc[:, 1:].dropna(axis=1).values.flatten().tolist()

    # Find max matches for this week across all groups
    max_matches = max(len(matches_a), len(matches_b), len(matches_c), len(matches_d))

    # Write week number only in first row
    if max_matches > 0:
        ws.append([week] + [matches_a[0] if len(matches_a) > 0 else ""] +
                  [matches_b[0] if len(matches_b) > 0 else ""] +
                  [matches_c[0] if len(matches_c) > 0 else ""] +
                  [matches_d[0] if len(matches_d) > 0 else ""])

    # Write remaining matches in subsequent rows
    for i in range(1, max_matches):
        ws.append([""] +
                  [matches_a[i] if i < len(matches_a) else ""] +
                  [matches_b[i] if i < len(matches_b) else ""] +
                  [matches_c[i] if i < len(matches_c) else ""] +
                  [matches_d[i] if i < len(matches_d) else ""])

# Formatting
for row in ws.iter_rows():
    for cell in row:
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

# Save the Excel file
wb.save("combined_schedule.xlsx")