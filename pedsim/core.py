from __future__ import division
from math import pi
import re

import datetime as dt
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
    try:
        latest_timestamp = max(report_out[[not x for x in report_out[const.timestamp].\
            isna()]][const.timestamp])
    except KeyError:
        print("..........Timestamp not found. Initialising the Excelsheet.........")
        report_out = initialise_df(report_out)
        latest_timestamp = max(report_out[const.timestamp])
    finally:
        if latest_timestamp==latest_timestamp:
            latest = report_out[report_out[const.timestamp]==latest_timestamp].reset_index()
            for each in const.ged_score.keys():
                const.ged_score[each] = latest[each][0]
            for each in const.ped_score.keys():
                const.ped_score[each] = latest[each][0]
            const.total_ged_count = latest['ged_count'][0]
            const.total_ped_count = latest['ped_count'][0]
        new_report_out = report_out[report_out[const.site_hosp] == hospital_name].\
        groupby([const.site_hosp]).max().fillna('').reset_index()
        return (report_out, new_report_out.replace('', np.nan))

def initialise_df(df):
    empty_data_column = [np.nan for i in range(len(df))]
    extra_columns = ["ped_count", 'ged_count', "timestamp", "ged_fbd",\
     "ged_sepsis", "ged_seizure", "ged_cardiac_arrest", "ged_teamwork",\
     "ged_emsc", "ged_qipi", "ged_emsc_staff", "ged_emsc_safety", "ged_emsc_equip",\
     "ged_emsc_policy", "ped_fbd", "ped_sepsis", "ped_seizure", "ped_cardiac_arrest",\
     "ped_teamwork", "ped_emsc", "ped_qipi", "ped_emsc_staff", "ped_emsc_safety",\
     "ped_emsc_equip", "ped_emsc_policy"]
    for each_col in extra_columns:
        df[each_col] = empty_data_column
    return df

def validate_team_participation(hosp_df, case_header):
    validate_series = hosp_df.filter(like=case_header[0]).T.reset_index()[0].isna()
    for question in case_header:
        case_df = hosp_df.filter(like=question).T.reset_index()
        case_df['index'] = case_df['index'].apply(lambda x: re.split('[.][0-9]$', x)[0])
        case_df = case_df[case_df['index'].isin(case_header)].reset_index()
        if len(case_df)!=len(const.team_dict.keys()):
            raise ValueError(const.column_name_error_message+question)
        this_series = case_df[0].isna()
        if (validate_series != this_series).any():
            raise ValueError(const.case_error_message+question)

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

def get_updated_checklist_format(checklist_df, case_name):
    case_replacement = const.case_map[case_name]
    replacements = []
    for each in checklist_df[const.index_name]:
        replacements.append(case_replacement[each])
    checklist_df[const.index_name] = replacements
    return checklist_df

