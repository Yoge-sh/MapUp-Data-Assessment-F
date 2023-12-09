import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    pivot_table = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set diagonal values to 0
    for i in pivot_table.index:
        pivot_table.loc[i, i] = 0
    # round all values to 1 decimal point
    pivot_table = pivot_table.round(1)
    df = pd.DataFrame(pivot_table)
    df = df*2

    return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    def car_type(x):
        if x<=15:
            return 'low'
        elif x>25:
            return 'high'
        else:
            return 'medium'
    df['car_type'] = df['car'].apply(car_type)
    
    return dict(df['car_type'].value_counts())


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    return sorted(list(df.index[df['bus']>2*df['bus'].mean()]))


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    route_avg = df.groupby('route')['truck'].mean()
    # Filter routes where the average of 'truck' is greater than 7
    routes = route_avg[route_avg > 7].index
    return list(sorted(routes))


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25).round(1)
    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    # Create a boolean column to modify further
    df['Correct_timestamps'] = df['id'].map(lambda x: (x/3).is_integer())
    grouped_df = df.groupby(['id','id_2']).filter(lambda x: True)
    day_mapping = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}

    i = 0
    while i != len(grouped_df):
        if (grouped_df['startTime'].iloc[i] == '00:00:00') & (grouped_df['endTime'].iloc[i] == '23:59:59') & (day_mapping[grouped_df['startDay'].iloc[i]]- day_mapping[grouped_df['endDay'].iloc[i]] <=0):
            grouped_df['Correct_timestamps'].iloc[i]=True
        else:
            grouped_df['Correct_timestamps'].iloc[i]=False
        i+=1    
    id_series = grouped_df.iloc[:,0]
    id_2_series = grouped_df.iloc[:,2]
    is_correct = grouped_df.iloc[:,-1]
    # new boolean Series with multi-index
    combined_series = pd.Series(index=pd.MultiIndex.from_arrays([id_series, id_2_series,is_correct ], names=['id', 'id_2','is_correct_timestamp']))
    combined_series

    return combined_series

if __name__=='__main__':
    # print('Yoyouiou')
    df = pd.read_csv('datasets\dataset-1.csv')

    #q1
    # print(generate_car_matrix(df))

    #q2
    # print(get_type_count(df))

    #q3
    # print(get_bus_indexes(df))

    #q4
    # print(filter_routes(df))

    # #q5
    # matrix = generate_car_matrix(df)
    # print(multiply_matrix(matrix))

    #q6
    # df2 = pd.read_csv('datasets\dataset-2.csv')
    # print(time_check(df2))