import os
import pandas as pd
import analysis

dir_data = os.path.join("path",
                        "to",
                        "data",
                        "directory")

dir_output = os.path.join("path",
                          "to",
                          "output",
                          "file")

# Create dataframes
df_info = pd.DataFrame(columns=["sub_num", "datetime",
                                "condition", "age", "sex", "RA"])

df_ant = pd.DataFrame(columns=["sub_num",
    "ant_follow_error_rt", "ant_follow_correct_rt",
    "ant_neutral_rt", "ant_congruent_rt", "ant_incongruent_rt",
    "ant_neutral_rtsd", "ant_congruent_rtsd", "ant_incongruent_rtsd",
    "ant_neutral_rtcov", "ant_congruent_rtcov", "ant_incongruent_rtcov",
    "ant_neutral_correct", "ant_congruent_correct", "ant_incongruent_correct",
    "ant_nocue_rt", "ant_center_rt", "ant_spatial_rt", "ant_double_rt",
    "ant_nocue_rtsd", "ant_center_rtsd", "ant_spatial_rtsd", "ant_double_rtsd",
    "ant_nocue_rtcov", "ant_center_rtcov", "ant_spatial_rtcov", "ant_double_rtcov",
    "ant_nocue_correct", "ant_center_correct", "ant_spatial_correct", "ant_double_correct",
    "ant_conflict_intercept", "ant_conflict_slope", "ant_conflict_slope_norm",
    "ant_alerting_intercept", "ant_alerting_slope", "ant_alerting_slope_norm",
    "ant_orienting_intercept", "ant_orienting_slope", "ant_orienting_slope_norm"])

df_flanker_compat = pd.DataFrame(columns=["sub_num",
            "flanker_compat_follow_error_rt", "flanker_compat_follow_correct_rt",
            "flanker_compat_congruent_rt", "flanker_compat_incongruent_rt",
            "flanker_compat_congruent_rtsd", "flanker_compat_incongruent_rtsd",
            "flanker_compat_congruent_rtcov", "flanker_compat_incongruent_rtcov",
            "flanker_compat_congruent_correct", "flanker_compat_incongruent_correct",
            "flanker_compat_conflict_intercept", "flanker_compat_conflict_slope", "flanker_compat_conflict_slope_norm"])

df_flanker_incompat = pd.DataFrame(columns=["sub_num",
            "flanker_incompat_follow_error_rt", "flanker_incompat_follow_correct_rt",
            "flanker_incompat_congruent_rt", "flanker_incompat_incongruent_rt",
            "flanker_incompat_congruent_rtsd", "flanker_incompat_incongruent_rtsd",
            "flanker_incompat_congruent_rtcov", "flanker_incompat_incongruent_rtcov",
            "flanker_incompat_congruent_correct", "flanker_incompat_incongruent_correct",
            "flanker_incompat_conflict_intercept", "flanker_incompat_conflict_slope", "flanker_incompat_conflict_slope_norm"])

df_flanker_both = df_flanker_compat.merge(df_flanker_incompat, on="sub_num")
cols = list(df_flanker_both.columns.values)
cols.pop(cols.index("sub_num")) #  Remove sub_num from list
df_flanker_both = df_flanker_both[["sub_num"] + cols]

df_digit = pd.DataFrame(columns=["sub_num", "digit_correct_count",
                                 "digit_correct_prop", "digit_num_items"])

df_mrt = pd.DataFrame(columns=["sub_num", "mrt_count",
                               "mrt_prop", "mrt_num_items"])

df_ravens = pd.DataFrame(columns=["sub_num", "ravens_rt",
                                  "ravens_count", "ravens_prop", "ravens_num_items"])

df_sart = pd.DataFrame(
                columns=["sub_num", "sart_follow_error_rt", "sart_follow_correct_rt",
            "sart_total_rt", "sart_total_rtsd", "sart_total_rtcov",
            "sart_frequent_rt", "sart_frequent_rtsd", "sart_frequent_rtcov",
            "sart_infrequent_rt", "sart_infrequent_rtsd", "sart_infrequent_rtcov",
            "sart_error_count"," sart_errors_prop", "sart_errors_num_items"])

df_sternberg = pd.DataFrame(
                columns=["sub_num",
                "stern_follow_error_rt", "stern_follow_correct_rt",
                "stern_set_2_rt", "stern_set_6_rt",
                "stern_set_2_rtsd", "stern_set_6_rtsd",
                "stern_set_2_rtcov", "stern_set_6_rtcov",
                "stern_set_2_correct", "stern_set_6_correct",
                "stern_intercept", "stern_slope", "stern_slope_norm"])

# Aggregate all data
for f in os.listdir(dir_data):
    if f.endswith(".xls"):
        print("Summarizing {}".format(f))

        sub = pd.read_excel(os.path.join(dir_data, f), None, converters={"sub_num":str})

        sub_num = sub["info"].loc[0,"sub_num"]
        datetime = sub["info"].loc[0,"datetime"]
        condition = int(sub["info"]["condition"])
        age = int(sub["info"]["age"])
        sex = sub["info"].loc[0,"sex"]
        ra = sub["info"].loc[0,"RA"]

        for task, data in sub.items():
            if task == "info":
                df_info.loc[df_info.shape[0]] = [sub_num, datetime, condition, age, sex, ra]
            elif task == "ANT":
                # full / correct / incorrect
                df_ant.loc[df_ant.shape[0]] = analysis.aggregate_ant(data, sub_num, "full")
            elif task == "Digit span (backwards)":
                df_digit.loc[df_digit.shape[0]] = analysis.aggregate_digit_span(data, sub_num)
            elif task == "Eriksen Flanker":
                compat_conditions = data["compatibility"].unique()
                # full / correct / incorrect
                if len(compat_conditions) == 1 and compat_conditions == "compatible":
                    df_flanker_compat.loc[df_flanker_compat.shape[0]] = analysis.aggregate_flanker(data, sub_num, "full")
                elif len(compat_conditions) == 1 and compat_conditions == "incompatible":
                    df_flanker_incompat.loc[df_flanker_incompat.shape[0]] = analysis.aggregate_flanker(data, sub_num, "full")
                else:
                    df_flanker_both.loc[df_flanker_both.shape[0]] = analysis.aggregate_flanker(data, sub_num, "full")
            elif task == "MRT":
                df_mrt.loc[df_mrt.shape[0]] = analysis.aggregate_mrt(data, sub_num)
            elif task == "Ravens Matrices":
                df_ravens.loc[df_ravens.shape[0]] = analysis.aggregate_ravens(data, sub_num)
            elif task == "SART":
                df_sart.loc[df_sart.shape[0]] = analysis.aggregate_sart(data, sub_num)
            elif task == "Sternberg":
                # full / correct / incorrect
                df_sternberg.loc[df_sternberg.shape[0]] = analysis.aggregate_sternberg(data, sub_num, "full")

# Merge task data
## Only merge tasks that were used
tasks = [df_ant, df_digit, df_flanker_compat, df_flanker_incompat, df_flanker_both,
         df_mrt, df_ravens, df_sart, df_sternberg]

all_data = df_info
for task in tasks:
    if task.shape[0] != 0:
        all_data = all_data.merge(task, on="sub_num", how="left")

# Save output csv
all_data = all_data.sort_values("sub_num").reset_index(drop=True)
all_data.to_csv(os.path.join(dir_output, "battery_data.csv"), index=False, sep=",")
