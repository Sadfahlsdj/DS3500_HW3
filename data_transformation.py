"""
initial database: https://www.kaggle.com/datasets/datasnaek/chess/data
initial database is read in as games.csv

remove unneeded columns from initial dataset - id, moves, white_id, black_id,
    opening_eco, created_at, last_move_at, opening_name, increment_code
add extra necessary columns - avg_rating, rating_difference, time_control

opening_name removed because there were far too many for it to be a good categorical variable
increment_code removed in favor of the numerical time_control

# explanation of remaining rows for the less chess-savvy:
    the term "half move" refers to a single move made by a player
        a full move is each player moving once

    rated - was the game rated or not - boolean
    turns - number of half turns that the game took - int
    victory_status - how the game ended(mate, resignation, out of time, draw etc) - str
    time_control - time per player in minutes - int
        calculated from increment_code; increment_code is given in starting_time+increment
        starting_time is the number of starting minutes per player
        increment is the number of seconds given to each player after each move
        total time is calculated at 60 moves--starting_time + increment minutes
    white_rating, black_rating - ratings of players - int
    opening_ply - number of half moves that were judged to still be in the opening - int
    avg_rating - average of the 2 players' ratings - float
    rating_diff - white rating minus black rating, if black is higher it will be negative - int
"""
import pandas as pd

df = pd.read_csv('games.csv')

avg_rating = [(d['white_rating'] + d['black_rating']) / 2 for r, d in df.iterrows()]
rating_diff = [d['white_rating'] - d['black_rating'] for r, d in df.iterrows()]
time_control = [int(d['increment_code'].split('+')[0]) + int(d['increment_code'].split('+')[1])
                for r, d in df.iterrows()]

df['avg_rating'] = avg_rating # (white + black) / 2
df['rating_diff'] = rating_diff # white minus black
df['time_control'] = time_control


"""for index, row in df.head().iterrows():
    print(f'white rating: {row["white_rating"]}, black rating: {row["black_rating"]}, '
          f'average rating: {row["avg_rating"]}')"""

df = df.drop(['id', 'moves', 'white_id', 'black_id', 'opening_eco', 'created_at',
              'last_move_at', 'opening_name', 'increment_code'], axis=1)
print(df.head().to_string())

df.to_csv('games_clean.csv')