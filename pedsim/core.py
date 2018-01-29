import constants as const
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



""""
1. Have to get row first
2. Calculate score from the row
"""

def get_hospital_data(excel_file, hospital_name):
    #It will consider max of the entries in the column if there are entries in both rows
    # #This ensures that nan is not selected but if both rows have entries it can create
    ##issues... to be kept in mind
    report_out = pd.read_excel(excel_file)
    new_report_out = report_out[report_out[const.site_hosp] == hospital_name].\
        groupby([const.site_hosp]).max().fillna('').reset_index()
    return new_report_out.replace('', np.nan)

def get_case_performance_data(hosp_df, case_headers):
    '''
    assuming cases have more than two headers
    :param df: df obtained from get_hospital_data, it has only one row
    :param case_headers: h
    :return:
    '''
    df1 = hosp_df.filter(like=case_headers[0]).T.reset_index()
    df2 = hosp_df.filter(like=case_headers[1]).T.reset_index()
    df = pd.concat([df1, df2])
    for i in range(2, len(case_headers)):
        curr_df = hosp_df.filter(like=case_headers[i]).T.reset_index()
        df = pd.concat([df, curr_df])
    case_df = df.reset_index()
    col_name = hosp_df.index[0]
    return case_df, col_name

def get_case_performance_score(case_df, col_name):
    '''
    count number of Yes and normalise, output in %
    :param hosp_df:
    :param case_headers:
    :return:
    '''
    score = case_df[col_name].value_counts(True).loc["Yes"]
    percent_score = 100*(np.around(score, decimals=4))
    return percent_score

def get_case_performance_checklist(case_df, col_name, filename):
    case_df[const.index_name] = case_df[const.index_name].apply(lambda x: x.split('.')[0])
    case_df = case_df.pivot_table(index=const.index_name, columns=const.replicates,
                             values=[col_name], aggfunc='first')
    case_df.rename(columns=const.team_dict).to_csv(filename)

def get_case_performance_graph(hosp_name, case_name, case_score, fig_name):
    fig, ax = plt.subplots(figsize=(10, 5))
    pos = [0,1,2]
    y_vals = [const.ged_score[case_name], const.ped_score[case_name], case_score]
    x_vals = [const.ged_name, const.ped_name, hosp_name]
    plt.bar(pos, y_vals, align='center', alpha=0.5)
    plt.xticks(pos, x_vals)
    plt.ylabel('%')
    plt.title('Case Performance')
    for a, b in zip(pos, y_vals):
        ax.text(a, b+0.25, str(b), color='blue', fontweight='bold')
    plt.savefig(fig_name)
