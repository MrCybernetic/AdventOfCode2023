from typing import Callable


def get_final_state_after_avoiding_cycles(initial_state: str, step_func: Callable, max_steps: int) -> str:
    previous_states = {}
    cycle_length = 0
    current_state = initial_state
    for steps_done in range(max_steps):
        current_state = step_func(current_state)
        if current_state not in previous_states:
            previous_states[current_state] = steps_done
        else:
            cycle_length = steps_done - previous_states[current_state]
            nth_step_in_cycle = previous_states[current_state]
            steps_to_do = (max_steps - steps_done) % cycle_length
            for _ in range(nth_step_in_cycle + steps_to_do):
                current_state = step_func(current_state)
            return current_state
    return current_state
