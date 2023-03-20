from fuzzywuzzy import fuzz
import jellyfish
import pandas as pd

valid_cities = ['London', 'Edinburgh']

# Read the Excel file
df1 = pd.read_excel('PD 2019 Wk 2.xlsx', sheet_name='London')
df2 = pd.read_excel('PD 2019 Wk 2.xlsx', sheet_name='Edinburgh')

# Concatenate the two tables
df = pd.concat([df1, df2], ignore_index=True)

# Define a function to match each city name to the closest valid city name
def match_city_name(City):
    # Calculate the Jaro distance between the given city name and each valid city name
    distances = [(valid_city, jellyfish.jaro_distance(City.lower(), valid_city.lower())) for valid_city in valid_cities]
    best_match = max(distances, key=lambda x: x[1])
    if best_match[1] >= 0.8:
        return best_match[0]
    # Use the fuzzywuzzy approach if Jaro distance is less than 0.8
    return process.extractOne(City, valid_cities)[0]

# Apply the match_city_name function to the City column
df['City'] = df['City'].apply(match_city_name)

# Pivot the data based on the 'Metric' column
df_pivot = df.pivot(index=['City', 'Date'], columns='Metric', values='Value').reset_index()

# Save the result as a CSV file
df_pivot.to_csv('week2.csv', index=False)

# Show the resulting dataframe
print(df_pivot)
