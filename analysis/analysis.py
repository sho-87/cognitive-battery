import collections
import statsmodels.formula.api as smf


def aggregate_digit_span(data, sub_num):
    digit_correct_count = data["correct"].sum()
    digit_correct_num_items = data.shape[0]
    digit_correct_prop = digit_correct_count / digit_correct_num_items

    return [sub_num, digit_correct_count, digit_correct_prop, digit_correct_num_items]


def aggregate_mrt(data, sub_num):
    mrt_count = data["correct"].sum()
    mrt_num_items = data.shape[0]
    mrt_prop = mrt_count / mrt_num_items

    return [sub_num, mrt_count, mrt_prop, mrt_num_items]


def aggregate_ravens(data, sub_num):
    ravens_rt = data["RT"].mean()
    ravens_count = data["correct"].sum()
    ravens_num_items = data.shape[0]
    ravens_prop = ravens_count / ravens_num_items

    return [sub_num, ravens_rt, ravens_count, ravens_prop, ravens_num_items]


def aggregate_sart(data, sub_num):
    # Calculate times following errors and correct responses
    follow_error_rt = data.loc[data.accuracy.shift() == 0, "RT"].mean()
    follow_correct_rt = data.loc[data.accuracy.shift() == 1, "RT"].mean()

    total_rt = data["RT"].mean()
    total_rtsd = data["RT"].std()
    total_rtcov = total_rtsd / total_rt

    frequent_rt = data[data["stimulus"] != 3]["RT"].mean()
    frequent_rtsd = data[data["stimulus"] != 3]["RT"].std()
    frequent_rtcov = frequent_rtsd / frequent_rt

    infrequent_rt = data[data["stimulus"] == 3]["RT"].mean()
    infrequent_rtsd = data[data["stimulus"] == 3]["RT"].std()
    infrequent_rtcov = infrequent_rtsd / infrequent_rt

    sart_error_count = data[data["stimulus"] == 3]["key press"].sum()
    sart_errors_num_items = collections.Counter(data['stimulus'])[3]
    sart_errors_prop = sart_error_count / sart_errors_num_items

    return [sub_num, follow_error_rt, follow_correct_rt,
            total_rt, total_rtsd, total_rtcov,
            frequent_rt, frequent_rtsd, frequent_rtcov,
            infrequent_rt, infrequent_rtsd, infrequent_rtcov,
            sart_error_count, sart_errors_prop, sart_errors_num_items]


