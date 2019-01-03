#!/usr/bin/python
# -*- coding: utf-8 -*-

##Changes made in raw file
##Changed column names which had small differences

##Column name which contains hospital names
site_hosp = "Enter the site's Hospital name"

##
hosprow_col = 0
index_name = "questions"
replicates = "team_num"
hosp_ans = 'survey_ans'
timestamp = 'timestamp'

##
team_dict = {0: "Team 1", 1: "Team 2", 2: "Team 3",
             3: "Team 4", 4: "Team 5", 5: "Team 6"}

##Headers for score calculations##
foreign_body_case = ["Foreign body case - Airway assessed (Look in mouth in first 3 min)",
                     "Foreign body case - Breathing assessed (Listen to lungs with stethoscope in 1st 3 min)",
                     "Foreign body case - Proper size McGill forceps used to remove foreign body (Pediatric not adult)  0 Check if finger used to remove",
                     "Foreign body case - Stridor verbalized (in 1st 3min)"]
fbd_replacement = {foreign_body_case[0]: "Airway assessed",
                   foreign_body_case[1]: "Breathing assessed",
                   foreign_body_case[2]: "McGill forceps used",
                   foreign_body_case[3]: "Stridor verbalized"}

sepsis = ["Sepsis case - Established 1st IV/IO (In first 3 min)",
          "Sepsis case - Began oxygen non-rebreather in first 3 min. Mention if other equipment (nasal cannula; simple mask; nothing) was used",
          "Sepsis case - 360 CC NS delivered in first 15 min. Total fluids given over 15 min case in mL:",
          "Sepsis case - Established 2nd IV/IO",
          "Sepsis case - Push-pull technique used 3-way stop-cock",
          "Sepsis case - Appropriate antibiotics given Ceftriaxone 240-720 mg AND Vancomycin 48-150mg",
          "Sepsis case - Any vasopressor given after 3rd bolus  Dopamine 25-80 mcg/min or Norepi 0.2-0.7 mcg/min or Epi 0.5-0.7 mcg/min"]
sep_replacement = {sepsis[0]: "Establish 1st IV/IO",
                   sepsis[1]: "Began high-flow O2",
                   sepsis[2]: "60mL/kg given over 15min",
                   sepsis[3]: "Establish 2nd IV/IO",
                   sepsis[4]: "Push-pull techniques used",
                   sepsis[5]: "Appropriate antibiotics given",
                   sepsis[6]: "Start 3rd vasopressor after 3rd bolus"}

seizure = ["Seizure case - Respiratory depression verbalized first 3 minutes.",
           "Seizure case - Began oxygen non rebreather in first 3 min. Mention if other (Nasal Cannula; Simple mask; nothing) was used.",
           "Seizure case - Bedside glucose checked first 3 min",
           "Seizure case - IV/IO Placed first 5 min",
           "Seizure case - Administered glucose D5 or 10 concentration. Mention if any other (D25/D50) was used",
           "Seizure case - Glucose dose correct D5: 48-144ccD10: 24-72cc",
           "Seizure case - ANY maintenance glucose infusion started"]
sei_replacement = {seizure[0]: "Respiratory depression recognised",
           seizure[1]: "Placed on O2",
           seizure[2]: "Bedside glucose checked",
           seizure[3]: "IV/IO placed",
           seizure[4]: "Correct glucose concentration",
           seizure[5]: "Correct Glucose dose",
           seizure[6]: "Maintenance glucose started"}

