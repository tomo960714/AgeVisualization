import pandas as pd

def create_country_year_dict(df, country, year):
    """
    Create a dictionary for a specific country and year with the number of births and deaths.
    :param df: DataFrame containing the data.
    :param country: The country to filter the data by.
    :param year: The year to get the data for.
    :return: A dictionary in the format {'country name': ['year', 'number of births in year', 'number of deaths in year']}
    """

    # Filtering data for the given country
    country_df = df[df["AssociatedModernCountry"] == country]

    # Getting the number of births and deaths in the given year
    births_in_year = country_df[country_df["Birth year"] == year].shape[0]
    deaths_in_year = country_df[country_df["Death year"] == year].shape[0]

    return {country: [year, births_in_year, deaths_in_year]}

# Load the dataset
file_path = 'TheAgeDatasetV5.csv'
df = pd.read_csv(file_path)

# Extracting the unique country names
unique_countries = df['Country'].unique().tolist()

# Extract unique years from 'Birth year' and 'Death year' columns
unique_birth_years = set(df['Birth year'].unique())
unique_death_years = set(df['Death year'].unique())

# Combine both sets to get all unique years
all_unique_years = unique_birth_years.union(unique_death_years)

# Convert to a sorted list (optional)
sorted_years = sorted(all_unique_years)

# Creating a list of tuples for each country and year combination
countries_and_years = [(country, year) for country in unique_countries for year in sorted_years]

# Loop through each country and year, create and print the dictionary
for country, year in countries_and_years:
    country_year_dict = create_country_year_dict(df, country, year)
    print(country_year_dict)

