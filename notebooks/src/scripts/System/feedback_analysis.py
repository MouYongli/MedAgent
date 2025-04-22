from typing import List, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from general.data_model.question_dataset import SuperCategory, all_supercategories, all_question_classes
from general.data_model.system_interactions import WorkflowSystem


def get_average_response_time(wf_system: WorkflowSystem) -> float:
  """Average response time for a wf_system in seconds"""
  response_times = [
    latency
    for chat in wf_system.generation_results
    for entry in chat.entries
    if (latency := entry.get_response_latency()) is not None
  ]
  return sum(response_times) / len(response_times)

def analyze_and_visualize_response_time_per_category(wf_system: WorkflowSystem):
  """Assumption: only one time interaction per question
  """
  def get_latency_stats(entries):
    latencies = np.array([
      entry.get_response_latency() for entry in entries
      if entry.get_response_latency() is not None
    ])
    if len(latencies) == 0:
      return latencies, None, None, None, None
    return latencies, np.mean(latencies), np.std(latencies, ddof=1) if len(latencies) > 1 else 0.0, np.min(latencies), np.max(latencies)

  rows = [{
    "supercategory": sc.value,
    "subcategory": None,
    "response_latencies": (latencies := get_latency_stats(wf_system.get_all_questions_for_super_category(sc)))[0],
    "avg_response_latency": latencies[1],
    "std_deviation_response_latency": latencies[2],
    "min_response_latency": latencies[3],
    "max_response_latency": latencies[4],
  } for sc in all_supercategories] + [{
    "supercategory": qt.supercategory.value,
    "subcategory": qt.subcategory.value,
    "response_latencies": (latencies := get_latency_stats(wf_system.get_all_questions_for_sub_category(super_cat=qt.supercategory, sub_cat=qt.subcategory)))[0],
    "avg_response_latency": latencies[1],
    "std_deviation_response_latency": latencies[2],
    "min_response_latency": latencies[3],
    "max_response_latency": latencies[4],
  } for qt in all_question_classes]

  response_times_df = pd.DataFrame(rows)

  def visualize_box_plots_response_time_per_category():
    supercat_base_colors = {
      SuperCategory.SIMPLE.value: "#33691E",  # Green
      SuperCategory.COMPLEX.value: "#0D47A1",  # Blue
      SuperCategory.NEGATIVE.value: "#EF6C00"  # Orange
    }

    exploded_df = response_times_df[response_times_df["subcategory"].notna()].explode("response_latencies")
    exploded_df["response_latencies"] = exploded_df["response_latencies"].astype(float)

    fig = px.box(
      exploded_df,
      x="subcategory",
      y="response_latencies",
      color="supercategory",
      color_discrete_map=supercat_base_colors,
      title="Response Latency per Question Type",
      labels={
        "response_latencies": "Response Latency (s)",
        "subcategory": "Subcategory",
        "supercategory": "Supercategory",
      },
      template="seaborn"
    )

    fig.update_traces(line_width=1, marker=dict(size=3), boxmean='sd')
    fig.update_layout(
      boxmode='overlay',
      xaxis=dict(
        autorange=True,
        title=None,
        tickangle=-90,
        showgrid=False
      ),
      showlegend=True,
    )
    fig.update_yaxes(range=[0, exploded_df["response_latencies"].max() + 1])
    return fig

  return response_times_df, visualize_box_plots_response_time_per_category()

def get_average_correctness(wf_system: WorkflowSystem) -> float:
  scores = [
    score
    for chat in wf_system.generation_results
    for entry in chat.entries
    if (score := entry.get_correctness_score()) is not None
  ]
  return sum(scores) / len(scores)

