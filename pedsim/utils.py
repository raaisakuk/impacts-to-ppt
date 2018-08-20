import pandas as pd

def convert_truth_values_to_num(df):
    '''Convert Yes to 1 and No to 0 in a dataframe
    '''
    df = df.replace('Yes', 1)
    df = df.replace('No', 0)
    return df