import datetime
import os
import warnings

import camelot
import pandas as pd
from transformers import TapasTokenizer, TFTapasForQuestionAnswering

warnings.filterwarnings("ignore")


# MODELS
MICROSOFT_LARGE_MODEL = "microsoft/tapex-large"
MICROSOFT_BASE_MODEL = "microsoft/tapex-base"


OMNITAB_FINETUNED_MODEL = "neulab/omnitab-large-finetuned-wtq"

GOOGLE_LARGE_MODEL = "google/tapas-large-finetuned-wtq"
GOOGLE_BASE_MODEL = "google/tapas-base-finetuned-wtq"
GOOGLE_MEDIUM_MODEL = "google/tapas-medium-finetuned-wtq"
GOOGLE_SMALL_MODEL = "google/tapas-small-finetuned-wtq"


model_names = [""]


def tensorflow_shutup(normal: bool = True):
    """
    The tensorflow_shutup function makes Tensorflow less verbose.
    It does this by setting the TF_CPP_MIN_LOG_LEVEL environment variable to 1, which
    tells TensorFlow to log only error messages. This is important because some of the 
    TensorFlow functions are very long and contain a lot of output that we don't always need.

    Args:
        normal:bool=True: Make the function callable with or without a parameter

    Returns:
        None
    """
    try:
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"
        import logging

        logging.getLogger("tensorflow").setLevel(logging.WARNING)

        # noinspection PyPackageRequirements
        import tensorflow as tf
        from tensorflow.python.util import deprecation

        # Place this before directly or indirectly importing tensorflow

        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

        # Monkey patching deprecation utils to shut it up! Maybe good idea to disable this once after upgrade
        # noinspection PyUnusedLocal
        def deprecated(
            date, instructions, warn_once=True
        ):  # pylint: disable=unused-argument
            def deprecated_wrapper(func):
                return func

            return deprecated_wrapper

        deprecation.deprecated = deprecated

    except ImportError:
        pass


def execute_query_csv(query: str, csv_file):
    """
    The execute_query_csv function takes a query and a csv file as input. It returns the result of the query in json format.
    
    Args:
        query:str: Pass the query that is to be answered
        csv_file: Specify the path to a csv file that contains the table
    
    Returns:
        A dictionary with two keys: query and result
    """
    a = datetime.datetime.now()

    table = pd.read_csv(csv_file, delimiter=",", nrows=64, skip_blank_lines=True)
    table.fillna(0, inplace=True)
    table = table.astype(str)

    model_name = GOOGLE_BASE_MODEL
    model = TFTapasForQuestionAnswering.from_pretrained(model_name)
    tokenizer = TapasTokenizer.from_pretrained(model_name)

    queries = [query]

    inputs = tokenizer(
        table=table, queries=queries, padding="max_length", return_tensors="tf"
    )
    outputs = model(**inputs)

    (
        predicted_answer_coordinates,
        predicted_aggregation_indices,
    ) = tokenizer.convert_logits_to_predictions(
        inputs, outputs.logits, outputs.logits_aggregation
    )

    # let's print out the results:
    id2aggregation = {0: "NONE", 1: "SUM", 2: "AVERAGE", 3: "COUNT"}
    aggregation_predictions_string = [
        id2aggregation[x] for x in predicted_aggregation_indices
    ]

    answers = []
    for coordinates in predicted_answer_coordinates:
        if len(coordinates) == 1:
            # only a single cell:
            answers.append(table.iat[coordinates[0]])
        else:
            # multiple cells
            cell_values = []
            for coordinate in coordinates:
                cell_values.append(table.iat[coordinate])
            answers.append(cell_values)

    for query, answer, predicted_agg in zip(
        queries, answers, aggregation_predictions_string
    ):
        if predicted_agg != "NONE":
            answers.append(predicted_agg)

    query_result = {"query": query, "result": answers}

    b = datetime.datetime.now()
    print(b - a)

    return query_result


