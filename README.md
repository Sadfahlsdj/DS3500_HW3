Instructions:

Initial dataset can be found at https://www.kaggle.com/datasets/datasnaek/chess/data - unzip and download into project folder.

If a professor or TA is reading this, I have submitted games.csv and games_clean.csv along with my project files--this just details my methodology.

Name this csv games.csv, or change the filename in the pd.read_csv inside of data_transformation.py.

Run data transformation.py.

A new file named games_clean.csv should appear.

Run chess_explorer.py to generate the webapp.

On the webapp, the "search" sidebar tab contains menus for x_column, y_column, and rated.

The x_column and y_column parameters determine which columns of the dataframe are shown in the graph on the "Graph" tab, as well as which columns appear in the table in the "Two Variable Table" tab (the entire dataframe can be found in the "Full Table" tab). The type of graph shown varies depending on if the x_column and y_column parameters correspond to numeric or categorical columns.

The rated parameter determines whether unrated only, rated only, or all games are included in the graph and table. If all games are included, scatter plots will be color coded between rated and unrated games.

The "plot" sidebar tab contains width and height sliders for the size of the graph.

A brief explanation of each column name for the less chess savvy, as well as its datatype, can be found below:

    The term "half move" refers to a single move made by a player; a full move is each player moving once
    
    rated - was the game rated or not - boolean

    winner - who won the game (white, black, draw) - str
    
    turns - number of half turns that the game took - int
    
    victory_status - how the game ended(mate, resignation, out of time, draw) - str
    
    time_control - time per player in minutes - int
    
    white_rating, black_rating - ratings of players - int
    
    opening_ply - number of half moves that were judged to still be in the opening - int
    
    avg_rating - average of the 2 players' ratings - float
    
    rating_diff - white rating minus black rating, if black is higher it will be negative - int

The same explanation, with a bit more detail in some areas, can be found in data_transformation.py. Enjoy!


