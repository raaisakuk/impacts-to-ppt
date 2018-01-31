import core
import constants as const

hosp_name = "Garfield Medical Center"
df = core.get_hospital_data("C:\Users\Raaisa\OneDrive\Yale\Sample_report_out_-_for_automation\Demo for Raaisa.xlsx",
                            hosp_name)

fbd_data = core.get_case_performance_data(df, const.foreign_body_case)
#sepsis_data = core.get_case_performance_data(df, const.sepsis)
seizure_data = core.get_case_performance_data(df, const.seizure)

core.get_case_performance_checklist(fbd_data[0], fbd_data[1], "fbd.csv")
fbd_score = core.get_case_performance_score(fbd_data[0], fbd_data[1])
core.get_case_performance_graph(hosp_name, "fbd", fbd_score, "fbd.png")
colname = fbd_data[1]
# core.get_case_performance_checklist(sepsis_data[0], sepsis_data[1], "sepsis.csv")
# sepsis_score = core.get_case_performance_score(sepsis_data[0], sepsis_data[1])
# core.get_case_performance_graph(hosp_name, "sepsis", sepsis_score, "sepsis.png")

core.get_case_performance_checklist(seizure_data[0], seizure_data[1], "seizure.csv")
seizure_score = core.get_case_performance_score(seizure_data[0], seizure_data[1])
core.get_case_performance_graph(hosp_name, "seizure", seizure_score, "seizure.png")

hosp_valdf = core.convert_truth_values_to_num(df)
qipi_val = core.get_emsc_score(hosp_valdf, colname, const.qi_pi, const.qi_pi_score)
admin_val = core.get_emsc_score(hosp_valdf, colname, const.admin, const.score_admin)
staff_val = core.get_emsc_score(hosp_valdf, colname, const.staff, const.score_staff)
safety_val = core.get_emsc_score(hosp_valdf, colname, const.safety, const.safety_score)
policy_val = core.get_emsc_score(hosp_valdf, colname, const.policy, const.policy_score)
equip_val = core.get_emsc_score(hosp_valdf, colname, const.equip, const.equip_score)

core.plot_emsc_graph(hosp_name, qipi_val, staff_val, safety_val, equip_val, policy_val, "emsc.png")

weight_data = core.get_case_performance_data(df, const.weight)
disposition = core.get_case_performance_data(df, const.disposition)
fam_pre = core.get_case_performance_data(df, const.family_pres)
fam_care = core.get_case_performance_data(df, const.family_care)

## . creating issues
core.get_case_performance_checklist(weight_data[0], colname, "weight.csv")
print core.get_case_performance_score(weight_data[0], colname)

core.get_case_performance_checklist(disposition[0], colname, "disposition.csv")
print core.get_case_performance_score(disposition[0], colname)

core.get_case_performance_checklist(fam_pre[0], colname, "fam_pre.csv")
print core.get_case_performance_score(fam_pre[0], colname)

core.get_case_performance_checklist(fam_care[0], colname, "fam_care.csv")
print core.get_case_performance_score(fam_care[0], colname)

print core.get_cts_score(df, const.cts_tool_all)

