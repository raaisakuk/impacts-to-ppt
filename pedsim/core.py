from __future__ import division

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
    :param df: df obtained from get_hospital_data, it has only the row which corresponds
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
    case_df.rename(mapper={'index': const.index_name, 'level_0': const.replicates,
                           const.hosprow_col: const.hosp_ans}, axis='columns', inplace=True)
    if case_df[const.hosp_ans].isnull().all():
        return -1
    else:
        return case_df

def get_case_performance_score(case_df):
    '''Case performance score is % of questions answered Yes by each team, averaged
    over all the teams.
    :param case_df: df from get_case_performance_data which contains questions and ans
    for all teams for a particular case
    :return: percentage score
    '''
    all_scores = case_df[const.hosp_ans].value_counts(True)
    try:
        return 100 * (np.around(all_scores.loc['Yes'], decimals=4))
    except KeyError:
        return 100 - 100 * (np.around(all_scores.loc['No'], decimals=4))

def get_case_performance_checklist(case_df):
    '''This checklist contains Question and corresponding answers for each team. It
    has to go in the report.
    :param case_df: df from get_case_performance_data which contains questions and ans
    for all teams for a particular case
    :return: dataframe of checklist formatted properly
    '''
    case_df[const.index_name] = case_df[const.index_name].apply(lambda x: x.split('.')[0])
    case_df = case_df.groupby([const.index_name]).\
        apply(lambda x: pd.Series(x[const.hosp_ans].dropna().values))\
        .rename(columns=const.team_dict)
    return case_df.reset_index(level=[const.index_name])

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
    y_vals = [const.ged_score[case_name], const.ped_score[case_name], case_score]
    x_vals = [const.ged_name, const.ped_name, hosp_name]
    plt.bar(pos, y_vals, align='center', alpha=0.5, color=sns.color_palette("muted"))
    plt.xticks(pos, x_vals)
    plt.ylabel('%')
    plt.title('Case Performance| '+const.case_name_dict[case_name])
    plt.ylim([0, 100])
    for a, b in zip(pos, y_vals):
        ax.text(a, b+0.25, str(b), color='blue', fontweight='bold')
    plt.tight_layout()
    return fig

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
    :return: percentage score and -1 if all values nan
    '''
    hosp_val_df = utils.convert_truth_values_to_num(hosp_df)
    total_score = sum(weights)
    num = 0
    for header, val in zip(emsc_header, weights):
        num = num + hosp_val_df.get_value(const.hosprow_col, header)*val
    percent_score = 100*np.around(num/total_score, decimals=4)
    if np.isnan(percent_score):
        return -1
    else:
        return percent_score

def get_total_emsc_score(qipi, staff, safety, equip, policy, admin):
    '''Total EMSC Readiness score is average of all the EMSC case scores
    calculated separately. As the scores are in percentages, final result
    is a percentage as well
    '''
    return np.around((qipi+staff+safety+equip+policy+admin)/6, decimals=4)

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

def plot_performance_summary(hosp_name, fbd, sepsis, cardiac_arrest, teamwork, emsc, seizure, filename):
    ged_scores = [const.ged_score["emsc"], const.ged_score["fbd"], const.ged_score["sepsis"],
                  const.ged_score["seizure"], const.ged_score["cardiac_arrest"], const.ged_score["teamwork"]]
    ped_scores = [const.ped_score["emsc"], const.ped_score["fbd"], const.ped_score["sepsis"],
                  const.ped_score["seizure"], const.ped_score["cardiac_arrest"], const.ped_score["teamwork"]]
    hosp_scores = [emsc, fbd, sepsis, seizure, cardiac_arrest, teamwork]
    plot_triple_bargraph(hosp_name, hosp_scores, const.ped_name, ped_scores, const.ged_name, ged_scores,
                         "Score %", "Performance Summary", ["EMSC Readiness Score", "Foreign Body Case Score",
                                                      "Sepsis Case Score", "Seizure Case Score", "Cardiac Arrest Score",
                                                            "Teamwork Score"], filename)

def get_cts_score(hosp_df, header):
    curr_df = hosp_df[header].T
    percent_score = 100*np.around(curr_df.sum()/(10*curr_df.count()), decimals=4)
    return percent_score

def create_ppt(input, output, report_data, chart):
    """ Take the input powerpoint file and use it as the template for the output
    file.
    """
    prs = Presentation(input)
    # Use the output from analyze_ppt to understand which layouts and placeholders
    # to use
    # Create a title slide first
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "Quarterly Report"
    subtitle.text = "Generated on {:%m-%d-%Y}".format(date.today())
