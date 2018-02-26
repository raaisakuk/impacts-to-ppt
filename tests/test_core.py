import os
import pickle

import pandas as pd
import matplotlib.pyplot as plt

import pedsim.core as core
import pedsim.constants as const

path_dir = os.path.join(os.path.dirname(__file__))

two_rows_df = pickle.load(open(os.path.join(path_dir, "hn.p"), "r"))
single_row_df = pickle.load(open(os.path.join(path_dir, "xb.p"), "r"))
hn_nofbddata = pickle.load(open(os.path.join(path_dir, "hn_nofbddata.p"), "r"))
emsc_hosp_df = pickle.load(open(os.path.join(path_dir, "rt.p"), "r"))

fbd_df = pickle.load(open(os.path.join(path_dir, "hn_fbd.p"), "r"))
fbd_all_no = pickle.load(open(os.path.join(path_dir, "fbd_all_no.p"), "r"))

checklist_multiteams = pickle.load(open(os.path.join(path_dir, "checklist_multiteams.p"), "r"))
checklist_oneteam = pickle.load(open(os.path.join(path_dir, "checklist_oneteam.p"), "r"))
#pickle.dump(xb,open("xb.p","w"))

def test_get_hospital_data_two_rows():
    input_file = os.path.join(path_dir, "simulated_data_automation.xlsx")
    hn = core.get_hospital_data(input_file,"hn")
    assert pd.DataFrame.equals(hn, two_rows_df)

def test_get_hospital_data_single_row():
    input_file = os.path.join(path_dir, "simulated_data_automation.xlsx")
    xb = core.get_hospital_data(input_file, "xb")
    assert pd.DataFrame.equals(xb, single_row_df)

def test_get_case_performance_data():
    case_df = core.get_case_performance_data(two_rows_df, const.foreign_body_case)
    assert pd.DataFrame.equals(case_df, fbd_df)

def test_get_case_performance_data_all_nan():
    case_df = core.get_case_performance_data(hn_nofbddata, const.foreign_body_case)
    assert case_df == -1

def test_get_case_performance_score():
    assert core.get_case_performance_score(fbd_df) == 50

def test_get_case_performance_score_all_no():
    assert core.get_case_performance_score(fbd_all_no) == 0

def test_get_case_performance_checklist_multiple_teams():
    checklist = core.get_case_performance_checklist(fbd_df)
    assert pd.DataFrame.equals(checklist, checklist_multiteams)

def test_get_case_performance_checklist_single_team():
    checklist = core.get_case_performance_checklist(fbd_all_no)
    assert pd.DataFrame.equals(checklist, checklist_oneteam)

def test_get_case_performance_graph():
    fig = core.get_case_performance_graph('medschool', 'fbd', 50)
    fig.savefig(os.path.join(path_dir,'test_plot1.png'))

def test_get_emsc_score():
    assert core.get_emsc_score(emsc_hosp_df, const.qi_pi, const.qi_pi_score) == 92.86

def test_get_total_emsc_score():
    assert core.get_total_emsc_score(60, 55, 70, 85, 30, 45) == 57.5

def test_get_emsc_score_nan():
    assert core.get_emsc_score(two_rows_df, const.qi_pi, const.qi_pi_score) == -1

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