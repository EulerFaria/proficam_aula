from data_acquisition import get_data


if __name__ == "__main__":

    df = get_data()
    print(df.head())
    