def analyze_and_visualize_correctness_per_category(wf_system: WorkflowSystem):
  """Assumption: only one time interaction per question
  """
  def get_avg_correctness_score(entries):
    correctness_scores = np.array([
      entry.get_correctness_score() for entry in entries
      if entry.get_correctness_score() is not None
    ])
    if len(correctness_scores) == 0:
      return correctness_scores, None

    return correctness_scores, np.mean(correctness_scores)

  rows = [{
    "supercategory": sc.value,
    "subcategory": None,
    "correctness_scores": (correctness_scores := get_avg_correctness_score(wf_system.get_all_questions_for_super_category(sc)))[0],
    "avg_correctness_score": correctness_scores[1],
  } for sc in all_supercategories] + [{
    "supercategory": qt.supercategory.value,
    "subcategory": qt.subcategory.value,
    "correctness_scores": (correctness_scores := get_avg_correctness_score(wf_system.get_all_questions_for_sub_category(super_cat=qt.supercategory, sub_cat=qt.subcategory)))[0],
    "avg_correctness_score": correctness_scores[1],
  } for qt in all_question_classes]

  correctness_scores_df = pd.DataFrame(rows)

  def visualize_box_plots_correctness_score_per_category():
    supercat_base_colors = {
      SuperCategory.SIMPLE.value: "#33691E",  # Green
      SuperCategory.COMPLEX.value: "#0D47A1",  # Blue
      SuperCategory.NEGATIVE.value: "#EF6C00"  # Orange
    }

    exploded_df = correctness_scores_df[correctness_scores_df["subcategory"].notna()].explode("correctness_scores")
    exploded_df["correctness_scores"] = exploded_df["correctness_scores"].astype(float)

    fig = px.box(
      exploded_df,
      x="subcategory",
      y="correctness_scores",
      color="supercategory",
      color_discrete_map=supercat_base_colors,
      title="Correctness score per Question Type",
      labels={
        "correctness_scores": "Correctness Score",
        "subcategory": "Subcategory",
        "supercategory": "Supercategory",
      },
      template="seaborn"
    )

    fig.update_traces(line_width=1, marker=dict(size=3), boxmean='sd')
    fig.update_layout(
      boxmode='overlay',
      xaxis=dict(
        autorange=True,
        title=None,
        tickangle=-90,
        showgrid=False
      ),
      showlegend=True,
    )
    fig.update_yaxes(range=[0.5, 5.5])
    return fig

  return correctness_scores_df, visualize_box_plots_correctness_score_per_category()


def get_sum_hallucinations_per_question(wf_system: WorkflowSystem) -> List[float]:
  halls = [
    sum([
      hallucinations_dict["FC"],
      hallucinations_dict["IC"],
      hallucinations_dict["CC"]
    ])
    for chat in wf_system.generation_results
    for entry in chat.entries
    if (hallucinations_dict := entry.get_hallucination_classification()) is not None
  ]
  return halls

