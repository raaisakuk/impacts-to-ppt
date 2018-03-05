from __future__ import division
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import constants as const
import utils

def get_hospital_data(excel_file, hospital_name):
    '''
    Reads excel file which has all the data and in case any hospital has data in more than
    one rows, combines them on the basis of max. The idea is that if this is the case, all
    rows will be empty except one.
    Todo: If both rows have entries it can create problems. User should be warned in such
    cases.
    :param excel_file: survey output from Qualtrix
    :param hospital_name: hospital for which report out has to be made
    :return: dataframe with the data corresponding to only the given hospital
    '''
    report_out = pd.read_excel(excel_file)
    new_report_out = report_out[report_out[const.site_hosp] == hospital_name].\
        groupby([const.site_hosp]).max().fillna('').reset_index()
    return new_report_out.replace('', np.nan)

def get_case_performance_data(hosp_df, case_headers):
    '''Getting data for all the teams for a particular set of questions. Here we are
    assuming that the number of questions for each case are two or more. The questions
    and answers are transposed to get a dataframe with given questions and answers as data
    in rows.
    Todo: Raise custom exception instead of returning -1
    :param hosp_df: df obtained from get_hospital_data, it has only the row which corresponds
    to the answers obtained from a particular hospital
    :param case_headers: Questions for a particular case form the column names and this list
    contains those column names
    :return: dataframe with team number, questions and answers, if answers Nan return -1
    '''
    df1 = hosp_df.filter(like=case_headers[0]).T.reset_index()
    df2 = hosp_df.filter(like=case_headers[1]).T.reset_index()
    df = pd.concat([df1, df2])
    for i in range(2, len(case_headers)):
        curr_df = hosp_df.filter(like=case_headers[i]).T.reset_index()
        df = pd.concat([df, curr_df])
    case_df = df.reset_index()
    case_df['index'] = case_df['index'].apply(lambda x: re.split('[.][0-9]$', x)[0])
    case_df = case_df[case_df['index'].isin(case_headers)]
    case_df.rename(mapper={'index': const.index_name, 'level_0': const.replicates,
                           const.hosprow_col: const.hosp_ans}, axis='columns', inplace=True)
    if case_df[const.hosp_ans].isnull().all():
        return np.nan
    else:
        return case_df

def get_case_performance_score(case_df):
    '''Case performance score is % of questions answered Yes by each team, averaged
    over all the teams.
    :param case_df: df from get_case_performance_data which contains questions and ans
    for all teams for a particular case
    :return: percentage score
    '''
    if isinstance(case_df, pd.DataFrame):
        all_scores = case_df[const.hosp_ans].value_counts(True)
        try:
            return 100 * (np.around(all_scores.loc['Yes'], decimals=2))
        except KeyError:
            return 100 - 100 * (np.around(all_scores.loc['No'], decimals=2))
    else:
        return np.nan

def get_case_performance_checklist(case_df):
    '''This checklist contains Question and corresponding answers for each team. It
    has to go in the report.
    :param case_df: df from get_case_performance_data which contains questions and ans
    for all teams for a particular case
    :return: dataframe of checklist formatted properly
    '''
    if isinstance(case_df, pd.DataFrame):
        case_df = case_df.groupby([const.index_name]).\
            apply(lambda x: pd.Series(x[const.hosp_ans].dropna().values))\
            .rename(columns=const.team_dict)
        return case_df.reset_index(level=[const.index_name])
    else:
        return np.nan

def get_case_performance_graph(hosp_name, case_name, case_score):
    '''Plot bar graph for case performance score with GED and PED scores
    :param hosp_name: Name of the hospital
    :param case_name: Name of the case to get ged and ped score from constants
    :param case_score: Score for the case
    :return: Figure handle for the bar plot
    '''
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(figsize=(10, 5))
    pos = [0, 1, 2]
    width = 0.25
    y_vals = [const.ged_score[case_name], const.ped_score[case_name], case_score]
    x_vals = [const.ged_name, const.ped_name, hosp_name]
    plt.bar(pos, y_vals, width, align='center', alpha=0.5, color=sns.color_palette("muted"))
    plt.xticks(pos, x_vals)
    ax.set_xticklabels(x_vals, rotation="vertical")
    plt.ylabel('%')
    plt.title('Case Performance| '+const.case_name_dict[case_name])
    plt.ylim([0, 100])
    for a, b in zip(pos, y_vals):
        ax.text(a, b+0.25, str(b), color='blue', fontweight='bold')
    plt.tight_layout()
    return fig