cardiac_arrest = ["Cardiac arrest case - CPR started in <30 sec",
                  "Cardiac arrest case - Backboard used",
                  "Cardiac arrest case - Pulse check < 120 sec into case",
                  "Cardiac arrest case - IV/IO placed",
                  "Cardiac arrest case - PEA verbalized",
                  "Cardiac arrest case - Epinephrine 1 given 1.6-2.4 mL IV 1:10K ETT 1:1K< 5mincase",
                  "Cardiac arrest case - Epinephrine 2 given 1.6-2.4 mL IV 1:10K ETT 1:1K 3-5 min after first epi",
                  "Cardiac arrest case - Continuous ETCO2 monitoring",
                  "Cardiac arrest case - Ventricular fib verbalized",
                  "Cardiac arrest case - Defibrillation dose 32-100J",
                  "Cardiac arrest case - <10 sec stop/pause CPR preshock",
                  "Cardiac arrest case - Defib safety: cleared people/O2",
                  "Cardiac arrest case - CPR resumed <10 seconds DEFIB cont 120sec",
                  "Cardiac arrest case - Patient intubated pause CPR <10sec",
                  "Cardiac arrest case - Correct intubation equipment 3.5-4.5 cuffed, 4.5-5.5 uncuffed, 2/3 Miller/Mac",
                  "Cardiac arrest case - Correct hand location",
                  "Cardiac arrest case - Correct depth",
                  "Cardiac arrest case - Adequate recoil",
                  "Cardiac arrest case - ROSC stated",
                  "Cardiac arrest case - Compression rate between 100-120/min?",
                  "Cardiac arrest case - Ventilation rate between 8-10/min?",
                  "Cardiac arrest case - ALL CPR cycles 120",
                  "Cardiac arrest case - No interruptions > 10 seconds (Count any pause in CPR except pre-shock)"]
cardiac_replacement = {cardiac_arrest[0]: "CPR started in <30 sec",
                  cardiac_arrest[1]: "Backboard used",
                  cardiac_arrest[2]: "Pulse check < 120 sec into case",
                  cardiac_arrest[3]: "IV/IO placed",
                  cardiac_arrest[4]: "PEA verbalized",
                  cardiac_arrest[5]: "1st dose of Epi in <5min",
                  cardiac_arrest[6]: "2nd dose of Epi in 2-3min after 1st",
                  cardiac_arrest[7]: "Continuous ETCO2 monitoring",
                  cardiac_arrest[8]: "Ventricular fib verbalized",
                  cardiac_arrest[9]: "Defibrillation dose 32-100J",
                  cardiac_arrest[10]: "<10 sec stop/pause CPR preshock",
                  cardiac_arrest[11]: "Defib safety: cleared people/O2",
                  cardiac_arrest[12]: "CPR resumed immediately after DEFIB cont 120sec",
                  cardiac_arrest[13]: "Patient intubated pause <10sec",
                  cardiac_arrest[14]: "Intubation equipment",
                  cardiac_arrest[15]: "Correct hand location",
                  cardiac_arrest[16]: "Correct depth",
                  cardiac_arrest[17]: "Adequate recoil",
                  cardiac_arrest[18]: "ROSC stated",
                  cardiac_arrest[19]: "Compression rate between 100-120/min",
                  cardiac_arrest[20]: "Ventilation rate between 8-10/min",
                  cardiac_arrest[21]: "ALL CPR cycles 120",
                  cardiac_arrest[22]: "No interruptions > 10 seconds"}

case_map = {'fbd': fbd_replacement,
            'sepsis': sep_replacement,
            'seizure': sei_replacement,
            'cardiac_arrest': cardiac_replacement}

##TeamWork Evaluation Table

weight = ["Foreign body case - Proper weight assessed 6kg (4.8-7.2)",
          "Sepsis case - Proper weight assessed 6 kg (4.8-7.2)",
          "Seizure case - Proper weight assessed 6 kg (4.8-7.2)",
          "Cardiac arrest case - Proper weight assessed 16-24 kg"]
weight_title = 'Proper weight assessed'

disposition = ["Sepsis case - Disposition: contacted PICU/transport to arrange xfer",
               "Seizure case - Disposition: plan to admit/transfer verbalized",
               "Cardiac arrest case - Disposition: contacted PICU/transport to arrange xfer"]
disposition_title = 'Disposition'