def analyze_and_visualize_hallucinations(wf_system: WorkflowSystem):
  rows = [
    {
      "wf_system": wf_system.name,
      "supercategory": qt.supercategory.value,
      "subcategory": qt.subcategory.value,
      "related_guidelines": [ea.guideline.awmf_register_number for ea in entry.question.expected_answers] if entry.question.expected_answers else [],
      "counts_fc": hallucination_dict["FC"] if (hallucination_dict := entry.get_hallucination_classification()) else None,
      "counts_ic": hallucination_dict["IC"] if hallucination_dict else None,
      "counts_cc": hallucination_dict["CC"] if hallucination_dict else None,
      "sum_hallucinations": hallucination_dict["FC"] + hallucination_dict["IC"] + hallucination_dict["CC"] if hallucination_dict else None,
    }
    for qt in all_question_classes
    for entry in wf_system.get_all_questions_for_sub_category(super_cat=qt.supercategory, sub_cat=qt.subcategory)
  ]

  hallucinations_df = pd.DataFrame(rows)

  def plot_hallucination_heatmap_for_supercategory(df, supercategory, color, z_min, z_max):
    def prepare_data():
      filtered_df = df[(df["supercategory"] == supercategory.value) & (df["subcategory"].notna())].copy()
      z = filtered_df[["counts_fc", "counts_ic", "counts_cc"]].T.to_numpy()
      x_labels = [f"Q{idx} ({subcat})" for idx, subcat in zip(filtered_df.index, filtered_df["subcategory"])]
      y_labels = ["Fact<br>conflicting", "Input<br>conflicting", "Context<br>conflicting"]
      return filtered_df, z, x_labels, y_labels

    def group_by_subcategory(df_subset):
      subcat_positions = {}
      for i, subcat in enumerate(df_subset["subcategory"]):
        subcat_positions.setdefault(subcat, []).append(i)
      return subcat_positions

    def create_shapes_and_annotations(subcat_positions, x_labels, y_range):
      shapes = []
      annotations = []
      for subcat, indices in subcat_positions.items():
        start = min(indices)
        end = max(indices)
        center = (start + end) / 2

        # Annotation
        annotations.append(dict(
          x=center,
          y=-0.07,
          text=subcat,
          showarrow=False,
          xref='x',
          yref='paper',
          xanchor='center'
        ))

        # Vertical line
        if end + 1 < len(x_labels):
          shapes.append(dict(
            type="line",
            x0=end + 0.5,
            x1=end + 0.5,
            y0=y_range[0],
            y1=y_range[1],
            line=dict(color="black", width=1),
            xref='x',
            yref='y'
          ))
      return shapes, annotations

    def create_heatmap(z, x_labels, y_labels, shapes, annotations):
      fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x_labels,
        y=y_labels,
        zmin=z_min,
        zmax=z_max,
        colorscale=[
          [0.0, 'rgba(255, 255, 255, 0.75)'],
          [1.0, color]
        ],
        colorbar=dict(
          title=dict(
            text="# Hallucinations<br>&nbsp;",
            side="top",
            font=dict(size=12)
          ),
          tickcolor='lightgray',
          tickfont=dict(size=10),
          ticks='outside',
          outlinewidth=0,
          thickness=15,
          len=1
        )
      ))

      fig.update_layout(
        title=f"Hallucinations per Question (Supercategory: {supercategory.value})",
        xaxis=dict(
          title='Subcategories with individual cell per question',
          title_standoff=40,
          tickson='boundaries',
          showgrid=True,
          gridwidth=1,
          showticklabels=False
        ),
        yaxis=dict(
          title=None,
          tickson='boundaries',
          showgrid=True,
          gridwidth=1
        ),
        template="seaborn",
        shapes=shapes,
        annotations=annotations,
      )
      return fig

    filtered_df, z, x_labels, y_labels = prepare_data()
    subcat_positions = group_by_subcategory(filtered_df)
    shapes, annotations = create_shapes_and_annotations(subcat_positions, x_labels, y_range=[-0.5, 2.5])
    return create_heatmap(z, x_labels, y_labels, shapes, annotations)

  max_count = hallucinations_df[["counts_fc", "counts_ic", "counts_cc"]].max(axis=1).max()
  simple_fig = plot_hallucination_heatmap_for_supercategory(df=hallucinations_df, supercategory=SuperCategory.SIMPLE, color='rgba(51, 105, 30, 0.75)', z_min=0, z_max=max_count)
  complex_fig = plot_hallucination_heatmap_for_supercategory(df=hallucinations_df, supercategory=SuperCategory.COMPLEX, color='rgba(13, 71, 161, 0.75)', z_min=0, z_max=max_count)
  negative_fig = plot_hallucination_heatmap_for_supercategory(df=hallucinations_df, supercategory=SuperCategory.NEGATIVE, color='rgba(239, 108, 0, 0.75)', z_min=0, z_max=max_count)

  def generate_subplot_heatmap_grid(simple_fig, complex_fig, negative_fig, title_text):
    def add_heatmaps(fig, figs):
      for i, subplot_fig in enumerate(figs, start=1):
        for trace in subplot_fig.data:
          if isinstance(trace, go.Heatmap):
            trace.colorbar = dict(
              title=trace.colorbar.title if i == 1 else "&nbsp;<br>&nbsp;",
              tickcolor='lightgray',
              tickfont=dict(size=10),
              ticks='outside',
              outlinewidth=0,
              thickness=15,
              len=1,
              x=1.01 + (i - 1) * 0.015,
              tickvals=None if i==3 else [],
            )
            fig.add_trace(trace, row=1, col=i)

    def calculate_domains(cols_per_subplot, padding_ratio):
      total_cols = sum(cols_per_subplot) + padding_ratio * 2
      domain_starts = [(sum(cols_per_subplot[:i]) + i * padding_ratio) / total_cols for i in range(3)]
      domain_ends = [(sum(cols_per_subplot[:i + 1]) + i * padding_ratio) / total_cols for i in range(3)]
      return domain_starts, domain_ends

    def add_annotations_and_shapes(fig, subplot_figs, xrefs):
      for subplot_fig, xref in zip(subplot_figs, xrefs):
        for ann in subplot_fig.layout.annotations or []:
          fig.add_annotation(
            x=ann.x,
            y=ann.y,
            text=ann.text,
            showarrow=ann.showarrow,
            xanchor=ann.xanchor,
            xref=xref,
            yref='paper'
          )
        for shape in subplot_fig.layout.shapes or []:
          shape_dict = shape.to_plotly_json()
          shape_dict["xref"] = xref
          shape_dict["yref"] = "y" if xref == "x" else f"y{xref[1:]}"
          fig.add_shape(**shape_dict)

    def add_grid_rectangles(fig, cols_per_subplot):
      for i in range(3):
        fig.add_shape(
          type="rect",
          xref=f"x{i + 1}" if i > 0 else "x",
          yref=f"y{i + 1}" if i > 0 else "y",
          x0=-1,
          x1=cols_per_subplot[i] + 1,
          y0=-0.5,
          y1=2.5,
          line=dict(color="lightgray", width=1.5),
          fillcolor="rgba(0,0,0,0)",
          layer="above",
        )

    fig = make_subplots(rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.02)
    add_heatmaps(fig, [simple_fig, complex_fig, negative_fig])

    cols_per_subplot = [len(simple_fig.data[0].x), len(complex_fig.data[0].x), len(negative_fig.data[0].x)]
    domain_starts, domain_ends = calculate_domains(cols_per_subplot, padding_ratio=2)

    fig.update_layout(
      title_text=title_text,
      title_x=0.5,
      template="seaborn",
      xaxis=dict(domain=[domain_starts[0], domain_ends[0]], tickson='boundaries', showgrid=True, showticklabels=False, range=[-0.5, cols_per_subplot[0] - 0.5]),
      xaxis2=dict(domain=[domain_starts[1], domain_ends[1]], tickson='boundaries', showgrid=True, showticklabels=False, range=[-0.5, cols_per_subplot[1] - 0.5]),
      xaxis3=dict(domain=[domain_starts[2], domain_ends[2]], tickson='boundaries', showgrid=True, showticklabels=False, range=[-0.5, cols_per_subplot[2] - 0.5]),
      yaxis=dict(tickson='boundaries', showgrid=True, gridwidth=1, showticklabels=True),
      yaxis2=dict(tickson='boundaries', showgrid=True, gridwidth=1, showticklabels=False),
      yaxis3=dict(tickson='boundaries', showgrid=True, gridwidth=1, showticklabels=False),
    )

    add_annotations_and_shapes(fig, [simple_fig, complex_fig, negative_fig], ['x', 'x2', 'x3'])

    fig.add_annotation(
      text="Subcategories (with one cell per assigned question)",
      x=0.5,
      y=-0.2,
      showarrow=False,
      font=dict(size=14),
      xref="paper",
      yref="paper"
    )

    for i, title in enumerate(["... for simple questions", "... for complex questions", "... for negative questions"]):
      center = (domain_starts[i] + domain_ends[i]) / 2
      fig.add_annotation(
        text=title,
        x=center,
        y=1.08,
        xref='paper',
        yref='paper',
        showarrow=False,
        xanchor='center',
        font=dict(size=14, color="#333")
      )

    add_grid_rectangles(fig, cols_per_subplot)

    return fig

  return hallucinations_df, generate_subplot_heatmap_grid(simple_fig, complex_fig, negative_fig, "Hallucination Types Count")


