import math

import numpy as np
import plotly.express as px
import pandas as pd

from general.helper.logging import logger

def get_number_of_documents(collection):
    return collection.count_documents({})

def get_number_of_outdated_documents(collection):
    return collection.count_documents({
        "$and": [
            {"validity_information.valid": False},
            {"validity_information.extended_validity": False}
        ]
    })

def get_total_page_count(collection):
    page_counts = []
    for doc in collection.find({}, {"download_information.page_count": 1, "_id": 0}):
        page_count = doc.get("download_information", {}).get("page_count")
        if page_count is not None:
            page_counts.append(page_count)
        else:
            logger.error(f"Could not extract page count for {doc['_id']}")

    return sum(page_counts)

def get_average_publication_interval_in_days(collection):
    """
    Calculate the average interval (in months) between publication dates
    from validity_information.guidelines_creation_date in the collection.
    """
    dates = []
    for doc in collection.find({}, {"validity_information.guidelines_creation_date": 1, "_id": 0}):
        date_value = doc.get("validity_information", {}).get("guidelines_creation_date")
        if date_value is not None:
            dates.append(date_value)
        else:
            logger.error(f"Missing publication date for document: {doc}")

    if not dates:
        logger.error("No publication dates found in the collection.")
        return None

    # Convert dates to a DataFrame and sort them
    df = pd.DataFrame(dates, columns=["publication_date"])
    df["publication_date"] = pd.to_datetime(df["publication_date"])
    df = df.sort_values("publication_date")

    # Compute the differences in days between consecutive dates
    df["diff"] = df["publication_date"].diff().dt.days
    avg_days = df["diff"].dropna().mean()

    return avg_days

def get_number_of_oms_specific_guidelines(collection):
    """
       Count the number of guidelines that are OMS-specific.
       A guideline is considered OMS-specific if any of the leading publishing organizations
       contains the phrase 'Mund-, Kiefer- und Gesichtschirurgie'.
       """
    keyword = "Mund-, Kiefer- und Gesichtschirurgie"
    count = collection.count_documents({
        "leading_publishing_organizations": {
            "$elemMatch": {"$regex": keyword, "$options": "i"}  # Case-insensitive match
        }
    })
    return count

def visualize_page_count(collection, bin_size=25):
    page_counts = []
    for doc in collection.find({}, {"download_information.page_count": 1, "_id": 0}):
        page_count = doc.get("download_information", {}).get("page_count")
        if page_count is not None:
            page_counts.append(page_count)
        else:
            logger.error(f"Could not extract page count for {doc['_id']}")

    df = pd.DataFrame(page_counts, columns=["page_count"])
    max_page = df["page_count"].max()
    bins = list(range(0, int(max_page + bin_size), bin_size))
    # Define labels like "0-10", "10-20", etc.
    # labels = [f"{b}-{b + bin_size}" for b in bins[:-1]]
    labels = [f"{b + bin_size}" for b in bins[:-1]]

    # Group page counts into these bins
    df["page_count_range"] = pd.cut(
        df["page_count"],
        bins=bins,
        labels=labels,
        right=False,  # Ensures left-inclusive bins
        include_lowest=True
    )

    # Group by the new bin and count guidelines per bin
    grouped = df.groupby("page_count_range", observed=False).size().reset_index(name="guideline_count")

    # For proper ordering, extract the left bound of each bin and sort by it.
    grouped["bin_start"] = grouped["page_count_range"].apply(lambda x: int(x.split('-')[0]))
    grouped["bin_pos"] = grouped["bin_start"].astype(int) + (bin_size / 2)
    grouped = grouped.sort_values(by="bin_start")

    # Create a horizontal bar chart.
    fig = px.bar(
        grouped,
        x="guideline_count",
        y="bin_pos",
        orientation="h",
        labels={
            "guideline_count": "Number of Guidelines",
            "bin_pos": f"Number of Pages <span style='color: gray; font-style: italic; font-size: 8pt'> Bin size: {bin_size}</span>"
        },
        template="seaborn",
        title=f"Distribution of Page Counts Across Guidelines"
    )

    # Reverse the y-axis so that the smallest range is at the top
    y_min = 0
    y_max = int(grouped["bin_start"].max()) + 2*bin_size
    fig.update_yaxes(range=[y_max, y_min], showgrid=True)

    # Compute dynamic tick spacing for the x-axis (guideline count)
    x_min = 0
    x_max = grouped["guideline_count"].max()
    x_range = x_max - x_min
    dtick_x = max(1, math.ceil(x_range / 10))
    fig.update_xaxes(tickmode='linear', dtick=dtick_x, tickformat="d", showgrid=True)

    return fig

