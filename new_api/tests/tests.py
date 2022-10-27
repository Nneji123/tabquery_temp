from test_utils import *

question = "what is the average salary?"

def test_execute_query_csv():
    assert str(execute_query_csv(question, "salaries.csv")) == "{'query': 'what is the average salary?', 'result': ['80000', 'AVERAGE']}"
    
def test_execute_query_excel():
    pass