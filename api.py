"""
Primary api for interacting with the gad dataset
"""

import pandas as pd

class API():
    df = None # dataframe

    def load_df(self, filename):
        """
        load the input file into instance variable dataframe
        """
        self.df = pd.read_csv(filename)

    def get_columns(self):
        """
        returns a list of columns in the dataframe, excluding the first (index) column
        """
        cols = [l for l in list(self.df.columns)[1:]]
        # first column is index, removing it
        return cols

    def column_datatypes(self):
        """
        :return: dict-like with key as column name and value as datatype
        relevant because graph behavior differs based on whether columns are numeric
        """
        return self.df.dtypes


    def extract_two_var_df(self, x_column, y_column, rated):
        """
        Args:
            x_column: string - column name of column to use as x variable
                gotten through selector widget on the webapp
            y_column: string - column name of column to use as y variable
                gotten through selector widget on the webapp
            rated: one of ['rated', 'unrated', 'all']
                determines whether rated/unrated/all games are considered for the graph
                gotten through selector widget on the webapp
        """
        df = self.df

        # discard games that are unrated/rated depending on input
        if rated == 'rated':
            df = df[df['rated'] == True]
        elif rated == 'unrated':
            df = df[df['rated'] == False]

        # return the x column, y column, and rated column if it is not the x or y column

        # if one of the chosen columns is rated, do not add it to returned df as it causes an error
        # if not, add that column so graphs can color code based on rated
        if x_column == 'rated' or y_column == 'rated':
            df = df[[x_column, y_column]]
        else:
            df = df[[x_column, y_column, 'rated']]
        return df

    def extract_full_df(self):
        df = self.df[1:]
        return df



def main():
    api = API()
    api.load_df('games_clean.csv')

    a = api.get_columns()
    b = api.extract_two_var_df('increment_code', 'white_rating', rated='unrated')
    c = api.column_datatypes()

    # print(b.head().to_string())
    print(str(c['white_rating']))



if __name__ == '__main__':
    main()