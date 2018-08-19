import os
import sys

import core
import constants as const
import pptoutput as ppt

if __name__ == "__main__":
    hosp_name = sys.argv[1]
    survey_file = sys.argv[2]
    output_ppt_path = sys.argv[3]
    total_df, df = core.get_hospital_data(survey_file, hosp_name)

fbd_checklist, fbd_fig, fbd_score = core.create_case_df_fig(hosp_name, df, const.foreign_body_case, 'fbd')
sep_checklist, sep_fig, sep_score = core.create_case_df_fig(hosp_name, df, const.sepsis, 'sepsis')
sei_checklist, sei_fig, sei_score = core.create_case_df_fig(hosp_name, df, const.seizure, 'seizure')
cdar_checklist, cdar_fig, cdar_score = core.create_case_df_fig(hosp_name, df, const.cardiac_arrest, 'cardiac_arrest')

qipi_val = core.get_emsc_score(df, const.qi_pi, const.qi_pi_score)
admin_val = core.get_emsc_score(df, const.admin, const.score_admin)
staff_val = core.get_emsc_score(df, const.staff, const.score_staff)
safety_val = core.get_emsc_score(df, const.safety, const.safety_score)
policy_val = core.get_emsc_score(df, const.policy, const.policy_score)
equip_val = core.get_emsc_score(df, const.equip, const.equip_score)

emsc_fig = core.plot_emsc_graph(hosp_name, qipi_val, staff_val, safety_val, equip_val, policy_val)
emsc_score = core.get_total_emsc_score(qipi_val, admin_val, staff_val, safety_val, policy_val, equip_val)
emsc_case_fig = core.get_case_performance_graph_donut(hosp_name, 'emsc', emsc_score)

overall_dict = core.get_overall_performance_scores(df)
cts_score = overall_dict[const.cts_title]

overall_fig = core.plot_performance_summary(hosp_name, fbd_score, sep_score, cdar_score, cts_score, emsc_score, sei_score)
overall_df = core.create_overall_df(overall_dict)

this_scores = {"sepsis": sep_score, "fbd": fbd_score, "seizure": sei_score, "cardiac_arrest": cdar_score, "teamwork": cts_score, "emsc": emsc_score,
       "emsc_qipi": qipi_val, "emsc_staff": staff_val, "emsc_safety": safety_val, "emsc_equip": equip_val, "emsc_policy": policy_val}

if df["timestamp"].isna().all():
	core.update_average_scores(total_df, survey_file, hosp_name, this_scores)

ppt.create_ppt(os.path.join(output_ppt_path, hosp_name+'.pptx'), ['Foreign Body', 'Sepsis', 'Seizure','Cardiac arrest'], [fbd_fig, sep_fig, sei_fig, cdar_fig],
               [fbd_checklist, sep_checklist, sei_checklist, cdar_checklist],
               emsc_case_fig, emsc_fig, overall_fig, overall_df)
