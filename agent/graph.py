# from dotenv import load_dotenv
# import os
# from pathlib import Path
#
# from langchain_core.globals import set_verbose, set_debug
# from langchain_groq.chat_models import ChatGroq
# from langgraph.constants import END
# from langgraph.graph import StateGraph
# # ✅ NEW - correct import
# from langgraph.prebuilt import create_react_agent
# from langchain_google_genai import ChatGoogleGenerativeAI
#
# # Build explicit path to .env relative to this file
# env_path = Path(__file__).parent.parent / ".env"
#
#
# load_dotenv(dotenv_path=env_path, override=True)
#
#
#
# api_key = os.getenv("GROQ_API_KEY")
# print("Loaded Key:", api_key)
#
# from agent.prompts import *
# from agent.states import *
# from agent.tools import write_file, read_file, get_current_directory, list_file
#
# #
# set_debug(True)
# set_verbose(True)
#
#
# #llm = ChatGroq(model="openai/gpt-oss-120b")
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-lite",
#     google_api_key=os.getenv("GEMINI_API_KEY"),
#     temperature=0
# )
#
#
# def planner_agent(state:dict) -> dict:
#     """Converts user prompt into a structured Plan."""
#     user_prompt = state["user_prompt"]
#     resp = llm.with_structured_output(Plan).invoke(
#         planner_prompt(user_prompt)
#     )
#
#     print(resp)
#     if resp is None:
#         raise ValueError("Planner did not return a valid response.")
#     return {"plan": resp}
#
#
# def architect_agent(state: dict) -> dict:
#     """Creates TaskPlan from Plan."""
#     plan: Plan = state["plan"]
#     resp = llm.with_structured_output(TaskPlan).invoke(
#         architect_prompt(plan=plan.model_dump_json())
#     )
#     if resp is None:
#         raise ValueError("Planner did not return a valid response.")
#
#     resp.plan = plan
#     # print(resp.model_dump_json())
#     return {"task_plan": resp}
# #
# #
# def coder_agent(state: dict) -> dict:
#     """LangGraph tool-using coder agent."""
#     coder_state: CoderState = state.get("coder_state")
#     if coder_state is None:
#         coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)
#
#     steps = coder_state.task_plan.implementation_steps
#     if coder_state.current_step_idx >= len(steps):
#         return {"coder_state": coder_state, "status": "DONE"}
#
#     current_task = steps[coder_state.current_step_idx]
#     existing_content = read_file.run(current_task.filepath)
#
#     system_prompt = coder_system_prompt()
#     user_prompt = (
#         f"Task: {current_task.task_description}\n"
#         f"File: {current_task.filepath}\n"
#         f"Existing content:\n{existing_content}\n"
#         "Use write_file(path, content) to save your changes."
#     )
# #
# #     coder_tools = [read_file, write_file, list_file, get_current_directory]
# #     react_agent = create_react_agent(llm, coder_tools)
# #
# #     react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
# #                                      {"role": "user", "content": user_prompt}]})
# #
# #     coder_state.current_step_idx += 1
# #     return {"coder_state": coder_state}
#
#
# graph = StateGraph(dict)
#
# graph.add_node("planner", planner_agent)
# graph.add_node("architect", architect_agent)
# graph.add_node("coder", coder_agent)
# #
# graph.add_edge("planner", "architect")
# # graph.add_edge("architect", "coder")
# # graph.add_conditional_edges(
# #     "coder",
# #     lambda s: "END" if s.get("status") == "DONE" else "coder",
# #     {"END": END, "coder": "coder"}
# # )
# #
# graph.set_entry_point("planner")
# agent = graph.compile()
# if __name__ == "__main__":
#     result = agent.invoke({"user_prompt": "Build a simple calculator in html css and js"},
#                           {"recursion_limit": 100})
#     # print("Final State:", result)


#new code

from dotenv import load_dotenv
from langchain_core.globals import set_verbose, set_debug
from langchain_groq.chat_models import ChatGroq
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent

from agent.prompts import *
from agent.states import *
from agent.tools import write_file, read_file, get_current_directory, list_file
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
# _ = load_dotenv()

import os

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)  # ✅ use the variable

api_key = os.environ.get("GROQ_API_KEY")
print(f"API Key: {api_key}")

set_debug(True)
set_verbose(True)

# llm = ChatGroq(model="openai/gpt-oss-120b")


llm = ChatGroq(model="openai/gpt-oss-120b")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

# response = llm.invoke("What is deep learning?")
# print(response.content)


def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan."""
    user_prompt = state["user_prompt"]
    resp = llm.with_structured_output(Plan).invoke(
        planner_prompt(user_prompt)
    )
    if resp is None:
        raise ValueError("Planner did not return a valid response.")
    return {"plan": resp}


def architect_agent(state: dict) -> dict:
    """Creates TaskPlan from Plan."""
    plan: Plan = state["plan"]
    resp = llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(plan=plan.model_dump_json())
    )
    if resp is None:
        raise ValueError("Planner did not return a valid response.")

    resp.plan = plan
    print(resp.model_dump_json())
    return {"task_plan": resp}


def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent."""
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]
    existing_content = read_file.run(current_task.filepath)

    system_prompt = coder_system_prompt()
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
    )

    coder_tools = [read_file, write_file, list_file, get_current_directory]
    react_agent = create_react_agent(llm, coder_tools)

    react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
                                     {"role": "user", "content": user_prompt}]})

    coder_state.current_step_idx += 1
    return {"coder_state": coder_state}


graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)

graph.set_entry_point("planner")
agent = graph.compile()
if __name__ == "__main__":
    result = agent.invoke({"user_prompt": "Build a colourful modern todo app in html css and js"},
                          {"recursion_limit": 100})
    print("Final State:", result)