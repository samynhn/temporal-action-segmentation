import pandas as pd

def extract_columns_from_csv(filename, columns_to_keep, output_filename):

    df = pd.read_csv(filename)

    new_df = df[columns_to_keep]

    new_df.to_csv(output_filename, index=False)



filename = 'data.csv'
selected_columns = ['rally', 'ball_round', 'roundscore_A', 'lose_reason', 'win_reason']
output_file = 'filteredData.csv'
extract_columns_from_csv(filename, selected_columns, output_file)