family_pres = ["Foreign body case - Family presence   (Parent asked to stay)",
              "Sepsis case - Family presence    Parent asked to stay",
              "Seizure case - Family presence   Parent asked to stay",
              "Cardiac arrest case - Family presence   Parent asked to stay"]
family_pres_title = 'Family Presence'

family_care = ["Cardiac arrest case - Family centered care Team interacted with parent throughout",
              "Foreign body case - Family centered care (Team interacted with parent throughout case)",
              "Seizure case - Family centered care (Team interacted with parent throughout case)",
              "Sepsis case - Family centered care  Team interacted with parent throughout case"]
family_care_title = 'Family centered care'

##CTS Tool
cts_tool_all = ["Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall: How would you rate teamwork during this delivery/emergency?",
                "Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Communication Rating:",
                "Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication : Orient new members (SBAR)",
                "Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication:  Transparent thinking",
                "Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication : Directed communication",
                "Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication : Closed loop communication",
                "Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Situational Awareness Rating:",
                "Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Situational Awareness:            Resource allocation",
                "Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Decision Making Rating:",
                "Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Decision Making: Prioritize",
                "Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Role Responsibility (Leader/Helper) Rating:",
                "Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility: Role clarity",
                "Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility: Perform as a leader",
                "Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility: Perform as a helper",
                "Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Patient friendly"]

cts_tool_ind_fbd = ["Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall: How would you rate teamwork during this delivery/emergency?",
                "Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Communication Rating:",
                "Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication : Orient new members (SBAR)",
                "Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication: Transparent thinking",
                "Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication : Directed communication",
                "Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication: Closed loop communication",
                "Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall situational awareness rating",
                "Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Situational Awareness:            Resource allocation",
                "Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall decision making rating",
                "Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Decision Making: Prioritize",
                "Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Role Responsibility (Leader/Helper) Rating",
                "Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility : Role clarity",
                "Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility : Perform as a leader",
                "Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility :  Perform as a helper",
                "Foreign Body - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Patient friendly"]

cts_tool_ind_sep = ["Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall: How would you rate teamwork during this delivery/emergency?",
                "Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Communication Rating:",
                "Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication:  Orient new members (SBAR)",
                "Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication : Transparent thinking",
                "Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication : Directed communication",
                "Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication: Closed loop communication",
                "Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Situational Awareness Rating:",
                "Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Situational Awareness: Resource allocation",
                "Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Decision Making Rating:",
                "Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Decision Making : Prioritize",
                "Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Role Responsibility (Leader/Helper) Rating:",
                "Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility : Role clarity",
                "Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility : Perform as a leader",
                "Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility : Perform as a helper",
                "Sepsis - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Patient friendly"]

cts_tool_ind_seiz = ["Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall: How would you rate teamwork during this delivery/emergency?",
                "Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Communication Rating:",
                "Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication: Orient new members (SBAR)",
                "Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication : Transparent thinking",
                "Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication: Directed communication",
                "Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication: Closed loop communication",
                "Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Situational Awareness Rating:",
                "Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Situational Awareness: Resource allocation",
                "Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Decision Making Rating:",
                "Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Decision Making: Prioritize",
                "Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Role Responsibility (Leader/Helper) Rating:",
                "Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility : Role clarity",
                "Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility : Perform as a leader",
                "Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility: Perform as a helper",
                "Seizure - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Patient friendly"]

cts_tool_ind_cardiac = ["Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall: How would you rate teamwork during this delivery/emergency?",
                "Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Communication Rating:",
                "Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication : Orient new members (SBAR)",
                "Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication : Transparent thinking",
                "Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication: Directed communication",
                "Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Communication: Closed loop communication",
                "Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Situational Awareness Rating:",
                "Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Situational Awareness:            Resource allocation",
                "Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Decision Making Rating:",
                "Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Decision Making: Prioritize",
                "Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Overall Role Responsibility (Leader/Helper) Rating:",
                "Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility: Role clarity",
                "Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility: Perform as a leader",
                "Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Role Responsibility : Perform as a helper",
                "Cardiac Arrest - Clinical Teamwork Scale (CTS) Not relevant- The task was not applicable to the scenario - Patient friendly"]

