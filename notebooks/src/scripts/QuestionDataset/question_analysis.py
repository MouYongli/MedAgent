import pandas as pd
import plotly.express as px

from general.data_model.question_dataset import SuperCategory,SubCategory
from general.helper.color import generate_color_variants


def get_total_question_count(questions_collection):
    return questions_collection.count_documents({})

def get_super_cat_question_count(questions_collection, question_types_collection, super_cat: SuperCategory):
    result = list(questions_collection.aggregate(pipeline = [
        {
            "$lookup": {
                "from": question_types_collection.name,
                "localField": "classification",
                "foreignField": "_id",
                "as": "question_type_data"
            }
        },
        { "$unwind": "$question_type_data" },
        {
            "$match": {
                "question_type_data.supercategory": super_cat.value,
            }
        },
        { "$count": "count" }
    ]))
    return result[0]["count"] if result else 0

def get_sub_cat_question_count(questions_collection, question_types_collection, super_cat: SuperCategory, sub_cat: SubCategory):
    result = list(questions_collection.aggregate(pipeline = [
        {
            "$lookup": {
                "from": question_types_collection.name,
                "localField": "classification",
                "foreignField": "_id",
                "as": "question_type_data"
            }
        },
        { "$unwind": "$question_type_data" },
        {
            "$match": {
                "question_type_data.supercategory": super_cat.value,
                "question_type_data.subcategory": sub_cat.value,
            }
        },
        { "$count": "count" }
    ]))
    return result[0]["count"] if result else 0

def get_oms_spec_guidelines(guideline_collection):
    keyword = "Mund-, Kiefer- und Gesichtschirurgie"

    oms_guidelines = list(guideline_collection.find(
        {
            "leading_publishing_organizations": {
                "$elemMatch": {"$regex": keyword, "$options": "i"}
            }
        }
    ))
    return oms_guidelines

def get_guidelines_with_answer(guideline_collection, answer_collection):
    guideline_ids = answer_collection.distinct("guideline")

    guidelines_with_answers = list(guideline_collection.find({
        "_id": { "$in": guideline_ids }
    }))
    return guidelines_with_answers

def get_answer_count_for_guideline(guideline, answer_collection):
    return answer_collection.count_documents({"guideline": guideline["_id"]})

def get_question_count_for_guideline(guideline, answer_collection, question_collection):
    expected_answers = answer_collection.distinct("_id", {"guideline": guideline["_id"]})
    if not expected_answers:
        return 0

    return question_collection.count_documents({
        "expected_answers": { "$elemMatch": { "$in": expected_answers } }
    })

def get_question_with_classification_for_guideline(guideline, answer_collection, question_collection, question_types_collection):
    """
    For each guideline, return a list of questions linked to it,
    with classification info and question ID.

    Returns:
        List of dicts with:
            - question_id
            - supercategory
            - subcategory
    """
    classification_lookup = {
        qt["_id"]: {
            "supercategory": qt.get("supercategory", "Unknown"),
            "subcategory": qt.get("subcategory", "Unknown")
        }
        for qt in question_types_collection.find({}, {"_id": 1, "supercategory": 1, "subcategory": 1})
    }
    expected_answers = answer_collection.distinct("_id", {"guideline": guideline["_id"]})
    if not expected_answers:
        return []

    question_cursor = question_collection.find({"expected_answers": {"$in": expected_answers}}, {"_id": 1, "classification": 1})

    results = []
    for question in question_cursor:
        question_id = question["_id"]
        class_id = question.get("classification")
        class_info = classification_lookup.get(class_id)
        if not class_info:
            return results
        results.append({
            "question_id": question_id,
            "supercategory": class_info["supercategory"],
            "subcategory": class_info["subcategory"]
        })

    return results

def analyze_and_visualize_question_distribution(questions_collection, question_type_collection, all_classes, supercategories):
    # count for all types
    rows = [{
        "supercategory": sc.value,
        "subcategory": None,
        "count": get_super_cat_question_count(questions_collection, question_type_collection, sc)
    } for sc in supercategories ] + [{
        "supercategory": qt.supercategory.value,
        "subcategory": qt.subcategory.value,
        "count": get_sub_cat_question_count(questions_collection, question_type_collection, qt.supercategory, qt.subcategory)
    } for qt in all_classes ]

    question_dist_df = pd.DataFrame(rows)
    question_dist_labeled = question_dist_df.copy()

    def format_label(cat, count):
        return f"{cat} <span style='color: gray; font-style: italic; font-size: 8pt'>[{count}]</span>"

    supercat_totals = question_dist_labeled[question_dist_labeled["subcategory"].isnull()].set_index("supercategory")["count"].to_dict()
    question_dist_labeled["supercategory_label"] = question_dist_labeled["supercategory"].map({
        super_cat: format_label(super_cat, count)
        for super_cat, count in supercat_totals.items()
    })
    subcat_totals = question_dist_labeled.groupby("subcategory")["count"].sum().to_dict()
    question_dist_labeled["subcategory_label"] = question_dist_labeled["subcategory"].map({
        sub_cat: format_label(sub_cat, count)
        for sub_cat, count in subcat_totals.items()
    })

    # Color mapping using labeled subcategories
    subcats_per_super = question_dist_labeled.groupby("supercategory")["subcategory_label"].unique().to_dict()
    supercat_base_colors = {
        SuperCategory.SIMPLE: "#33691E",  # Green
        SuperCategory.COMPLEX: "#0D47A1",  # Blue
        SuperCategory.NEGATIVE: "#EF6C00"  # Orange
    }
    color_map = {}
    for supercat, base in supercat_base_colors.items():
        subcats = subcats_per_super.get(supercat.value, [])
        variants = generate_color_variants(base, len(subcats))
        for subcat, color in zip(subcats, variants):
            color_map[subcat] = color

    # Plot
    fig = px.bar(
        question_dist_labeled,
        x="supercategory_label",
        y="count",
        color="subcategory_label",
        title="Question Distribution by Question Type",
        labels={
            "count": "Number of Questions",
            "subcategory_label": "Subcategory",
            "supercategory_label": "Supercategory"
        },
        color_discrete_map=color_map,
        template="seaborn"
    )

    fig.update_layout(
        barmode="stack",
        xaxis_title=None,
        showlegend=True,
        xaxis=dict(showgrid=False)
    )
    fig.update_traces(text=None, marker_line_width=0)

    return question_dist_df, fig