def aggregate_ant(data, sub_num, response_type="full"):

    # Calculate times following errors and correct responses
    df = data
    follow_error_rt = df.loc[df.correct.shift() == 0, "RT"].mean()
    follow_correct_rt = df.loc[df.correct.shift() == 1, "RT"].mean()

    if response_type == "correct":
        df = data[data["correct"] == 1]
    elif response_type == "incorrect":
        df = data[data["correct"] == 0]
    elif response_type == "full":
        df = data

    # Aggregated descriptives

    ## congruency conditions
    grouped_congruency = df.groupby("congruency")
    neutral_rt = grouped_congruency.mean().get_value("neutral", "RT")
    congruent_rt = grouped_congruency.mean().get_value("congruent", "RT")
    incongruent_rt = grouped_congruency.mean().get_value("incongruent", "RT")

    neutral_rtsd = grouped_congruency.std().get_value("neutral", "RT")
    congruent_rtsd = grouped_congruency.std().get_value("congruent", "RT")
    incongruent_rtsd = grouped_congruency.std().get_value("incongruent", "RT")

    neutral_rtcov = neutral_rtsd / neutral_rt
    congruent_rtcov = congruent_rtsd / congruent_rt
    incongruent_rtcov = incongruent_rtsd / incongruent_rt

    neutral_correct = grouped_congruency.sum().get_value("neutral", "correct")
    congruent_correct = grouped_congruency.sum().get_value("congruent", "correct")
    incongruent_correct = grouped_congruency.sum().get_value("incongruent", "correct")

    ## cue conditions
    grouped_cue = df.groupby("cue")
    nocue_rt = grouped_cue.mean().get_value("nocue", "RT")
    center_rt = grouped_cue.mean().get_value("center", "RT")
    spatial_rt = grouped_cue.mean().get_value("spatial", "RT")
    double_rt = grouped_cue.mean().get_value("double", "RT")

    nocue_rtsd = grouped_cue.std().get_value("nocue", "RT")
    center_rtsd = grouped_cue.std().get_value("center", "RT")
    spatial_rtsd = grouped_cue.std().get_value("spatial", "RT")
    double_rtsd = grouped_cue.std().get_value("double", "RT")

    nocue_rtcov = nocue_rtsd / nocue_rt
    center_rtcov = center_rtsd / center_rt
    spatial_rtcov = spatial_rtsd / spatial_rt
    double_rtcov = double_rtsd / double_rt

    nocue_correct = grouped_cue.sum().get_value("nocue", "correct")
    center_correct = grouped_cue.sum().get_value("center", "correct")
    spatial_correct = grouped_cue.sum().get_value("spatial", "correct")
    double_correct = grouped_cue.sum().get_value("double", "correct")

    # OLS regression
    conflict_df = df[(df["congruency"] == "congruent") | (df["congruency"] == "incongruent")]
    formula_conflict = "RT ~ C(congruency, Treatment(reference='congruent'))"
    ols_results = smf.ols(formula_conflict, conflict_df).fit()
    conflict_intercept, conflict_slope = ols_results.params
    conflict_slope_norm = conflict_slope / congruent_rt

    alerting_df = df[(df["cue"] == "double") | (df["cue"] == "nocue")]
    formula_alerting = "RT ~ C(cue, Treatment(reference='double'))"
    ols_results = smf.ols(formula_alerting, alerting_df).fit()
    alerting_intercept, alerting_slope = ols_results.params
    alerting_slope_norm = alerting_slope / double_rt

    orienting_df = df[(df["cue"] == "spatial") | (df["cue"] == "center")]
    formula_orienting = "RT ~ C(cue, Treatment(reference='spatial'))"
    ols_results = smf.ols(formula_orienting, orienting_df).fit()
    orienting_intercept, orienting_slope = ols_results.params
    orienting_slope_norm = orienting_slope / spatial_rt

    return [sub_num,
            follow_error_rt, follow_correct_rt,
            neutral_rt, congruent_rt, incongruent_rt,
            neutral_rtsd, congruent_rtsd, incongruent_rtsd,
            neutral_rtcov, congruent_rtcov, incongruent_rtcov,
            neutral_correct, congruent_correct, incongruent_correct,
            nocue_rt, center_rt, spatial_rt, double_rt,
            nocue_rtsd, center_rtsd, spatial_rtsd, double_rtsd,
            nocue_rtcov, center_rtcov, spatial_rtcov, double_rtcov,
            nocue_correct, center_correct, spatial_correct, double_correct,
            conflict_intercept, conflict_slope, conflict_slope_norm,
            alerting_intercept, alerting_slope, alerting_slope_norm,
            orienting_intercept, orienting_slope, orienting_slope_norm]


def aggregate_sternberg(data, sub_num, response_type="full"):

    # Calculate times following errors and correct responses
    df = data
    follow_error_rt = df.loc[df.correct.shift() == 0, "RT"].mean()
    follow_correct_rt = df.loc[df.correct.shift() == 1, "RT"].mean()

    if response_type == "correct":
        df = data[data["correct"] == 1]
    elif response_type == "incorrect":
        df = data[data["correct"] == 0]
    elif response_type == "full":
        df = data

    # Aggregated descriptives
    grouped_set_size = df.groupby("setSize")
    set_2_rt = grouped_set_size.mean().get_value(2, "RT")
    set_2_rtsd = grouped_set_size.std().get_value(2, "RT")
    set_2_rtcov = set_2_rtsd / set_2_rt
    set_2_correct = grouped_set_size.sum().get_value(2, "correct")

    set_6_rt = grouped_set_size.mean().get_value(6, "RT")
    set_6_rtsd = grouped_set_size.std().get_value(6, "RT")
    set_6_rtcov = set_6_rtsd / set_6_rt
    set_6_correct = grouped_set_size.sum().get_value(6, "correct")

    # OLS regression
    formula = "RT ~ C(setSize, Treatment(reference=2))"
    ols_results = smf.ols(formula, df).fit()
    intercept, slope = ols_results.params
    slope_norm = slope / set_2_rt

    return [sub_num,
            follow_error_rt, follow_correct_rt,
            set_2_rt, set_6_rt,
            set_2_rtsd, set_6_rtsd,
            set_2_rtcov, set_6_rtcov,
            set_2_correct, set_6_correct,
            intercept, slope, slope_norm]