cts_title = 'Teamwork Evaluation: CTS Tool'

##EMSC
admin = ["11. Does your hospital have a physician coordinator? (e.g., oversees quality improvement, collaborates with nursing, ensures pediatric skills of staff, develops and periodically reviews policies)",
        "13. Does your hospital have a nurse coordinator? (e.g., facilitates continuing education, facilitates quality improvement activities, ensures pediatric-specific elements are included in orientation of staff)?Note: The nurse coordinator for pediatric emergency care may have additional administrative roles in the ED."]
score_admin = [9.5, 9.5]

staff = ["17. Does your hospital require specific peds competency evaluations of physicians?  (e.g., sedation and analgesia)",
    "20. Does your hospital require specific peds competency evaluations of nurses? (e.g., triage, pain assessment)"]
score_staff = [5, 5]

qi_pi = ["25. Does your ED have a peds patient care-review process? (This may be a separate Quality Improvement/Performance Improvement Plan for pediatric patients or integrated into the overall ED Quality Improvement/Performance Improvement Plan.)",
    "26. If yes, is each of the following components included in the QI/PI plan? - a. Identification of quality indicators for children (e.g., performing lumbar puncture on febrile neonates)",
    "26. If yes, is each of the following components included in the QI/PI plan? - b. Collection and analysis of peds emergency care data (e.g., admissions, transfers, death in the ED, or return visits)",
    "26. If yes, is each of the following components included in the QI/PI plan? - c. Development of a plan for improvement in pediatric emergency care e (e.g., process to ensure that variances in care are addressed through education or training and reassessed for evidence of improvement)",
    "26. If yes, is each of the following components included in the QI/PI plan? - d. Re-evaulation of performance using outcomes-based measures (e.g., how often pain was rapidly controlled or fever properly treated)"]
qi_pi_score = [5, 0.5, 0.5, 0.5, 0.5]

safety = ["28. Is the weight recorded in the ED medical record in kilograms only?",
          "Pediatric safety in the ED - 30. Temp, heart rate, respiratory rate recorded?",
          "Pediatric safety in the ED - 31. Blood pressure monitoring available for children of all ages based on severity of illness",
          "Pediatric safety in the ED - 32. Pulse ox monitoring available for children of all ages based on severity of illness?",
          "Pediatric safety in the ED - 33. Written procedure in place for notification of physicians when abnormal vital signs are found in all children ?",
          "Pediatric safety in the ED - 34. Process in place for use of pre-calculated drug dosing",
          "Pediatric safety in the ED - 35. Is a process in place that allows for 24/7 access to interpreter services in the ED?"]
safety_score = [3.5, 1.4, 1.4, 1.4, 1.4, 3.5, 1.4]

policy = ["36.Does your ED have a triage policy that specifically addresses ill and injured children?",
            "Other policies/procedures - 38a. Does your ED have pediatric patient assessment/reassessment",
            "Other policies/procedures - 38b. Immunization assessment and management?",
            "Other policies/procedures - 38c. Child maltreatment?",
            "Other policies/procedures - 38d. Death of the child in the ED",
            "Other policies/procedures - 38e. Reduced-dose radiation for CT and x-ray imaging based on pediatric age or weight",
            "Other policies/procedures - 39. Does your ED have a policy for promoting family-centered care?(e.g., family presence, family involvement in clinical decision making, etc.)",
            "Other policies/procedures - 40. Does your hospital disaster plan address issues specific to care of children?",
            "43. Does your hospital have written inter-facility guidelines that outline procedural and administrative policies with other hospitals for the transfer of patients of all ages including children in need of care not available at your hospital? (Note: Compliance with EMTALA does not constitute having inter-facility transfer guidelines. The guidelines may be a separate document or part of an inter-facility transfer agreement document.)"]
policy_score = [2.12, 1.7, 1.7, 1.7, 1.7, 1.7, 2.12, 2.12, 2.12]