def execute_query_excel(query: str, excel_file):
    """
    The execute_query_excel function takes in a query and an excel file as input. It then parses the excel file into
    a pandas dataframe, fills all null values with 0, converts all columns to strings, and returns a list of answers to the 
    query.
    
    Args:
        query:str: Pass the query that should be answered
        excel_file: Specify the path to the excel file
    
    Returns:
        A dictionary with two keys: query and result
    """
    a = datetime.datetime.now()

    table = pd.read_excel(excel_file, nrows=64)
    table.fillna(0, inplace=True)
    table = table.astype(str)

    model_name = "google/tapas-base-finetuned-wtq"
    model = TFTapasForQuestionAnswering.from_pretrained(model_name)
    tokenizer = TapasTokenizer.from_pretrained(model_name)

    queries = [query]

    inputs = tokenizer(
        table=table, queries=queries, padding="max_length", return_tensors="tf"
    )
    outputs = model(**inputs)

    (
        predicted_answer_coordinates,
        predicted_aggregation_indices,
    ) = tokenizer.convert_logits_to_predictions(
        inputs, outputs.logits, outputs.logits_aggregation
    )

    # let's print out the results:
    id2aggregation = {0: "NONE", 1: "SUM", 2: "AVERAGE", 3: "COUNT"}
    aggregation_predictions_string = [
        id2aggregation[x] for x in predicted_aggregation_indices
    ]

    answers = []
    for coordinates in predicted_answer_coordinates:
        if len(coordinates) == 1:
            # only a single cell:
            answers.append(table.iat[coordinates[0]])
        else:
            # multiple cells
            cell_values = []
            for coordinate in coordinates:
                cell_values.append(table.iat[coordinate])
            answers.append(cell_values)

    for query, answer, predicted_agg in zip(
        queries, answers, aggregation_predictions_string
    ):
        if predicted_agg != "NONE":
            answers.append(predicted_agg)

    query_result = {"query": query, "result": answers}

    b = datetime.datetime.now()
    print(b - a)

    return query_result


def execute_query_parquet(query: str, parquet_file):
    a = datetime.datetime.now()

    table = pd.read_parquet(
        parquet_file, delimiter=",", nrows=64, skip_blank_lines=True
    )
    table.fillna(0, inplace=True)
    table = table.astype(str)

    # model_name = "google/tapas-base-finetuned-wtq"
    model = TFTapasForQuestionAnswering.from_pretrained(model_name)
    tokenizer = TapasTokenizer.from_pretrained(model_name)

    queries = [query]

    inputs = tokenizer(
        table=table, queries=queries, padding="max_length", return_tensors="tf"
    )
    outputs = model(**inputs)

    (
        predicted_answer_coordinates,
        predicted_aggregation_indices,
    ) = tokenizer.convert_logits_to_predictions(
        inputs, outputs.logits, outputs.logits_aggregation
    )

    # let's print out the results:
    id2aggregation = {0: "NONE", 1: "SUM", 2: "AVERAGE", 3: "COUNT"}
    aggregation_predictions_string = [
        id2aggregation[x] for x in predicted_aggregation_indices
    ]

    answers = []
    for coordinates in predicted_answer_coordinates:
        if len(coordinates) == 1:
            # only a single cell:
            answers.append(table.iat[coordinates[0]])
        else:
            # multiple cells
            cell_values = []
            for coordinate in coordinates:
                cell_values.append(table.iat[coordinate])
            answers.append(cell_values)

    for query, answer, predicted_agg in zip(
        queries, answers, aggregation_predictions_string
    ):
        if predicted_agg != "NONE":
            answers.append(predicted_agg)

    query_result = {"query": query, "result": answers}

    b = datetime.datetime.now()
    print(b - a)

    return query_result


# def convert_pdf_to_csv(question: str, files: str = "data/filename.pdf"):
#     files = "data/filename.pdf"
#     tables = camelot.read_pdf(files)
#     dataframe = tables[0].df
#     dataframe.to_csv("data/file.csv", index=False, header=False)
#     answer = execute_query_csv(question, "data/file.csv")
#     return answer


tensorflow_shutup()
# print(convert_pdf_to_csv("what is the improved speed of distance=1.3?", "fo.pdf"))
