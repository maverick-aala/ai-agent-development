"""
Day 09 — Agent state: a plain dictionary that tracks the user request, each tool step, and the final answer.

The loop (loop.py) reads and updates this state every iteration so the planner can see what already ran.
"""


def create_state(user_request, max_steps=5):
    """
    Create a fresh state dict before the agent loop starts.

    Parameters:
        user_request (str): Original text from the user; copied into state for the planner and final answer.
        max_steps (int, optional): Max planner→execute cycles before the loop stops (default 5). Prevents infinite loops.

    Returns:
        dict: New agent state with empty actions/observations and finished=False.
    """
    return {
        "user_request": user_request,  # What the user asked; shown in planner prompts.
        "current_step": 0,  # Zero-based counter; incremented after each tool run via next_step().
        "max_steps": max_steps,  # Upper bound compared in can_continue().
        "actions": [],  # List of tool names (strings) already chosen by the planner.
        "observations": [],  # List of dicts: step, action, observation — memory of each tool result.
        "finished": False,  # True after finish() — makes can_continue() return False.
        "final_answer": "",  # Natural-language reply set when the planner returns FINISH.
    }


def add_action(state, action):
    """
    Record that the planner chose a tool name this iteration (called after a successful execute).

    Parameters:
        state (dict): Agent state from create_state().
        action (str): Tool name returned by the planner (e.g. "generate_password"), not including FINISH.

    Returns:
        None — mutates state["actions"] in place.
    """
    state["actions"].append(action)  # append adds one item to the end of the actions list.


def record_observation(state, action, observation):
    """
    Store what the tool returned so the next planner call can read previous results.

    Parameters:
        state (dict): Agent state; uses state["current_step"] for the step field.
        action (str): Same tool name as add_action() for this iteration.
        observation (str): Text (or stringified) output from execute_action() / MCP.

    Returns:
        None — appends one dict to state["observations"].
    """
    state["observations"].append(
        {
            "step": state["current_step"],  # Which loop iteration produced this result.
            "action": action,  # Which tool was run.
            "observation": observation,  # What the tool returned (password, time, etc.).
        }
    )


def next_step(state):
    """
    Advance the loop counter after one planner→execute→record cycle.

    Parameters:
        state (dict): Agent state.

    Returns:
        None — increments state["current_step"] by 1.
    """
    state["current_step"] += 1


def can_continue(state):
    """
    Decide whether the while-loop in loop.py should run another iteration.

    Parameters:
        state (dict): Agent state.

    Returns:
        bool: True if not finished and current_step < max_steps; False otherwise.
    """
    return not state["finished"] and state["current_step"] < state["max_steps"]


def finish(state, answer):
    """
    Mark the agent done and store the user-facing final answer (from format_answer).

    Parameters:
        state (dict): Agent state.
        answer (str): Polished reply text from the LLM after planner returned FINISH.

    Returns:
        None — sets final_answer and finished=True.
    """
    state["final_answer"] = answer
    state["finished"] = True
