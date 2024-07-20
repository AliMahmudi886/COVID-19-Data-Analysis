import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def preprocess_data(df):
    # Convert date columns to datetime
    df['date'] = pd.to_datetime(df['date'])
    # Fill missing values
    df = df.fillna(0)
    return df

if __name__ == "__main__":
    file_path = '../data/covid_19_data.csv'
    df = load_data(file_path)
    df = preprocess_data(df)
    df.to_csv('../data/preprocessed_covid_19_data.csv', index=False)
    print("Data preprocessing completed.")
