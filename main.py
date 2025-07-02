from agent import run_agent
import json

if __name__ == "__main__":
    input_data = {
        "today_sales": 1000,
        "today_cost": 800,
        "today_customers": 50,
        "yesterday_sales": 900,
        "yesterday_cost": 700,
        "yesterday_customers": 500
    }

    result = run_agent(input_data)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))