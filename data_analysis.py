import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_preprocessed_data(file_path):
    return pd.read_csv(file_path)

def plot_cases_over_time(df):
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='date', y='cases', data=df, marker='o')
    plt.title('COVID-19 Cases Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Cases')
    plt.show()

if __name__ == "__main__":
    file_path = '../data/preprocessed_covid_19_data.csv'
    df = load_preprocessed_data(file_path)
    plot_cases_over_time(df)
