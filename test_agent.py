import pytest
from agent import input_node, processing_node, recommendation_node, run_agent

valid_input = {
    "today_sales": 1000,
    "today_cost": 800,
    "today_customers": 50,
    "yesterday_sales": 900,
    "yesterday_cost": 700,
    "yesterday_customers": 50
}

invalid_input_missing_keys = {
    "today_sales": 1000,
    "today_cost": 800
}

invalid_input_negative = {
    "today_sales": 1000,
    "today_cost": -800,
    "today_customers": 50,
    "yesterday_sales": 900,
    "yesterday_cost": 700,
    "yesterday_customers": 50
}

zero_input = {
    "today_sales": 0,
    "today_cost": 0,
    "today_customers": 0,
    "yesterday_sales": 0,
    "yesterday_cost": 0,
    "yesterday_customers": 0
}

def test_input_node_valid():
    state = {"input_data": valid_input, "messages": [], "metrics": {}, "recommendations": []}
    result = input_node(state)
    assert result["error"] is None
    assert result["input_data"] == valid_input
    assert "Input data received" in result["messages"]
    assert result["metrics"] == {}
    assert result["recommendations"] == []

def test_input_node_missing_keys():
    state = {"input_data": invalid_input_missing_keys, "messages": [], "metrics": {}, "recommendations": []}
    result = input_node(state)
    assert result["error"] == "Missing required input data: ['today_customers', 'yesterday_sales', 'yesterday_cost', 'yesterday_customers']"
    assert "Error: Missing required input data" in result["messages"]
    assert result["metrics"] == {}
    assert result["recommendations"] == []

def test_input_node_negative_value():
    state = {"input_data": invalid_input_negative, "messages": [], "metrics": {}, "recommendations": []}
    result = input_node(state)
    assert result["error"] == "Invalid value for today_cost: must be a non-negative number"
    assert "Error: Invalid value for today_cost" in result["messages"]
    assert result["metrics"] == {}
    assert result["recommendations"] == []

def test_input_node_invalid_type():
    state = {"input_data": "not a dict", "messages": [], "metrics": {}, "recommendations": []}
    result = input_node(state)
    assert result["error"] == "Input data must be a dictionary"
    assert "Error: Input data must be a dictionary" in result["messages"]
    assert result["metrics"] == {}
    assert result["recommendations"] == []

def test_processing_node_valid():
    state = {
        "input_data": valid_input,
        "messages": ["Enter your input data"],
        "metrics": {},
        "recommendations": [],
        "error": None
    }
    result = processing_node(state)
    assert result["error"] is None
    assert result["metrics"]["profit"] == 200
    assert result["metrics"]["sales_change"] == pytest.approx(11.111111, 0.01)
    assert result["metrics"]["cost_change"] == pytest.approx(14.285714, 0.01)
    assert result["metrics"]["today_cac"] == 16.0
    assert result["metrics"]["cac_change"] == pytest.approx(14.285714, 0.01)
    assert "Metrics calculated" in result["messages"]
    assert result["recommendations"] == []

def test_processing_node_with_error():
    state = {
        "input_data": valid_input,
        "messages": ["Enter your input data"],
        "metrics": {},
        "recommendations": [],
        "error": "Previous error"
    }
    result = processing_node(state)
    assert result["error"] == "Previous error"
    assert result["metrics"] == {}
    assert result["recommendations"] == []
    assert "Metrics calculated" not in result["messages"]

def test_processing_node_zero_values():
    state = {
        "input_data": zero_input,
        "messages": ["Enter your input data"],
        "metrics": {},
        "recommendations": [],
        "error": None
    }
    result = processing_node(state)
    assert result["error"] is None
    assert result["metrics"]["profit"] == 0
    assert result["metrics"]["sales_change"] == 0
    assert result["metrics"]["cost_change"] == 0
    assert result["metrics"]["today_cac"] == 0
    assert result["metrics"]["cac_change"] == 0
    assert "Metrics calculated" in result["messages"]
    assert result["recommendations"] == []

def test_recommendation_node_valid():
    state = {
        "input_data": valid_input,
        "metrics": {
            "profit": -200,
            "sales_change": -15.0,
            "cac_change": 25.0
        },
        "messages": ["Metrics calculated"],
        "recommendations": [],
        "error": None
    }
    result = recommendation_node(state)
    assert result["error"] is None
    assert "Reduce costs as profit is negative." in result["recommendations"]
    assert "Review sales strategies as sales have declined significantly." in result["recommendations"]
    assert "Review marketing campaigns as CAC has increased significantly." in result["recommendations"]
    assert "Recommendations generated" in result["messages"]

def test_recommendation_node_with_error():
    state = {
        "input_data": valid_input,
        "metrics": {},
        "messages": ["Metrics calculated"],
        "recommendations": [],
        "error": "Previous error"
    }
    result = recommendation_node(state)
    assert result["error"] == "Previous error"
    assert result["recommendations"] == []
    assert result["metrics"] == {}
    assert "Recommendations generated" not in result["messages"]

def test_recommendation_node_empty_metrics():
    state = {
        "input_data": valid_input,
        "metrics": {},
        "messages": ["Metrics calculated"],
        "recommendations": [],
        "error": None
    }
    result = recommendation_node(state)
    assert result["error"] == "No metrics available for recommendations"
    assert result["recommendations"] == []
    assert result["metrics"] == {}
    assert "Error: No metrics available for recommendations" in result["messages"]

def test_run_agent_valid():
    result = run_agent(valid_input)
    assert result["error"] is None
    assert result["profit_status"] == "Profit"
    assert result["metrics"]["profit"] == 200
    assert len(result["recommendations"]) > 0
    assert "Maintain or optimize current cost structure." in result["recommendations"]

def test_run_agent_invalid_input():
    result = run_agent(invalid_input_missing_keys)
    assert result["error"] == "Missing required input data: ['today_customers', 'yesterday_sales', 'yesterday_cost', 'yesterday_customers']"
    assert result["profit_status"] == "Error"
    assert result["metrics"] == {}
    assert result["recommendations"] == []

def test_run_agent_non_dict_input():
    result = run_agent("not a dict")
    assert result["error"] == "Input data must be a dictionary"
    assert result["profit_status"] == "Error"
    assert result["metrics"] == {}
    assert result["recommendations"] == []