def analyze_and_visualize_question_per_guideline(questions_coll, question_type_coll, gl_coll, answer_coll):
    oms_spec_guidelines, with_answer_guidelines = get_oms_spec_guidelines(gl_coll), get_guidelines_with_answer(gl_coll, answer_coll)

    guideline_map = {
        doc["_id"]: {
            "_id": doc["_id"], "title": doc.get("title", ""), "awmf_register_number": doc.get("awmf_register_number"),
            "oms_spec": doc in oms_spec_guidelines,
            "answer_count": get_answer_count_for_guideline(doc, answer_coll),
            "question_count": get_question_count_for_guideline(doc, answer_coll, questions_coll),
            "questions": get_question_with_classification_for_guideline(doc, answer_coll, questions_coll, question_type_coll)
        }
        for doc in oms_spec_guidelines + with_answer_guidelines
    }

    df = pd.DataFrame(guideline_map.values())

    def visualize_question_count_per_guideline(df: pd.DataFrame, min_total_questions: int = 0):
        """
        Visualize the number of questions per guideline in a stacked bar chart using plotly.express (without melt).
        """

        def count_cat(questions, category):
            if not isinstance(questions, list):
                return 0
            return sum(1 for q in questions if isinstance(q, dict) and q.get("supercategory") == category)

        df_fig = df.copy()
        df_fig[SuperCategory.SIMPLE.value] = df_fig["questions"].apply(lambda q: count_cat(q, SuperCategory.SIMPLE.value))
        df_fig[SuperCategory.COMPLEX.value] = df_fig["questions"].apply(lambda q: count_cat(q, SuperCategory.COMPLEX.value))
        df_fig[SuperCategory.NEGATIVE.value] = df_fig["questions"].apply(lambda q: count_cat(q, SuperCategory.NEGATIVE.value))

        df_fig["awmf_register_number"] = df_fig["awmf_register_number"].fillna("Unknown")
        df_fig["awmf_label"] = df_fig.apply(
            lambda row: f"<span style='color: gray; font-style: italic;'>{row['awmf_register_number']}</span>" if not row["oms_spec"] else row["awmf_register_number"],
            axis=1
        )
        df_fig = df_fig[df_fig["question_count"] >= min_total_questions]
        df_fig = df_fig.sort_values("question_count", ascending=True)

        supercat_base_colors = {
            SuperCategory.SIMPLE.value: "#33691E",  # Green
            SuperCategory.COMPLEX.value: "#0D47A1",  # Blue
            SuperCategory.NEGATIVE.value: "#EF6C00"  # Orange
        }

        fig = px.bar(
            df_fig,
            x=[SuperCategory.SIMPLE.value, SuperCategory.COMPLEX.value, SuperCategory.NEGATIVE.value],
            y="awmf_label",
            orientation="h",
            title="Question Counts per Guideline",
            labels={
                "value": "Number of Questions",
                "awmf_label": "AWMF Register Number",
                "variable": "Question Types"
            },
            template="seaborn",
            color_discrete_map=supercat_base_colors
        )

        fig.update_layout(
            barmode="stack",
            yaxis=dict(tickformat="d", dtick=1, automargin=True, showgrid=False),
            xaxis=dict(tickformat="d", showgrid=True),
            bargap=0.4,
            margin=dict(r=175),  # Add enough space on the right
            annotations=[
                dict(
                    x=1.05,
                    y=0.5,
                    xref='paper',
                    yref='paper',
                    text=(
                        '<span style="font-size: 14px">Guideline type</span><br>'
                        '&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:black;">OMS-specific</span><br>'
                        '&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:gray; font-style: italic;">Non OMS-spec.</span>'
                    ),
                    showarrow=False,
                    align='left',
                    bgcolor='rgba(255,255,255,0.95)',
                    xanchor='left',
                    yanchor='top'
                )
            ],
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.05
            )
        )

        fig.update_traces(marker_line_width=0)

        return fig

    return df, visualize_question_count_per_guideline(df)
