"""langgraph config for langgraph studio"""


from agent import build_agent

graphs = {
    "business_agent": build_agent()
}
