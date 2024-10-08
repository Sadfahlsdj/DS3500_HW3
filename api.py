"""
Primary api for interacting with the gad dataset
"""

import pandas as pd

class API():
    df = None # dataframe

    def load_df(self, filename):
        self.df = pd.read_csv(filename)

    def get_columns(self, exclude=None):
        """
        exclude column is for later if I can make the x_column result not show in y_column list
        """
        cols = [l for l in list(self.df.columns)[1:] if l != exclude]
        # first column is index, removing it
        return cols

    def column_datatypes(self):
        """

        :return: dict-like with key as column name and value as datatype
        """
        return self.df.dtypes


    def extract_local_network(self, x_column, y_column, rated):
        df = self.df

        # discard games that are unrated/rated depending on input
        if rated == 'rated':
            df = df[df['rated'] == True]
        elif rated == 'unrated':
            df = df[df['rated'] == False]

        # Focus on a particular set of columns
        df = df[[x_column, y_column, 'rated']]

        return df



def main():
    api = API()
    api.load_df('games_clean.csv')

    a = api.get_columns()
    b = api.extract_local_network('increment_code', 'white_rating', rated='unrated')
    c = api.column_datatypes()

    # print(b.head().to_string())
    print(str(c['white_rating']))



if __name__ == '__main__':
    main()