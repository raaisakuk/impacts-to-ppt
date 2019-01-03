import os
import pickle

import pandas as pd
import numpy as np
import pytest

import pedsim.core as core
import pedsim.constants as const

path_dir = os.path.join(os.path.dirname(__file__))

two_rows_df = pickle.load(open(os.path.join(path_dir, "hn.p"), "r"))
two_rows_without_na_df = pickle.load(open(os.path.join(path_dir, "hn_without_na.p"), "r"))
single_row_df = pickle.load(open(os.path.join(path_dir, "xb.p"), "r"))
hn_nofbddata = pickle.load(open(os.path.join(path_dir, "hn_nofbddata.p"), "r"))
emsc_hosp_df = pickle.load(open(os.path.join(path_dir, "rt.p"), "r"))
cts_all_df = pickle.load(open(os.path.join(path_dir, "vm.p"), "r"))
cts_ind_some_miss = pickle.load(open(os.path.join(path_dir, "af.p"), "r"))
cts_ind_all = pickle.load(open(os.path.join(path_dir, "dh.p"), "r"))
overall_scores_df = pickle.load(open(os.path.join(path_dir, "overall_score.p"), "r"))

fbd_df = pickle.load(open(os.path.join(path_dir, "fbd.p"), "r"))
fbd_all_no = pickle.load(open(os.path.join(path_dir, "fbd_all_no.p"), "r"))

checklist_multiteams = pickle.load(open(os.path.join(path_dir, "checklist_multiteams.p"), "r"))
checklist_oneteam = pickle.load(open(os.path.join(path_dir, "checklist_oneteam.p"), "r"))

def test_get_hospital_data_two_rows():
    input_file = os.path.join(path_dir, "simulated_data_automation.xlsx")
    total_df, hn = core.get_hospital_data(input_file, "hn")
    assert pd.DataFrame.equals(hn[two_rows_df.columns], two_rows_df)

def test_get_hospital_data_single_row():
    input_file = os.path.join(path_dir, "simulated_data_automation.xlsx")
    total_df, xb = core.get_hospital_data(input_file, "xb")
    assert pd.DataFrame.equals(xb[single_row_df.columns], single_row_df)

def test_get_case_performance_data():
    case_df = core.get_case_performance_data(two_rows_df, const.foreign_body_case)
    assert pd.DataFrame.equals(case_df, fbd_df)

def test_get_case_performance_data_all_nan():
    case_df = core.get_case_performance_data(hn_nofbddata, const.foreign_body_case)
    assert np.isnan(case_df)

def test_get_case_performance_score():
    assert core.get_case_performance_score(fbd_df) == 50

def test_get_case_performance_score_all_no():
    assert core.get_case_performance_score(fbd_all_no) == 0

def test_get_case_performance_score_all_nan():
    score = core.get_case_performance_score(np.nan)
    assert np.isnan(score)

def test_get_case_performance_checklist_multiple_teams():
    checklist = core.get_case_performance_checklist(fbd_df)
    assert pd.DataFrame.equals(checklist, checklist_multiteams)

def test_get_case_performance_checklist_single_team():
    checklist = core.get_case_performance_checklist(fbd_all_no)
    assert pd.DataFrame.equals(checklist, checklist_oneteam)

def test_get_case_performance_graph_donut():
    fig = core.get_case_performance_graph_donut('medschool', 'fbd', 50)
    fig.savefig(os.path.join(path_dir,'test_plot1.png'))

def test_create_case_df_fig():
    case_df, fig, score = core.create_case_df_fig('hn', two_rows_df, const.foreign_body_case, 'fbd')
    fig.savefig(os.path.join(path_dir,'test_plot1.png'))

def test_get_emsc_score():
    emsc_score = core.get_emsc_score(emsc_hosp_df, const.qi_pi, const.qi_pi_score)
    assert emsc_score == 93.0

def test_get_total_emsc_score():
    assert core.get_total_emsc_score(60, 55, 70, 85, 30, 45) == 53.51

def test_get_emsc_score_nan():
    with pytest.raises(ValueError):
        core.get_emsc_score(two_rows_df, const.qi_pi, const.qi_pi_score)

def test_get_emsc_score():
    assert core.get_emsc_score(two_rows_without_na_df, const.qi_pi, const.qi_pi_score)==0

def test_plot_triple_bargraph():
    fig = core.plot_triple_bargraph('medschool', [50,60,30], 'ped', [78,56,35], 'ged',
                              [88,70,50], 'ylab', 'title', ['a', 'b', 'c'])
    fig.savefig(os.path.join(path_dir,'test_plot2.png'), bbox_inches='tight')

def test_plot_emsc_graph():
    fig = core.plot_emsc_graph('medschool', 60, 55, 70, 85, 30)
    fig.savefig(os.path.join(path_dir, 'test_plot3.png'), bbox_inches='tight')

def test_plot_performance_summary():
    fig = core.plot_performance_summary('medschool', 60, 55, 70, 85, 30, 45)
    fig.savefig(os.path.join(path_dir, 'test_plot4.png'), bbox_inches='tight')

def test_get_cts_score():
    assert core.get_cts_score(cts_all_df, const.cts_tool_all) == 80.0

def test_get_cts_score_all_nan():
    assert np.isnan(core.get_cts_score(single_row_df, const.cts_tool_all))

def test_get_cts_ind_score():
    assert core.get_cts_ind_score(cts_ind_all, const.cts_tool_ind_fbd) == 80.0

def test_get_cts_score_from_parts():
    assert core.get_cts_score_from_parts(cts_ind_all) == 84.75

def test_get_cts_score_from_parts_some_case_miss():
    assert core.get_cts_score_from_parts(cts_ind_some_miss) == 29.33

def test_get_overall_performance_scores():
    score_dict = core.get_overall_performance_scores(overall_scores_df)
    assert all([score_dict['Family Presence'] == 75.0, score_dict['Proper weight assessed'] == 75.0,
                score_dict['Disposition'] == 100.0, score_dict['Family centered care'] == 75.0,
               np.isnan(score_dict['Teamwork Evaluation: CTS Tool'])])

def test_update_average_scores():
    this_scores = {"sepsis": const.ped_score['ped_sepsis'], "fbd": const.ped_score['ped_fbd'],
         "seizure": const.ped_score['ped_seizure'], "cardiac_arrest": const.ped_score['ped_cardiac_arrest'],
         "teamwork": const.ped_score['ped_teamwork'], "emsc": const.ped_score['ped_emsc'],
         "emsc_qipi": const.ped_score['ped_emsc_qipi'], "emsc_staff": const.ped_score['ped_emsc_staff'],
         "emsc_safety": const.ped_score['ped_emsc_safety'], "emsc_equip": const.ped_score['ped_emsc_equip'],
         "emsc_policy": const.ped_score['ped_emsc_policy']}
    total_df = two_rows_without_na_df
    input_file = 'saved_ped_ged.xlsx'
    hosp_name = 'hn'
    total_df = core.initialise_df(total_df)
    if total_df["timestamp"].isna().all():
        core.update_average_scores(total_df, input_file, total_df, hosp_name, this_scores)