def create_case_df_fig(hosp_name, hosp_df, case_header, case_name):
    '''Get case performance checklist and figure from hospital info
    :param hosp_name: Name of the hospital
    :param hosp_df: df obtained from get_hospital_data, it has only
    the row which corresponds to the answers obtained from a
    particular hospital
    :param case_header: Questions for a particular case form the column
    names and this list contains those column names
    :param case_name: Name of the case to get ged and ped score from
    constants
    :return: case checklist, case performance fig, case score
    '''
    data = get_case_performance_data(hosp_df, case_header)
    df = get_case_performance_checklist(data)
    score = get_case_performance_score(data)
    fig = get_case_performance_graph(hosp_name, case_name, score)
    return df, fig, score

def get_emsc_score(hosp_df, emsc_header, weights):
    '''Calculate EMSC score for different EMSC cases. Each question is
    weighted which acts as the score for that questions. A hospital has
    only one EMSC score and not averaged over teams.
    :param hosp_df: df obtained from get_hospital_data, it has only the row
    which corresponds to the answers obtained from a particular hospital
    :param emsc_header: headers of the EMSC case for which score has to be
    calculated
    :param weights: weights corresponding to the above headers in the same
    order
    :return: percentage score which will be nan if all vals nan
    '''
    hosp_val_df = utils.convert_truth_values_to_num(hosp_df)
    total_score = sum(weights)
    num = 0
    for header, val in zip(emsc_header, weights):
        num = num + hosp_val_df.get_value(const.hosprow_col, header)*val
    percent_score = 100*np.around(num/total_score, decimals=2)
    return percent_score

def get_total_emsc_score(qipi, staff, safety, equip, policy, admin):
    '''Total EMSC Readiness score is average of all the EMSC case scores
    calculated separately. As the scores are in percentages, final result
    is a percentage as well
    '''
    return np.around((qipi+staff+safety+equip+policy+admin)/6, decimals=2)

def plot_triple_bargraph(first_name, first_val_arr, second_name,
                         second_val_arr, third_name, third_val_arr, ylabel,
                         title, xlabels):
    '''Plotting grouped bargraph, with three values from different cases
    grouped together and then plotted for multiple conditions on x axis
    :param first_name: name corresponding to the first set of values
    :param first_val_arr: list of values which will form leftmost bars
    :param second_name: name corresponding to the second set of values
    :param second_val_arr: list of values which will form middle bars
    :param third_name: name corresponding to the third set of values
    :param third_val_arr: list of values which will form rightmost bars
    :param ylabel: Y axis label
    :param title: Title of the plot
    :param xlabels: list of x labels whose length is equal to length of
    values to be plotted for each set
    :return: Figure handle
    '''
    sns.set_style('whitegrid')
    pos = list(range(len(first_val_arr)))
    width = 0.25
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.bar(pos, first_val_arr, width, alpha=0.5, color='r',
            label=first_name, capsize=2)
    plt.bar([p + width for p in pos], second_val_arr, width, alpha=0.5,
            color='g', label=second_name, capsize=2)
    plt.bar([p + 2 * width for p in pos], third_val_arr, width, alpha=0.5,
            color='b', label=third_name, capsize=2)
    ax.set_title(title)
    ax.set_xticks([p + width for p in pos])
    ax.set_xticklabels(xlabels, rotation="vertical")
    ax.set_ylabel(ylabel)
    plt.legend([first_name, second_name, third_name],
               loc="lower center", bbox_to_anchor=(1.1, 0.8))
    plt.tight_layout()
    return fig

def plot_emsc_graph(hosp_name, qipi, staff, safety, equip, policy):
    '''Plot EMSC graph with hospital, GED and PED scores for all EMSC
    cases
    :param hosp_name: name of the hospital
    :param qipi: Quality Improvement score
    :param staff: Physician/Nurse Staffing score
    :param safety: Patient Safety score
    :param equip: Equipment and Supplies score
    :param policy: Policies/Procedures score
    :return: Figure handle
    '''
    ged_scores = [const.ged_score["emsc_qipi"], const.ged_score["emsc_policy"],
                  const.ged_score["emsc_safety"], const.ged_score["emsc_staff"],
                  const.ged_score["emsc_equip"]]
    ped_scores = [const.ped_score["emsc_qipi"], const.ped_score["emsc_policy"],
                  const.ped_score["emsc_safety"], const.ped_score["emsc_staff"],
                  const.ped_score["emsc_equip"]]
    hosp_scores = [qipi, policy, safety, staff, equip]
    return plot_triple_bargraph(hosp_name, hosp_scores, const.ped_name, ped_scores,
                         const.ged_name, ged_scores, "Score %", "EMSC Pediatric Readiness",
                         ["Quality Improvement", "Policies/Procedures", "Patient Safety",
                          "Physician/Nurse Staffing", "Equipment and Supplies"])