def get_case_performance_graph_donut(hosp_name, case_name, case_score):
    hosp_graph = [[100 - case_score, case_score], ['white', const.hosp_color], 1]
    ped_graph = [[100 - const.ped_score["ped_"+case_name], const.ped_score["ped_"+case_name]],
                    ['white', const.ped_color], 1.15]
    ged_graph = [[100 - const.ged_score["ged_"+case_name], const.ged_score["ged_"+case_name]],
                    ['white', const.ged_color], 1.3]
    center_graph = [[100], ['white'], 0.85]

    fig = plt.figure(figsize = (10,10))
    for each in [ged_graph, ped_graph, hosp_graph, center_graph]:
        plt.pie(each[0], colors=each[1], 
            startangle=90, shadow=False, radius=each[2])
    plt.text(0, 0.1, str(case_score)+"%", horizontalalignment='center',
         verticalalignment='center', fontsize=80, weight='bold', color='#00BFFF')
    plt.text(0,-0.14, "PED-"+str(const.ped_score["ped_"+case_name])+"%", 
         horizontalalignment='center', verticalalignment='center', fontsize=40,
         weight='bold', color='#E3E3E3')
    plt.text(0,-0.34, "GED-"+str(const.ged_score["ged_"+case_name])+"%",
         horizontalalignment='center', verticalalignment='center', fontsize=40,
         weight='bold', color='#03A89E')
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
    validate_team_participation(hosp_df, case_header)
    data = get_case_performance_data(hosp_df, case_header)
    df = get_case_performance_checklist(data)
    score = round(get_case_performance_score(data), 2)
    if np.isnan(score):
        return df, np.nan, score
    fig = get_case_performance_graph_donut(hosp_name, case_name, score)
    if isinstance(df, pd.DataFrame):
        df = get_updated_checklist_format(df, case_name)
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
    is_entry_na = hosp_df[emsc_header].isna().any()
    for i in range(len(emsc_header)):
        if is_entry_na[i]==True:
            raise ValueError("Following column cannot be empty:\n\t"+emsc_header[i])
    hosp_val_df = utils.convert_truth_values_to_num(hosp_df)
    total_score = sum(weights)
    num = 0
    for header, val in zip(emsc_header, weights):
        num = num + hosp_val_df.get_value(const.hosprow_col, header)*val
    percent_score = 100*np.around(num/total_score, decimals=2)
    return percent_score

def get_total_emsc_score(qipi, admin, staff, safety, policy, equip):
    '''Total EMSC Readiness score is average of all the EMSC case scores
    calculated separately. As the scores are in percentages, final result
    is a percentage as well
    '''
    total_emsc_weights = []
    numerator = 0
    weights = [const.qi_pi_score, const.score_admin, const.score_staff,
                 const.safety_score, const.policy_score, const.equip_score]
    percentages=[qipi, admin, staff, safety, policy, equip]
    for i in range(len(percentages)):
        numerator+=percentages[i]*sum(weights[i])
        total_emsc_weights.extend(weights[i])

    return np.around(numerator/sum(total_emsc_weights), decimals=2)

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
    plt.bar(pos, first_val_arr, width, alpha=0.5, color=const.hosp_color,
            label=first_name, capsize=2)
    plt.bar([p + width for p in pos], second_val_arr, width, alpha=0.5,
            color=const.ped_color, label=second_name, capsize=2)
    plt.bar([p + 2 * width for p in pos], third_val_arr, width, alpha=0.5,
            color=const.ged_color, label=third_name, capsize=2)
    ax.set_title(title)
    ax.set_xticks([p + width for p in pos])
    ax.set_xticklabels(xlabels, rotation="vertical")
    ax.set_ylabel(ylabel)
    plt.legend([first_name, second_name, third_name],
               loc="lower center", bbox_to_anchor=(1.1, 0.8))
    plt.tight_layout()
    return fig