equip = ["Equipment / Supplies - 46. Is the ED staff trained on the location of all pediatric equipment and meds?",
            "Equipment / Supplies - 47. Is there a daily method used to verify the proper location and function of ped equipment and supplies?",
            "Equipment / Supplies - 48. Is a med chart, length-based tape, medical software, or other system readily available to ensure proper sizing of resuscitation equipment and proper dosing of meds?",
            "Equipment / Supplies - 49a. Is a neonatal blood pressure cuff available for immediate use in the ED?",
            "Equipment / Supplies - 49b. Infant blood pressure cuff",
            "Equipment / Supplies - 49c. Child blood pressure cuff",
            "Equipment / Supplies - 49d. Defibrillator with ped and adult capabilities including pads/paddles",
            "Equipment / Supplies - 49e. Pulse oximeter with ped and adult probes",
            "Equipment / Supplies - 49f. Continuous end-tidal CO2 monitoring defice",
            "Equipment / Supplies - 50a. 22 gauge catheter-over-the-needle",
         "Equipment / Supplies - 50b. 24gauge catheter-over-the-needle",
            "Equipment / Supplies - 50c. Pediatric IO needle",
            "Equipment / Supplies - 50d. IV administration with calibrated chambers and extension tubing and/or infusion devices with ability to regulate rate & volume of infusate",
            "Equipment / Supplies - 50e. Umbilical vein catheters (3.5 F or 5F)",
            "Equipment / Supplies - 50f. Central venous catheters (any two sizes in range, 4F-7F)",
            "Equipment / Supplies - 51a. Endotracheal tubes: cuffed or uncuffed 2.5 mm",
            "Equipment / Supplies - 51b. Endotracheal tubes: cuffed or uncuffed 3.0 mm",
            "Equipment / Supplies - 51c. Endotracheal tubes: cuffed or uncuffed 3.5 mm",
            "Equipment / Supplies - 51d. Endotracheal tubes: cuffed or uncuffed 4.0 mm",
            "Equipment / Supplies - 51e. Endotracheal tubes: cuffed or uncuffed 4.5 mm",
            "Equipment / Supplies - 51f. Endotracheal tubes: cuffed or uncuffed 5.0 mm",
            "Equipment / Supplies - 51g. Endotracheal tubes: cuffed or uncuffed 5.5 mm",
            "Equipment / Supplies - 51h. Endotracheal tubes: cuffed 6 mm",
            "Equipment / Supplies - 51i. Laryngoscope blades: straight, size 00",
            "Equipment / Supplies - 51j. Laryngoscope blades: straight, size 0",
            "Equipment / Supplies - 51k. Laryngoscope blades: straight, size 1",
            "Equipment / Supplies - 51l. Laryngoscope blades: straight, size 2",
            "Equipment / Supplies - 51m. Laryngoscope blades: curved, size 2",
            "Equipment / Supplies - 51n. Pediatric-sized Mcgill forceps",
            "Equipment / Supplies - 51o. Nasopharyngeal airways: infant-sized",
            "Equipment / Supplies - 51p. Nasopharyngeal airways: child-sized",
            "Equipment / Supplies - 51q. Oropharyngeal airways: size 0 (50 mm)",
            "Equipment / Supplies - 51r. Oropharyngeal airways: size 1 (60 mm)",
            "Equipment / Supplies - 51s. Oropharyngeal airways: size 2 (70 mm)",
            "Equipment / Supplies - 51t. Oropharyngeal airways: size 3 (80 mm)",
            "Equipment / Supplies - 51u. Stylets for ped/infant-sized ET tubes",
            "Equipment / Supplies - 51v. Tracheostomy tubes: size 3.0 mm",
            "Equipment / Supplies - 51w. Tracheostomy tubes: size 3.5 mm",
            "Equipment / Supplies - 51x. Tracheostomy tubes: size 4.0 mm",
            "Equipment / Supplies - 51y. Bag-mask device, self-inflating, 450 ml",
            "Equipment / Supplies - 51z. Masks to fit bag-mask device adaptor: neonatal",
            "Equipment / Supplies - 51aa. Masks to fit bag-mask device adaptor: infant",
            "Equipment / Supplies - 51bb. Masks to fit bag-mask device adaptor: child",
            "Equipment / Supplies - 51cc. Clear oxygen masks: standard infant",
            "Equipment / Supplies - 51dd. Clear oxygen masks: standard child",
            "Equipment / Supplies - 51ee. Non-rebreather masks: infant",
            "Equipment / Supplies - 51ff. Non-rebreather masks: child",
            "Equipment / Supplies - 51gg. Nasal cannulas: infant",
            "Equipment / Supplies - 51hh. Nasal cannulas: child",
            "Equipment / Supplies - 51ii. Laryngeal mask airways: size 1",
            "Equipment / Supplies - 51jj. Laryngeal mask airways: size 1.5",
            "Equipment / Supplies - 51kk. Laryngeal mask airways: size 2",
            "Equipment / Supplies - 51ll. Laryngeal mask airways: size 2.5",
            "Equipment / Supplies - 51mm. Laryngeal mask airways: size 3",
            "Equipment / Supplies - 51nn. Suction catheters: at least one in range of 6-8F",
            "Equipment / Supplies - 51oo. Suction catheters: at least one in range of 10-12F",
            "Supplies/kit for pediatric patients with difficult airways (supraglottic airways of all sizes, needle cricothyrotomy supplies, surgical cricothyrotomy kit)"]
