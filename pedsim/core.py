import constants as const
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    :param df: df obtained from get_hospital_data, it has only the row which corresponds
    to the answers obtained from a particular hospital
    :param case_headers: Questions for a particular case form the column names and this list
    contains those column names
    :return: dataframe with team number, questions and answers
    '''
    df1 = hosp_df.filter(like=case_headers[0]).T.reset_index()
    df2 = hosp_df.filter(like=case_headers[1]).T.reset_index()
    df = pd.concat([df1, df2])
    for i in range(2, len(case_headers)):
        curr_df = hosp_df.filter(like=case_headers[i]).T.reset_index()
        df = pd.concat([df, curr_df])
    case_df = df.reset_index()
    case_df.rename(mapper={'index': const.index_name, 'level_0': const.replicates,
                           0: const.hosp_ans}, axis='columns', inplace=True)
    return case_df

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
    plt.tight_layout()
    plt.savefig(fig_name)

def convert_truth_values_to_num(hosp_df):
    curr_df = hosp_df.replace('Yes', 1)
    curr_df = curr_df.replace('No', 0)
    return curr_df

def get_emsc_score(hosp_val_df, col_name, emsc_header, emsc_score):
    '''assume nan doesn't exist
    hosp_val_df : yes/no converted to 1/0
    '''
    total_score = sum(emsc_score)
    num = 0
    for header, val in zip(emsc_header, emsc_score):
        num = num + hosp_val_df.get_value(col_name, header)*val
    percent_score = 100*np.around(num/total_score, decimals=4)
    return percent_score

def plot_triple_bargraph(hosp_name, first_val_arr, second_name,
                         second_val_arr, third_name, third_val_arr, ylabel,
                         title, xlabels, filename):
    pos = list(range(len(first_val_arr)))
    width = 0.25
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.bar(pos, first_val_arr, width, alpha=0.5, color='r', label=hosp_name, capsize=2)
    plt.bar([p + width for p in pos], second_val_arr, width, alpha=0.5, color='g', label=second_name, capsize=2)
    plt.bar([p + 2 * width for p in pos], third_val_arr, width, alpha=0.5, color='b', label=third_name, capsize=2)
    ax.set_title(title)
    ax.set_xticks([p + width for p in pos])
    ax.set_xticklabels(xlabels, rotation="vertical")
    ax.set_ylabel(ylabel)
    plt.legend([hosp_name, second_name, third_name], loc="lower center", bbox_to_anchor=(1.1, 0.8))
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')


def plot_emsc_graph(hosp_name, qipi, staff, safety, equip, policy, filename):
    ged_scores = [const.ged_score["emsc_qipi"], const.ged_score["emsc_policy"], const.ged_score["emsc_safety"],
                  const.ged_score["emsc_staff"], const.ged_score["emsc_equip"]]
    ped_scores = [const.ped_score["emsc_qipi"], const.ped_score["emsc_policy"], const.ped_score["emsc_safety"],
                  const.ped_score["emsc_staff"], const.ped_score["emsc_equip"]]
    hosp_scores = [qipi, policy, safety, staff, equip]
    plot_triple_bargraph(hosp_name, hosp_scores, const.ped_name, ped_scores, const.ged_name, ged_scores, "Score %",
                         "EMSC Pediatric Readiness", ["Quality Improvement", "Policies/Procedures", "Patient Safety", "Physician/Nurse Staffing", "Equipment and Supplies"], filename)

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
