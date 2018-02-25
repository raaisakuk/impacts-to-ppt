import os
import pickle

import pandas as pd
import pedsim.core as core
import pedsim.constants as const

path_dir = os.path.join(os.path.dirname(__file__))
two_rows_df = pickle.load(open(os.path.join(path_dir, "hn.p"), "r"))
single_row_df = pickle.load(open(os.path.join(path_dir, "xb.p"), "r"))
hn_nofbddata = pickle.load(open(os.path.join(path_dir, "hn_nofbddata.p"), "r"))

fbd_df = pickle.load(open(os.path.join(path_dir, "hn_fbd.p"), "r"))
empty_fbd_case = pickle.load(open(os.path.join(path_dir, "empty_fbd_case.p"), "r"))
fbd_all_no = pickle.load(open(os.path.join(path_dir, "fbd_all_no.p"), "r"))
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

def test_get_case_performance_score_all_nan():
    assert core.get_case_performance_score(empty_fbd_case) == -1

def test_get_case_performance_score_all_no():
    assert core.get_case_performance_score(fbd_all_no) == 0

def test_get_case_performance_graph():
    core.get_case_performance_graph('Garfield', 'fbd', 50, 'test_plot.png')