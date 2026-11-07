"""
Day 09 — Agent loop: repeated plan → act → observe until FINISH or max_steps.

This file does not call OpenAI or MCP directly; it receives planner, execute_action, and format_answer as callables.
"""

from state import (
    create_state,
    add_action,
    record_observation,
    next_step,
    can_continue,
    finish,
)


async def run_agent_loop(
    user_request,
    planner,
    execute_action,
    format_answer,
    tools,
    client,
):
    """
    Run the multi-step agent until the planner says FINISH or max_steps is reached.

    Parameters:
        user_request (str): User question or task (stored in state for every planner turn).
        planner (callable): Function(state, tools) -> str; next tool name or "FINISH".
        execute_action (async callable): async (action, state, client) -> observation str.
        format_answer (callable): Function(state) -> str; final natural-language answer when finishing.
        tools (list): MCP tool metadata from discover_tools(); passed into planner().
        client: MCP FastMCP client from connect(); passed into execute_action() for call_tool.

    Returns:
        dict: Final agent state (includes final_answer when the planner finished).
    """
    # create_state() builds the empty history the planner will update each turn.
    state = create_state(user_request)

    # can_continue(state) is True while not finished and under max_steps — same pattern as a game loop.
    while can_continue(state):

        # planner() asks the LLM what to do next given user_request, past actions, and observations.
        action = planner(state, tools)
        # print() writes the planner's choice to the terminal for debugging while you learn the loop.
        print("Planner Selected: Start <=== ", action, " ===> End")

        # When the planner returns FINISH, we stop calling tools and ask format_answer() for the reply.
        if action == "FINISH":
            answer = format_answer(state)
            finish(state, answer)
            break  # break exits the while-loop immediately.

        # await execute_action() runs the MCP tool; must be async because MCP I/O is async.
        observation = await execute_action(action, state, client)

        # Remember which tool ran so the planner won't repeat it (per planner rules).
        add_action(state, action)

        # Tie tool output to this step for the next planner prompt.
        record_observation(state, action, observation)

        # Bump step counter so can_continue() can enforce max_steps.
        next_step(state)

    return state
