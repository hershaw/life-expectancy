"""
Assignment 1 of academy NOS foundations
"""

# pylint: disable=missing-function-docstring

# import pandas libraries
import pandas as pd

def load_datafile() -> pd.DataFrame:
    #filepath = 'life_expectancy/data/eu_life_expectancy_raw.tsv'
    filepath = 'data/eu_life_expectancy_raw.tsv'
    return pd.read_csv(filepath, sep='\t')

def rearrange_columns(df_life_expectancy: pd.DataFrame) -> None:
    # Remove "time" from column name
    df_life_expectancy.rename(columns = {'unit,sex,age,geo\\time': 'unit,sex,age,geo'},
                              inplace = True)

    # Split aggregated column in 4 columns
    df_life_expectancy[['unit','sex','age','region']] = \
        df_life_expectancy['unit,sex,age,geo'].str.split(',', expand = True)

    # Remove  aggregated column
    del df_life_expectancy['unit,sex,age,geo']

    # Move the splited columns to the start of df_life_expectancy
    cols = list(df_life_expectancy.columns)
    cols = cols[-4:] + cols[:-4]
    df_life_expectancy = df_life_expectancy[cols]

def unpivot_date(df_life_expectancy: pd.DataFrame) -> pd.DataFrame:
    return df_life_expectancy.melt(id_vars=['unit', 'sex', 'age', 'region'],
                                   var_name='year', value_name='value')

def filter_time_empty_values(df_unpivoted: pd.DataFrame) -> pd.DataFrame:
    """ Remove rows with value=':' """
    return df_unpivoted[df_unpivoted.value.str.strip() != ':']

def change_year_dtype_to_int(df_unpivoted: pd.DataFrame) -> None:
    df_unpivoted['year'] = df_unpivoted['year'].astype(int)

def remove_letters_from_value_column(df_unpivoted: pd.DataFrame) -> None:
    df_unpivoted['value'] = df_unpivoted.value.str.replace(r'[a-zA-Z]+', '', regex=True)

def change_value_dtype_to_float(df_unpivoted: pd.DataFrame) -> None:
    df_unpivoted['value'] = df_unpivoted['value'].astype(float)

def filter_region(df_unpivoted: pd.DataFrame) -> pd.DataFrame:
    return df_unpivoted[df_unpivoted.region == 'PT']

def save_dataframe_as_csv(df_unpivoted: pd.DataFrame) -> None:
    """ Set the prefix of filename with region and saves the dataframe as CVS"""

    filepath = 'data/' + 'pt' + '_life_expectancy.csv'
    df_unpivoted.to_csv(filepath, index = False)


def clean_data() -> None:
    """Cleaning of life expectancy file"""

    df_life_expectancy = load_datafile()

    rearrange_columns(df_life_expectancy)

    df_unpivoted = unpivot_date(df_life_expectancy)

    df_unpivoted = filter_time_empty_values(df_unpivoted)

    change_year_dtype_to_int(df_unpivoted)

    remove_letters_from_value_column(df_unpivoted)

    change_value_dtype_to_float(df_unpivoted)

    df_unpivoted = filter_region(df_unpivoted)

    save_dataframe_as_csv(df_unpivoted)

if __name__ == "__main__":  # pragma: no cover
    clean_data()
