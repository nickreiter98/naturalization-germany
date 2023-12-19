import pandas as pd

def _load_data() -> pd.DataFrame:
    # Load the data from the csv file
    df = pd.read_csv('naturalization-germany.csv', sep=';', header=[0,1], encoding='ISO-8859-1', skiprows=7, skipfooter=3)
    # Set the index of the dataframe using the first three columns
    df = df.set_index(list(df.columns[0:3]))
    # Rename the index levels to Jahr, Herkunft and Familienstand
    df.index.names = ['jahr', 'herkunft', 'familienstand']
    # Convert all data to numeric values and coerce any errors to NaN
    df = df.apply(pd.to_numeric, errors='coerce')

    # Change index labels to lowercase and replace spaces with underscores
    for i in range(0, df.index.nlevels):
        if df.index.levels[i].dtype == object:
            df.index = df.index.set_levels(df.index.levels[i].str.lower().str.replace(' ', '_'), level=i)

    # Change column labels to lowercase and replace spaces with underscores
    for i in range(0, df.columns.nlevels):
        df.columns = df.columns.set_levels(df.columns.levels[i].str.lower().str.replace(' ', '_'), level=i)


    for gender in df.columns.levels[0]:
        if "unnamed" not in gender:
            # Aggregate single year columns (x-jährige) to period (x_bis_unter_y)
            df[gender, '15_bis_unter_20_Jahre'] = df.loc[:, (gender, df[gender].columns[3:8])].sum(axis=1)
            df[gender, '20_bis_unter_25_Jahre'] = df.loc[:, (gender, df[gender].columns[8:13])].sum(axis=1)
            # Sum up all years
            df[gender, 'gesamt'] = df.loc[:,(gender, df[gender].columns[:])].sum(axis=1)

    # Drop all single year columns
    df = df.drop(df['insgesamt'].columns[3:13], axis=1, level=1)
    # drop all Drittstaten and European treaty regions
    indices = [idx for idx in df.index.levels[1] if '(' not in idx]
    indices.remove('insgesamt')
    df = df[df.index.get_level_values(1).isin(indices)]

    return df

class Naturalization:

    def __init__(self):
        """_summary_
        """
        self.df = _load_data()

    def get_regions(self) -> list:
        """_summary_

        :return: _description_
        """
        return list([idx for idx in self.df.index.levels[1] if '(' not in idx])

    def get_gender(self) -> list:
        return [i for i in self.df.columns.levels[0] if 'unnamed' not in i]

    def get_age_classes(self) -> list:
        return [i for i in self.df.columns.levels[1] if 'unnamed' not in i and '-' not in i]




    def get_amount_per_region(self, regions: list, gender = 'insgesamt') -> dict:
        """_summary_

        :param df: _description_
        :param region: _description_
        :param age: _description_
        :return: _description_
        """
        data = pd.DataFrame(index=self.df.index.levels[0])

        for region in regions:
            temp_df = self.df[gender].xs(region, level=1)
            temp_df = temp_df.groupby(level='jahr').sum()
            data[region] = temp_df['gesamt']

        return data

    def get_amount_per_age_class(self, region: str, genders: list, ages: list) -> (pd.DataFrame, list):
        data = pd.DataFrame(index=self.df.index.levels[0])

        for gender in genders:
            temp_df = self.df[gender].xs(region, level=1)
            temp_df = temp_df[ages]
            temp_df.columns = [(gender+'_'+i) for i in temp_df.columns]
            data = pd.merge(data, temp_df, left_index=True, right_index=True)

        data = data.groupby(level='jahr').sum()

        return data, data.columns