def get_average_retrieval_scores(wf_system: WorkflowSystem) -> Tuple[float, float, float]:
  scores = [
    {"precision": p, "recall": r, "f1": f}
    for chat in wf_system.generation_results
    for entry in chat.entries
    if (res := entry.get_retrieval_scores())  and (p := res[0]) is not None and (r := res[1]) is not None and (f := res[2]) is not None
  ]

  if not scores:
    return 0.0, 0.0, 0.0

  return (
    sum(score["precision"] for score in scores) / len(scores),
    sum(score["recall"] for score in scores) / len(scores),
    sum(score["f1"] for score in scores) / len(scores),
  )


def analyze_and_visualize_retrieval_scores_per_category(wf_system: WorkflowSystem):
  """Assumption: only one time interaction per question
  """
  def get_avg_retrieval_score(entries):
    retrieval_scores = np.array([
      {"precision": p, "recall": r, "f1": f}
      for entry in entries
      if (res := entry.get_retrieval_scores()) and (p := res[0]) is not None and (r := res[1]) is not None and (
        f := res[2]) is not None
    ])
    if len(retrieval_scores) == 0:
      return retrieval_scores, None, retrieval_scores, None, retrieval_scores, None,

    precision_scores = [score["precision"] for score in retrieval_scores]
    recall_scores = [score["recall"] for score in retrieval_scores]
    f1_scores = [score["f1"] for score in retrieval_scores]
    return precision_scores, np.mean(precision_scores), recall_scores, np.mean(recall_scores), f1_scores, np.mean(f1_scores)

  rows = [{
    "supercategory": sc.value,
    "subcategory": None,
    "retrieval_precision_scores": (scores := get_avg_retrieval_score(wf_system.get_all_questions_for_super_category(sc)))[0],
    "avg_retrieval_precision_score": scores[1],
    "retrieval_recall_scores": scores[2],
    "avg_retrieval_recall_score": scores[3],
    "retrieval_f1_scores": scores[4],
    "avg_retrieval_f1_score": scores[5],
  } for sc in all_supercategories] + [{
    "supercategory": qt.supercategory.value,
    "subcategory": qt.subcategory.value,
    "retrieval_precision_scores": (scores := get_avg_retrieval_score(wf_system.get_all_questions_for_sub_category(super_cat=qt.supercategory, sub_cat=qt.subcategory)))[0],
    "avg_retrieval_precision_score": scores[1],
    "retrieval_recall_scores": scores[2],
    "avg_retrieval_recall_score": scores[3],
    "retrieval_f1_scores": scores[4],
    "avg_retrieval_f1_score": scores[5],
  } for qt in all_question_classes]

  retrieval_scores_df = pd.DataFrame(rows)

  def visualize_box_plot(scores_df: pd.DataFrame, score_col: str, y_label: str, title: str):
    """Reusable visualization function for box plots."""
    exploded_df = scores_df[scores_df["subcategory"].notna()].explode(score_col)
    exploded_df[score_col] = exploded_df[score_col].astype(float)

    supercat_base_colors = {
      SuperCategory.SIMPLE.value: "#33691E",  # Green
      SuperCategory.COMPLEX.value: "#0D47A1",  # Blue
      SuperCategory.NEGATIVE.value: "#EF6C00"  # Orange
    }

    fig = px.box(
      exploded_df,
      x="subcategory",
      y=score_col,
      color="supercategory",
      color_discrete_map=supercat_base_colors,
      title=title,
      labels={"subcategory": "Subcategory", "supercategory": "Supercategory", score_col: y_label},
      template="seaborn"
    )
    fig.update_traces(line_width=1, marker=dict(size=3), boxmean='sd')
    fig.update_layout(
      boxmode="overlay",
      xaxis=dict(autorange=True, tickangle=-90, showgrid=False),
      yaxis=dict(range=[0, 1]),
      showlegend=True,
    )
    return fig

  precision_fig = visualize_box_plot(retrieval_scores_df, "retrieval_precision_scores", "Precision Scores", "Precision by Question Type")
  recall_fig = visualize_box_plot(retrieval_scores_df, "retrieval_recall_scores", "Recall Scores", "Recall by Question Type")
  f1_fig = visualize_box_plot(retrieval_scores_df, "retrieval_f1_scores", "F1 Scores", "F1 Score by Question Type")

  return retrieval_scores_df, precision_fig, recall_fig, f1_fig


