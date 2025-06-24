import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns
import datetime

def simulate_dates(df, start_date="2023-01-01", end_date="2024-12-31"):
    np.random.seed(42)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    df["date_added"] = np.random.choice(date_range, size=len(df))
    return df

def prepare_skill_timeseries(df, skill):
    df = simulate_dates(df.copy())
    df["date_added"] = pd.to_datetime(df["date_added"])
    df["skill_mentioned"] = df["job_description"].str.lower().str.contains(skill.lower()).astype(int)
    daily = df.groupby(df["date_added"].dt.to_period("M"))["skill_mentioned"].sum().reset_index()
    daily["date"] = daily["date_added"].dt.to_timestamp()
    return daily

def forecast_skill_trend(daily_df, months_ahead=6):
    # Prepare data
    daily_df = daily_df.copy()
    daily_df["month_num"] = (daily_df["date"] - daily_df["date"].min()).dt.days
    X = daily_df["month_num"].values.reshape(-1, 1)
    y = daily_df["skill_mentioned"].values

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Forecast future months
    future_months = np.arange(X.max() + 30, X.max() + 30*(months_ahead+1), 30).reshape(-1, 1)
    future_dates = [daily_df["date"].max() + pd.DateOffset(months=i+1) for i in range(months_ahead)]
    future_preds = model.predict(future_months)

    # Plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=daily_df["date"], y=daily_df["skill_mentioned"], label="Historical")
    sns.lineplot(x=future_dates, y=future_preds, label="Forecast", linestyle="--")
    plt.title("Skill Trend Forecast")
    plt.xlabel("Date")
    plt.ylabel("Mentions per Month")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt
