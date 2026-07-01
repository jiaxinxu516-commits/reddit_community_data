import os
import matplotlib.pyplot as plt


def create_dashboard(activity, features, bugs):
    """
    Reddit Community Dashboard
    """

    # ----------------------------
    # 创建输出文件夹
    # ----------------------------
    os.makedirs("output", exist_ok=True)

    # ----------------------------
    # Figure
    # ----------------------------
    fig, axs = plt.subplots(
        2,
        2,
        figsize=(15, 10)
    )

    fig.suptitle(
        "Reddit Community Intelligence Dashboard",
        fontsize=18,
        fontweight="bold"
    )

    ax1 = axs[0, 0]
    ax2 = axs[0, 1]
    ax3 = axs[1, 0]
    ax4 = axs[1, 1]

    # ====================================================
    # 1. Posts Over Time
    # ====================================================

    dates = list(activity["posts_per_day"].keys())
    counts = list(activity["posts_per_day"].values())

    ax1.plot(
        dates,
        counts,
        marker="o",
        linewidth=2
    )

    ax1.set_title("Posts Over Time")

    ax1.set_xlabel("Date")

    ax1.set_ylabel("Posts")

    ax1.grid(True)

    ax1.tick_params(
        axis="x",
        rotation=45
    )

    # ====================================================
    # 2. Feature Requests
    # ====================================================

    feature_names = list(features.keys())
    feature_counts = list(features.values())

    ax2.barh(
        feature_names,
        feature_counts
    )

    ax2.set_title("Top Feature Requests")

    ax2.set_xlabel("Mentions")

    for i, value in enumerate(feature_counts):

        ax2.text(
            value + 0.1,
            i,
            str(value),
            va="center"
        )

    # ====================================================
    # 3. Bug Analysis
    # ====================================================

    bug_names = list(bugs.keys())
    bug_counts = list(bugs.values())

    ax3.barh(
        bug_names,
        bug_counts
    )

    ax3.set_title("Bug Analysis")

    ax3.set_xlabel("Mentions")

    for i, value in enumerate(bug_counts):

        ax3.text(
            value + 0.1,
            i,
            str(value),
            va="center"
        )

    # ====================================================
    # 4. Community Summary
    # ====================================================

    avg_comments = 0

    if activity["posts"] != 0:

        avg_comments = (
            activity["comments"]
            / activity["posts"]
        )

    top_feature = "-"

    if len(features) > 0:

        top_feature = features.most_common(1)[0][0]

    top_bug = "-"

    if len(bugs) > 0:

        top_bug = bugs.most_common(1)[0][0]

    summary = f"""
Community Summary

Posts:
{activity['posts']}

Comments:
{activity['comments']}

Active Users:
{activity['users']}

Average Comments/Post:
{avg_comments:.2f}

Top Feature:
{top_feature}

Top Bug:
{top_bug}
"""

    ax4.text(
        0.02,
        0.98,
        summary,
        fontsize=13,
        verticalalignment="top"
    )

    ax4.axis("off")

    # ====================================================
    # Layout
    # ====================================================

    plt.tight_layout()

    # 给标题留空间
    plt.subplots_adjust(top=0.92)

    # 保存图片
    plt.savefig(
        "output/dashboard.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print("Dashboard saved to output/dashboard.png")