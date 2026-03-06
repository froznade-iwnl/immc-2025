import pandas as pd
from bs4 import BeautifulSoup


def extract_table_from_html_file(file_path):

    try:
       
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')

        if table:
            # Convert table to pd
            df = pd.read_html(str(table))[0]
            return df
        else:
            print("No table found pls")
            return None


# Example usage
file_path = 'UEFA.html'
table_data = extract_table_from_html_file(file_path)

if table_data is not None:
    print(table_data)
    table_data.to_csv('UEFA.csv', index=False)


# If you want to extract multiple tables
def extract_all_tables_from_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()


        soup = BeautifulSoup(html_content, 'html.parser')
        tables = soup.find_all('table')

        if tables:
            # Convert all tables to df
            dataframes = pd.read_html(str(tables))
            return dataframes
        else:
            print("No tables found lol.")
            return []