def plot_performance_summary(hosp_name, fbd, sepsis, cardiac_arrest, teamwork, emsc,
                             seizure):
    '''Plot case performance summary graph with hospital, GED and PED scores for all
    cases
    :param hosp_name: name of the hospital
    :param fbd: Foreign Body Case Score
    :param sepsis: Sepsis Case Score
    :param cardiac_arrest: Cardiac Arrest Case Score
    :param teamwork: Teamwork Score
    :param emsc: EMSC Readiness Score
    :param seizure: Seizure Case Score
    :return: Figure handle
    '''
    ged_scores = [const.ged_score["emsc"], const.ged_score["fbd"], const.ged_score["sepsis"],
                  const.ged_score["seizure"], const.ged_score["cardiac_arrest"],
                  const.ged_score["teamwork"]]
    ped_scores = [const.ped_score["emsc"], const.ped_score["fbd"], const.ped_score["sepsis"],
                  const.ped_score["seizure"], const.ped_score["cardiac_arrest"],
                  const.ped_score["teamwork"]]
    hosp_scores = [emsc, fbd, sepsis, seizure, cardiac_arrest, teamwork]
    return plot_triple_bargraph(hosp_name, hosp_scores, const.ped_name, ped_scores, const.ged_name,
                                ged_scores, "Score %", "Performance Summary",
                                ["EMSC Readiness Score", "Foreign Body Case Score", "Sepsis Case Score",
                                 "Seizure Case Score", "Cardiac Arrest Case Score", "Teamwork Score"])

def get_cts_score(hosp_df, header):
    '''CTS score for the case when CTS values for different cases are combined
    in one set of questions
    :param hosp_df: df obtained from get_hospital_data, it has only the row which corresponds
    to the answers obtained from a particular hospital
    :param header: col names for CTS questions
    :return: percentage score which is nan in case values are nan
    '''
    curr_df = (hosp_df[header].T)[const.hosprow_col]
    percent_score = 100*np.around(curr_df.sum()/(10*curr_df.count()), decimals=2)
    return percent_score

def get_cts_ind_score(hosp_df, cts_ind_header):
    '''Individual CTS score calculated for given CTS case. It is
    averaged over all teams
    :param hosp_df: df obtained from get_hospital_data, it has only the row which corresponds
    to the answers obtained from a particular hospital
    :param cts_ind_header: col names for the given CTS case
    :return: percent score which is na if case is empty
    '''
    curr_df = get_case_performance_data(hosp_df, cts_ind_header)
    if isinstance(curr_df, pd.DataFrame):
        percent_score = 100*np.around(curr_df[const.hosp_ans].sum()/(10*curr_df[const.hosp_ans].count()),
                                      decimals=2)
    else:
        percent_score = np.nan
    return percent_score

def get_cts_score_from_parts(hosp_df):
    '''Calculate CTS score by averaging CTS score of ind cases i.e
    FBD, Cardiac, Seizure, Sepsis
    :param hosp_df: df obtained from get_hospital_data, it has only the row which corresponds
    to the answers obtained from a particular hospital
    :return: avearged percent which takes into account the fact that
    if a case doesn't exist, don't include it in average
    '''
    cardiac = get_cts_ind_score(hosp_df, const.cts_tool_ind_cardiac)
    fbd = get_cts_ind_score(hosp_df, const.cts_tool_ind_fbd)
    seiz = get_cts_ind_score(hosp_df, const.cts_tool_ind_seiz)
    sep = get_cts_ind_score(hosp_df, const.cts_tool_ind_sep)
    return np.around(np.nanmean([cardiac, fbd, seiz, sep]), decimals=2)

def get_overall_performance_scores(hosp_df):
    '''Get scores for overall performance metrices
    :param hosp_df: df obtained from get_hospital_data, it has only
    the row which corresponds to the answers obtained from a
    particular hospital
    :return: dictionary with name -> score
    '''
    weight_data = get_case_performance_data(hosp_df, const.weight)
    disposition = get_case_performance_data(hosp_df, const.disposition)
    fam_pre = get_case_performance_data(hosp_df, const.family_pres)
    fam_care = get_case_performance_data(hosp_df, const.family_care)

    cts_score = get_cts_score(hosp_df, const.cts_tool_all)
    if np.isnan(cts_score):
       cts_score = get_cts_score_from_parts(hosp_df)

    overall_scores = {const.weight_title: get_case_performance_score(weight_data),
                      const.disposition_title: get_case_performance_score(disposition),
                      const.family_pres_title: get_case_performance_score(fam_pre),
                      const.family_care_title: get_case_performance_score(fam_care),
                      const.cts_title: cts_score}
    return overall_scores

def create_overall_df(overall_scores_dict):
    '''Create df with overall metric names and scores
    :param overall_scores_dict: dict with name -> scores
    :return: dataframe with columns Metric and Score
    '''
    df = pd.DataFrame(list(overall_scores_dict.iteritems()),
                        columns=['Metric', 'Score'])
    return df