def get_average_factuality(wf_system: WorkflowSystem) -> float:
  scores = [
    score
    for chat in wf_system.generation_results
    for entry in chat.entries
    if (score := entry.get_correctness_score()) is not None
  ]
  return sum(scores) / len(scores)

def analyze_and_visualize_factuality_per_category(wf_system: WorkflowSystem):
  """Assumption: only one time interaction per question
  """
  def get_avg_factuality_score(entries):
    factuality_scores = np.array([
      entry.get_factuality_score() for entry in entries
      if entry.get_factuality_score() is not None
    ])
    if len(factuality_scores) == 0:
      return factuality_scores, None

    return factuality_scores, np.mean(factuality_scores)

  rows = [{
    "supercategory": sc.value,
    "subcategory": None,
    "factuality_scores": (factuality_scores := get_avg_factuality_score(wf_system.get_all_questions_for_super_category(sc)))[0],
    "avg_factuality_score": factuality_scores[1],
  } for sc in all_supercategories] + [{
    "supercategory": qt.supercategory.value,
    "subcategory": qt.subcategory.value,
    "factuality_scores": (factuality_scores := get_avg_factuality_score(wf_system.get_all_questions_for_sub_category(super_cat=qt.supercategory, sub_cat=qt.subcategory)))[0],
    "avg_correctness_score": factuality_scores[1],
  } for qt in all_question_classes]

  factuality_scores_df = pd.DataFrame(rows)

  def visualize_box_plots_factuality_score_per_category():
    supercat_base_colors = {
      SuperCategory.SIMPLE.value: "#33691E",  # Green
      SuperCategory.COMPLEX.value: "#0D47A1",  # Blue
      SuperCategory.NEGATIVE.value: "#EF6C00"  # Orange
    }

    exploded_df = factuality_scores_df[factuality_scores_df["subcategory"].notna()].explode("factuality_scores")
    exploded_df["factuality_scores"] = exploded_df["factuality_scores"].astype(float)

    fig = px.box(
      exploded_df,
      x="subcategory",
      y="factuality_scores",
      color="supercategory",
      color_discrete_map=supercat_base_colors,
      title="Factuality score per Question Type",
      labels={
        "factuality_scores": "Factuality Score",
        "subcategory": "Subcategory",
        "supercategory": "Supercategory",
      },
      template="seaborn"
    )
    fig.update_traces(line_width=1, marker=dict(size=3), boxmean='sd')
    fig.update_layout(
      boxmode='overlay',
      xaxis=dict(
        autorange=True,
        title=None,
        tickangle=-90,
        showgrid=False
      ),
      showlegend=True,
    )
    fig.update_yaxes(range=[0, 1])
    return fig

  return factuality_scores_df, visualize_box_plots_factuality_score_per_category()

