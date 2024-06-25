import pandas as pd

def read_csv_file(path, num_rows=0):
    """
    Reads a CSV file and returns it as a DataFrame.

    Args:
        path (str): The file path of the CSV file.
        num_rows (int, optional): The number of rows to read from the CSV file. 
            If not specified or set to 0, all rows will be read. Default is 0.

    Returns:
        pandas.DataFrame: The DataFrame containing the CSV data.
    """
    df = pd.read_csv(path)
    if num_rows != 0:
        df = df.head(num_rows)
    return df


def save_csv_file(df, path):
    """
    Saves a DataFrame to a CSV file.

    Args:
        df (pandas.DataFrame): The DataFrame to be saved.
        path (str): The file path to save the CSV file.
    """
    df.to_csv(path, index=False)


def cut_csv_file(path, num_rows):
    """
    Cuts a CSV file to a specified number of rows and saves it as a new file.

    Args:
        path (str): The file path of the CSV file to be cut.
        num_rows (int): The number of rows to keep in the new CSV file.
    """
    new_path = path.replace('.csv', f'_{num_rows}.csv')
    read_csv_file(path, num_rows).to_csv(new_path, index=False)
