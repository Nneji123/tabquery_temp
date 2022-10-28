import sys
import pytest

sys.path.append("..")

from .test_inference import *

question_csv = "what is the average salary?"
question_excel = "what is the pregnancy of someone with blood pressure of 72"

@pytest.mark.filterwarnings('ignore')
def test_execute_query_csv():
    assert (
        str(execute_query_csv(question_csv, "salaries.csv"))
        == "{'query': 'what is the average salary?', 'result': ['80000', 'AVERAGE']}"
    )


# def test_execute_query_excel():
#     assert (
#         str(execute_query_excel(question_excel, "diabetes.xlsx"))
#         == "{'query': 'what is the pregnancy of someone with blood pressure of 72', 'result': [['5','4']]}"
