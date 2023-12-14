import pandas as pd

# Load the dataset
file_path = 'TheAgeDatasetV5.csv'
age_data = pd.read_csv(file_path)

# Determine the range of years to consider
min_year = age_data['Birth year'].min()
max_year = age_data['Death year'].max()

# Initialize a dictionary to hold the counts for each country
country_counts = {}

# Iterate through each year in the range
for year in range(min_year, max_year + 1):
    # Filter the dataset to find individuals who were alive in that year
    alive_people = age_data[(age_data['Birth year'] <= year) & (age_data['Death year'] >= year)]

    # Count the number of alive people for each country in this year
    counts_by_country = alive_people['AssociatedModernCountry'].value_counts().to_dict()

    # Update the main dictionary with the counts for this year
    for country, count in counts_by_country.items():
        if country not in country_counts:
            country_counts[country] = []
        country_counts[country].append(count)

# Create a list of years for reference
years = list(range(min_year, max_year + 1))

# Display the years
print("Years:", years)

# Display the counts for each country
for country, counts in country_counts.items():
    print(f"\n{country}:")
    print("Years: ", years)
    print("Counts:", counts)
