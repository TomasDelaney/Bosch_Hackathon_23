import pandas as pd


def load_csv():
    # Replace 'your_file.csv' with the path to your CSV file
    file_path = 'functional_layer/developmentData.csv'

    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(file_path)

    # Convert DataFrame to a dictionary of NumPy arrays
    data_dict = {column: df[column].to_numpy() for column in df.columns}

    # Now, data_dict is a dictionary where keys are column names and values are NumPy arrays
    return data_dict


if __name__ == "__main__":
    dataset = load_csv()
    print(dataset)