def plot_triple_radargraph(first_name, first_val_arr, second_name,
                         second_val_arr, third_name, third_val_arr,
                         title, xlabels):
    N = len(xlabels)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    fig = plt.figure(figsize=(30,15))
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.set_title(title, size=45)
    ax.set_rlabel_position(0)
    plt.yticks([10 * i for i in range(1,10)],
        [10 * i for i in range(1,10)],
        color="black", size=20)
    plt.ylim(0,100)
    names = [second_name, third_name, first_name]
    val_arr = [second_val_arr, third_val_arr, first_val_arr]
    colors = [const.ped_color, const.ged_color, const.hosp_color]
    for i in range(len(names)):
        val_arr[i] += val_arr[i][:1]
        ax.plot(angles, val_arr[i], linewidth=1, linestyle='solid',
         label=names[i], color=colors[i])
        ax.fill(angles, val_arr[i], colors[i], alpha=0.7)
    plt.xticks(angles[:-1],[])
    for i in range(N):
        angle_rad = i / float(N) * 2 * pi
        if angle_rad == 0:
            ha, distance_ax = "center", 2
        elif 0 < angle_rad < pi:
            ha, distance_ax = "left", 2
        elif angle_rad == pi:
            ha, distance_ax = "center", 3
        else:
            ha, distance_ax = "right", 2
        ax.text(angle_rad, 100 + distance_ax,
            xlabels[i]+": "+str(int(first_val_arr[i]))+"%", size=25, color = "#1874CD",
            horizontalalignment=ha, verticalalignment="center")

    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), prop={'size':20})
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
    ged_scores = [const.ged_score["ged_emsc_qipi"], const.ged_score["ged_emsc_policy"],
                  const.ged_score["ged_emsc_safety"], const.ged_score["ged_emsc_staff"],
                  const.ged_score["ged_emsc_equip"]]
    ped_scores = [const.ped_score["ped_emsc_qipi"], const.ped_score["ped_emsc_policy"],
                  const.ped_score["ped_emsc_safety"], const.ped_score["ped_emsc_staff"],
                  const.ped_score["ped_emsc_equip"]]
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
    ged_scores = [const.ged_score["ged_emsc"], const.ged_score["ged_fbd"], const.ged_score["ged_sepsis"],
                  const.ged_score["ged_seizure"], const.ged_score["ged_cardiac_arrest"],
                  const.ged_score["ged_teamwork"]]
    ped_scores = [const.ped_score["ped_emsc"], const.ped_score["ped_fbd"], const.ped_score["ped_sepsis"],
                  const.ped_score["ped_seizure"], const.ped_score["ped_cardiac_arrest"],
                  const.ped_score["ped_teamwork"]]
    hosp_scores = [emsc, fbd, sepsis, seizure, cardiac_arrest, teamwork]
    xlabels = ["EMSC Readiness", "Foreign Body", "Sepsis",
                    "Seizure", "Cardiac Arrest", "Teamwork"]
    for i in range(6):
        if not np.isnan(hosp_scores[i]):
            hosp_scores.append(hosp_scores[i])
            ged_scores.append(ged_scores[i])
            ped_scores.append(ped_scores[i])
            xlabels.append(xlabels[i])
    hosp_scores = hosp_scores[6:]
    ged_scores = ged_scores[6:]
    ped_scores = ped_scores[6:]
    xlabels = xlabels[6:]
    return plot_triple_radargraph(hosp_name, hosp_scores, const.ped_name, ped_scores, const.ged_name,
                                ged_scores, "Performance Summary", xlabels)

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
        curr_df = curr_df.astype(dtype= {const.hosp_ans:"float64"})
        percent_score = 100*np.around(curr_df[const.hosp_ans].\
            sum()/(10*curr_df[const.hosp_ans].count()),decimals=2)
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
                        columns=['Other Elements', 'Score'])
    return df

def update_average_scores(total_df, excel_file, hosp_name, this_scores):
    new_filepath = (".".join(excel_file.split(".")[:-1])).split("___")[0] +\
        "___"+"-".join(re.split("\s|\:|\.", str(dt.datetime.now())))+".xlsx"
    for each_key in this_scores.keys():
        updated_ped_score = (const.ped_score['ped_'+each_key]*const.total_ped_count+
            this_scores[each_key])/(const.total_ped_count+1)
        updated_ged_score = (const.ged_score['ged_'+each_key]*const.total_ged_count+
            this_scores[each_key])/(const.total_ged_count+1)
        total_df.loc[total_df[const.site_hosp]==hosp_name, 'ped_'+each_key] = updated_ped_score
        total_df.loc[total_df[const.site_hosp]==hosp_name, 'ged_'+each_key] = updated_ged_score
    total_df.loc[total_df[const.site_hosp]==hosp_name, 'ped_count']\
        = const.total_ped_count+1
    total_df.loc[total_df[const.site_hosp]==hosp_name, 'ged_count']\
        = const.total_ged_count+1
    total_df.loc[total_df[const.site_hosp]==hosp_name, const.timestamp] = dt.datetime.now()
    writer = pd.ExcelWriter(new_filepath, engine='openpyxl')
    total_df.to_excel(writer)
    writer.save()
