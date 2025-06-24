import matplotlib.pyplot as plt
import seaborn as sns

def plot_top_skills(skills_df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=skills_df, x="Frequency", y="Skill", palette="magma", ax=ax)
    ax.set_title("Top In-Demand Tech Skills", fontsize=16)
    ax.set_xlabel("Frequency", fontsize=12)
    ax.set_ylabel("Skill", fontsize=12)
    plt.tight_layout()
    return fig
