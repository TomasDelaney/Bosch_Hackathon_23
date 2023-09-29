import pandas as pd


def load_csv():
    # Replace 'your_file.csv' with the path to your CSV file
    file_path = 'functional_layer/developmentData.csv'

    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(file_path)

    # Convert DataFrame to a dictionary of NumPy arrays
    data_dict = {column: df[column].to_numpy() for column in df.columns}

    # transform the distance data
    distance_constant = 128
    data_dict["FirstObjectDistance_X"] = data_dict["FirstObjectDistance_X"] / distance_constant
    data_dict["FirstObjectDistance_Y"] = data_dict["FirstObjectDistance_Y"] / distance_constant
    data_dict["SecondObjectDistance_X"] = data_dict["SecondObjectDistance_X"] / distance_constant
    data_dict["SecondObjectDistance_Y"] = data_dict["SecondObjectDistance_Y"] / distance_constant
    data_dict["ThirdObjectDistance_X"] = data_dict["ThirdObjectDistance_X"] / distance_constant
    data_dict["ThirdObjectDistance_Y"] = data_dict["ThirdObjectDistance_Y"] / distance_constant
    data_dict["FourthObjectDistance_X"] = data_dict["FourthObjectDistance_X"] / distance_constant
    data_dict["FourthObjectDistance_Y"] = data_dict["FourthObjectDistance_Y"] / distance_constant

    # transform the velocity data
    velocity_constant = 256
    data_dict["VehicleSpeed"] = data_dict["VehicleSpeed"] / velocity_constant
    data_dict["FirstObjectSpeed_X"] = data_dict["FirstObjectSpeed_X"] / velocity_constant
    data_dict["FirstObjectSpeed_Y"] = data_dict["FirstObjectSpeed_Y"] / velocity_constant
    data_dict["SecondObjectSpeed_X"] = data_dict["SecondObjectSpeed_X"] / velocity_constant
    data_dict["SecondObjectSpeed_Y"] = data_dict["SecondObjectSpeed_Y"] / velocity_constant
    data_dict["ThirdObjectSpeed_X"] = data_dict["ThirdObjectSpeed_X"] / velocity_constant
    data_dict["ThirdObjectSpeed_Y"] = data_dict["ThirdObjectSpeed_Y"] / velocity_constant
    data_dict["FourthObjectSpeed_X"] = data_dict["FourthObjectSpeed_X"] / velocity_constant
    data_dict["FirstObjectSpeed_Y"] = data_dict["FirstObjectSpeed_Y"] / velocity_constant

    # Now, data_dict is a dictionary where keys are column names and values are NumPy arrays
    return data_dict


if __name__ == "__main__":
    dataset = load_csv()
    print(dataset)
