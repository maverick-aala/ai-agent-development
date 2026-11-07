"""
Day 09 — Manual test: walk through create_state → add_action → record_observation → finish without MCP or LLM.

Run: python test_state.py from the day09/agent directory (or adjust PYTHONPATH).
"""

from state import (
    create_state,
    add_action,
    record_observation,
    next_step,
    finish,
)

# create_state() takes the user text and optional max_steps (default 5).
state = create_state(
    "Generate a password and tell me the time when it was created."
)

print("Initial state: ")  # print() writes a label to the console before showing the dict.
print(state)  # print(state) shows all keys: user_request, current_step, actions, etc.

add_action(state, "generate_password")  # Simulates the planner choosing generate_password.

record_observation(
    state,
    "generate_password",
    "Password: nd78^*&^",
)  # Simulates MCP returning a password string.

next_step(state)  # current_step becomes 1 as if one loop iteration completed.

print("\nState After one iteration")
print(state)

finish(
    state,
    "Password: nd78^*&^ \nCurrent Time: 10:45",
)  # Simulates format_answer() output when planner returns FINISH.

print("\nFinal State")
print(state)
