from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class State(TypedDict):
    input_data: dict
    metrics: dict
    recommendations: list
    messages: Annotated[list, add_messages]
    error: str  

def input_node(state: State) -> State:
    """Receives and validates input data."""
    try:
        input_data = state.get("input_data", {})
        required_keys = [
            "today_sales", "today_cost", "today_customers",
            "yesterday_sales", "yesterday_cost", "yesterday_customers"
        ]
        
        if not isinstance(input_data, dict):
            raise ValueError("Input data must be a dictionary")
        
        if not all(key in input_data for key in required_keys):
            missing_keys = [key for key in required_keys if key not in input_data]
            raise ValueError(f"Missing required input data: {missing_keys}")
        
        for key in required_keys:
            if not isinstance(input_data[key], (int, float)) or input_data[key] < 0:
                raise ValueError(f"Invalid value for {key}: must be a non-negative number")
        
        return {
            "input_data": input_data,
            "metrics": state.get("metrics", {}),
            "recommendations": state.get("recommendations", []),
            "messages": ["Input data received"],
            "error": None
        }
    
    except ValueError as e:
        logger.error(f"Error in input_node: {str(e)}")
        return {
            "input_data": input_data,
            "metrics": state.get("metrics", {}),
            "recommendations": state.get("recommendations", []),
            "messages": state["messages"] + [f"Error: {str(e).split(':')[0]}"],
            "error": str(e)
        }
    
    except Exception as e:
        logger.error(f"Unexpected error in input_node: {str(e)}")
        return {
            "input_data": input_data,
            "metrics": state.get("metrics", {}),
            "recommendations": state.get("recommendations", []),
            "messages": state["messages"] + [f"Unexpected error: {str(e)}"],
            "error": str(e)
        }

def processing_node(state: State) -> State:
    """Calculates key metrics from input data."""
    try:
        if state.get("error"):
            logger.warning("Skipping processing_node due to previous error")
            return {
                "input_data": state.get("input_data", {}),
                "metrics": state.get("metrics", {}),
                "recommendations": state.get("recommendations", []),
                "messages": state["messages"],
                "error": state["error"]
            }
        
        data = state["input_data"]
        today_sales = data["today_sales"]
        today_cost = data["today_cost"]
        today_customers = data["today_customers"]
        yesterday_sales = data["yesterday_sales"]
        yesterday_cost = data["yesterday_cost"]
        yesterday_customers = data["yesterday_customers"]

        profit = today_sales - today_cost
        sales_change = ((today_sales - yesterday_sales) / yesterday_sales * 100) if yesterday_sales != 0 else 0
        cost_change = ((today_cost - yesterday_cost) / yesterday_cost * 100) if yesterday_cost != 0 else 0
        today_cac = today_cost / today_customers if today_customers != 0 else 0
        yesterday_cac = yesterday_cost / yesterday_customers if yesterday_customers != 0 else 0
        cac_change = ((today_cac - yesterday_cac) / yesterday_cac * 100) if yesterday_cac != 0 else 0

        metrics = {
            "profit": profit,
            "sales_change": sales_change,
            "cost_change": cost_change,
            "today_cac": today_cac,
            "cac_change": cac_change
        }
        
        return {
            "input_data": state.get("input_data", {}),
            "metrics": metrics,
            "recommendations": state.get("recommendations", []),
            "messages": state["messages"] + ["Metrics calculated"],
            "error": None
        }
    
    except KeyError as e:
        logger.error(f"Key error in processing_node: {str(e)}")
        return {
            "input_data": state.get("input_data", {}),
            "metrics": state.get("metrics", {}),
            "recommendations": state.get("recommendations", []),
            "messages": state["messages"] + [f"Error: Missing key {str(e)}"],
            "error": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error in processing_node: {str(e)}")
        return {
            "input_data": state.get("input_data", {}),
            "metrics": state.get("metrics", {}),
            "recommendations": state.get("recommendations", []),
            "messages": state["messages"] + [f"Unexpected error: {str(e)}"],
            "error": str(e)
        }

def recommendation_node(state: State) -> State:
    """Generates actionable recommendations based on metrics."""
    try:
        if state.get("error"):
            logger.warning("Skipping recommendation_node due to previous error")
            return {
                "input_data": state.get("input_data", {}),
                "metrics": state.get("metrics", {}),
                "recommendations": state.get("recommendations", []),
                "messages": state["messages"],
                "error": state["error"]
            }
        
        metrics = state.get("metrics", {})
        recommendations = []

        if not metrics:
            raise ValueError("No metrics available for recommendations")

        if metrics.get("profit", 0) < 0:
            recommendations.append("Reduce costs as profit is negative.")
        else:
            recommendations.append("Maintain or optimize current cost structure.")

        if metrics.get("sales_change", 0) > 10:
            recommendations.append("Consider increasing advertising budget due to sales growth.")
        elif metrics.get("sales_change", 0) < -10:
            recommendations.append("Review sales strategies as sales have declined significantly.")

        if metrics.get("cac_change", 0) > 20:
            recommendations.append("Review marketing campaigns as CAC has increased significantly.")

        return {
            "input_data": state.get("input_data", {}),
            "metrics": state.get("metrics", {}),
            "recommendations": recommendations,
            "messages": state["messages"] + ["Recommendations generated"],
            "error": None
        }
    
    except ValueError as e:
        logger.error(f"Error in recommendation_node: {str(e)}")
        return {
            "input_data": state.get("input_data", {}),
            "metrics": state.get("metrics", {}),
            "recommendations": state.get("recommendations", []),
            "messages": state["messages"] + [f"Error: {str(e)}"],
            "error": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error in recommendation_node: {str(e)}")
        return {
            "input_data": state.get("input_data", {}),
            "metrics": state.get("metrics", {}),
            "recommendations": state.get("recommendations", []),
            "messages": state["messages"] + [f"Unexpected error: {str(e)}"],
            "error": str(e)
        }

def build_graph():
    workflow = StateGraph(State)
    workflow.add_node("input", input_node)
    workflow.add_node("processing", processing_node)
    workflow.add_node("recommendation", recommendation_node)

    workflow.add_edge("input", "processing")
    workflow.add_edge("processing", "recommendation")
    workflow.add_edge("recommendation", END)

    workflow.set_entry_point("input")

    return workflow.compile()

graph = build_graph()

def run_agent(input_data: dict) -> dict:
    """Runs the agent with input data."""
    try:
        if not isinstance(input_data, dict):
            raise ValueError("Input data must be a dictionary")
        
        initial_state = {
            "input_data": input_data,
            "metrics": {},
            "recommendations": [],
            "messages": [],
            "error": None
        }
        final_state = graph.invoke(initial_state)

        if final_state.get("error"):
            return {
                "profit_status": "Error",
                "alerts": [],
                "recommendations": final_state["recommendations"],
                "metrics": final_state["metrics"],
                "error": final_state["error"]
            }

        return {
            "profit_status": "Profit" if final_state["metrics"].get("profit", 0) >= 0 else "Loss",
            "alerts": [r for r in final_state["recommendations"] if "Review" in r],
            "recommendations": final_state["recommendations"],
            "metrics": final_state["metrics"],
            "error": None
        }
    
    except Exception as e:
        logger.error(f"Error in run_agent: {str(e)}")
        return {
            "profit_status": "Error",
            "alerts": [],
            "recommendations": [],
            "metrics": {},
            "error": str(e)
        }