import constants

def calc_score_binary(df, header_list):
    """"yes/no scores
    """
    subdf = df[[header_list]]
    score = subdf.iloc[0, :].value_counts(True).loc["Yes"]
    return score