def visualize_publication_dates(collection):
    """Analyse publication dates using validity_information.guidelines_creation_date."""
    dates = []
    for doc in collection.find({}, {
        "validity_information.guidelines_creation_date": 1,
        "validity_information.valid": 1,
        "validity_information.extended_validity": 1,
        "_id": 0
    }):
        date_value = doc.get("validity_information", {}).get("guidelines_creation_date")
        valid = doc.get("validity_information", {}).get("valid", False)
        extended_validity = doc.get("validity_information", {}).get("extended_validity", False)
        if date_value is not None:
            dates.append({
                "guidelines_creation_date": date_value,
                "valid": valid,
                "extended_validity": extended_validity
            })
        else:
            logger.error(f"Missing publication date for document: {doc}")

    if not dates:
        logger.error("No publication dates found.")
        return None

    df = pd.DataFrame(dates)
    df["guidelines_creation_date"] = pd.to_datetime(df["guidelines_creation_date"])
    # logger.note("Grouped guidelines by publication date.")

    grouped = df.groupby(["guidelines_creation_date"]).size().reset_index(name="count")

    fig_scatter = px.scatter(
        grouped,
        x="guidelines_creation_date",
        y="count",
        labels={
            "guidelines_creation_date": "Publication Date",
            "count": "Number of Publications",
        },
        template="seaborn",
        title="Guidelines Publication Over Time"
    )
    fig_scatter.update_traces(mode="lines+markers", fill="tozeroy", fillcolor="rgba(0, 0, 255, 0.2)", line=dict(color='rgba(0, 0, 255, 0.1)'))
    fig_scatter.update_yaxes(rangemode="tozero", tickmode="linear", dtick="1")

    df["status"] = df.apply(
        lambda row: "expanded valid" if row["extended_validity"] else
                    ("outdated" if not row["valid"] else "valid"),
        axis=1
    )
    df["quarter"] = df["guidelines_creation_date"].dt.to_period("Q").astype(str)  # Converts to YYYY-QX
    df["year"] = df["guidelines_creation_date"].dt.year.astype(str)

    grouped_bar = df.groupby(["quarter", "status"]).size().unstack(fill_value=0).reset_index()

    min_date = (df["guidelines_creation_date"].min().to_period("Q") - 1)
    max_date = (df["guidelines_creation_date"].max().to_period("Q") + 1)
    all_quarters = pd.period_range(start=min_date, end=max_date, freq="Q").astype(str)
    full_quarters_df = pd.DataFrame({"quarter": all_quarters})
    grouped_bar = full_quarters_df.merge(grouped_bar, on="quarter", how="left").fillna(0)

    grouped_bar[["valid", "expanded valid", "outdated"]] = grouped_bar[["valid", "expanded valid", "outdated"]].astype(int)

    first_quarters = grouped_bar[grouped_bar["quarter"].str.endswith("Q1")]["quarter"].tolist()

    fig_bar = px.bar(
        grouped_bar,
        x="quarter",
        y=["outdated", "expanded valid", "valid"],
        labels={
            "quarter": "Publication Date <span style='color: gray; font-style: italic; font-size: 8pt'> Binned by quarter (Q1, Q2, Q3, Q4)</span>",
            "value": "Number of Guidelines",
            "variable": "Validity Status"
        },
        title="Guidelines Status Over Time",
        color_discrete_map={
            "valid": "#636efa",
            "expanded valid": "#63a1fa",
            "outdated": "#e59952"
        },
        template="seaborn"
    )

    grouped_bar["quarter_numeric"] = np.arange(len(grouped_bar))  # Assigns a sequential index to each quarter

    first_quarter_positions = grouped_bar[grouped_bar["quarter"].isin(first_quarters)]["quarter_numeric"]

    fig_bar.update_layout(
        barmode="stack",
        bargroupgap=0,
        bargap=0.4,

        yaxis=dict(
            tickmode="linear",
            dtick=1,  # Ensure only integer ticks
            range=[0.01, grouped_bar[["valid", "expanded valid", "outdated"]].sum(axis=1).values.max() + 0.5],
        ),

        xaxis=dict(
            tickmode="array",
            tickvals=first_quarter_positions - 0.5,
            ticktext=[q[:4] for q in first_quarters],  # Display only year (YYYY)
            showgrid=True,
        ),

        legend=dict(
            x=0.025,  # Adjust horizontal position (0 = left, 1 = right)
            y=0.975,  # Adjust vertical position (0 = bottom, 1 = top)
            bgcolor="rgba(255,255,255,0.7)",
        )
    )

    fig_bar.update_traces(x=grouped_bar["quarter_numeric"])

    return fig_scatter, fig_bar