equip_score = [1, 1, 1, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55,
               0.55, 0.55, 0.55, 0.550, 0.557, 0.557, 0.557, 0.557, 0.557,
               0.557, 0.557, 0.557, 0.557, 0.557, 0.557, 0.557, 0.557, 0.557,
               0.557, 0.557, 0.557, 0.557, 0.557, 0.557, 0.557, 0.557, 0.557,
               0.557, 0.557, 0.557, 0.557, 0.557, 0.557, 0.557, 0.557, 0.557,
               0.557, 0.557, 0.557, 0.557, 0.557, 0.557, 0.557, 0.557, 0.557, 0.557]

##GED and PED
ged_name = "GED"
ped_name = "PED"
ed_category = "6. Which of the following is the best description of your ED for the care of children?"
ped_category = "Pediatric ED in a Children's Hospital (hospital cares ONLY for children)"

ped_color = "#E3E3E3"
ged_color = "#03A89E"
hosp_color = "#00BFFF"


case_name_dict = {'sepsis': 'Sepsis', 'cardiac_arrest': 'Cardiac Arrest', 'seizure': 'Seizure',
                  'fbd': 'Foreign Body', 'emsc':'EMSC Readiness'}
case_error_message = "Following question has been answered by different number of teams:\n\t"
column_name_error_message = "Excel sheet should contain exactly "+str(len(team_dict))+" columns with following name:\n\t"
column_not_empty_message = "Following column cannot be empty:\n\t"


######################################################################################
############################# CONFIGURE THE VALUES BELOW #############################
######################################################################################


total_ged_count = 0
total_ped_count = 0

ged_score = {"ged_sepsis": 73, "ged_fbd": 80, "ged_seizure": 68, "ged_cardiac_arrest": 52, "ged_teamwork": 74, "ged_emsc": 64,
       "ged_emsc_qipi": 36, "ged_emsc_staff": 60, "ged_emsc_safety": 72, "ged_emsc_equip": 84, "ged_emsc_policy": 53}

ped_score = {"ped_sepsis": 100, "ped_fbd": 80, "ped_seizure": 78, "ped_cardiac_arrest": 67, "ped_teamwork": 86, "ped_emsc": 90,
       "ped_emsc_qipi": 81, "ped_emsc_staff": 85, "ped_emsc_safety": 76, "ped_emsc_equip": 98, "ped_emsc_policy": 92}
