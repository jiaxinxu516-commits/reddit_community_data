from data_loader import load_data

from activity_analysis import activity_analysis
from feature_analysis import feature_analysis
from bug_analysis import bug_analysis

from dashboard import create_dashboard


def main():

    data = load_data("data/reddit_rokid_glasses_data.json")

    activity = activity_analysis(data)

    features = feature_analysis(data)

    bugs = bug_analysis(data)

    create_dashboard(
        activity,
        features,
        bugs
    )


if __name__ == "__main__":
    main()