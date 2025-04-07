from collections import defaultdict

def run_selection_strategy(costs, preference='min'):
    num_options = 4
    rounds = 7
    accumulated = [0] * num_options
    chosen = []
    overall_cost = 0

    for round_index in range(rounds):
        current_round = round_index + 1
        if current_round == 1:
            choice = 0
        else:
            smallest = min(accumulated)
            contenders = [idx for idx in range(num_options) if accumulated[idx] == smallest]
            if preference == 'min':
                choice = min(contenders)
            elif preference == 'max':
                choice = max(contenders)
            else:
                raise ValueError("Unsupported preference")
        
        chosen_option = choice + 1  # Convert to 1-based indexing
        chosen.append(chosen_option)
        overall_cost += costs[round_index][choice]

        for idx in range(num_options):
            accumulated[idx] += costs[round_index][idx]

    return chosen, overall_cost

def calculate_external_regret(costs, algo_cost):
    per_option_total = [sum(col) for col in zip(*costs)]
    optimal = min(per_option_total)
    return algo_cost - optimal

def calculate_swap_regret(picks, costs):
    history = defaultdict(list)
    for time_step, selected in enumerate(picks):
        history[selected].append(time_step)
    
    total_arms = len(costs[0])
    optimal_switch = {}

    for source_arm in history:
        best_sum = float('inf')
        best_replacement = None
        for candidate in range(1, total_arms + 1):
            switch_cost = sum(costs[t][candidate - 1] for t in history[source_arm])
            if switch_cost < best_sum:
                best_sum = switch_cost
                best_replacement = candidate
        optimal_switch[source_arm] = (best_replacement, best_sum)

    swap_cost = sum(c for _, c in optimal_switch.values())
    actual_cost = sum(costs[t][p - 1] for t, p in enumerate(picks))

    return actual_cost - swap_cost

# Generating specific cost sequences

arms = 4
time_steps = 7

# Cost matrix A
matrix_a = []
for t in range(1, time_steps + 1):
    row_data = []
    for a in range(1, arms + 1):
        row_data.append(1 if (t - a) % 4 == 0 else 0)
    matrix_a.append(row_data)

# Cost matrix B
matrix_b = []
for t in range(1, time_steps + 1):
    row_data = []
    for a in range(1, arms + 1):
        row_data.append(0 if (t - a) % 4 == 0 else 1)
    matrix_b.append(row_data)

# Simulating different strategy outcomes

# Strategy: original greedy (lowest tie-break) on matrix A
picks_a_default, cost_a_default = run_selection_strategy(matrix_a, 'min')
external_a_default = calculate_external_regret(matrix_a, cost_a_default)
swap_a_default = calculate_swap_regret(picks_a_default, matrix_a)

# Strategy: original greedy on matrix B
picks_b_default, cost_b_default = run_selection_strategy(matrix_b, 'min')
external_b_default = calculate_external_regret(matrix_b, cost_b_default)
swap_b_default = calculate_swap_regret(picks_b_default, matrix_b)

# Strategy: modified greedy (highest tie-break) on matrix A
picks_a_mod, cost_a_mod = run_selection_strategy(matrix_a, 'max')
external_a_mod = calculate_external_regret(matrix_a, cost_a_mod)
swap_a_mod = calculate_swap_regret(picks_a_mod, matrix_a)

# Strategy: modified greedy on matrix B
picks_b_mod, cost_b_mod = run_selection_strategy(matrix_b, 'max')
external_b_mod = calculate_external_regret(matrix_b, cost_b_mod)
swap_b_mod = calculate_swap_regret(picks_b_mod, matrix_b)

# Displaying results
print("Results for matrix A (original greedy):")
print(f"External Regret: {external_a_default}, Swap Regret: {swap_a_default}")
print("\nResults for matrix B (original greedy):")
print(f"External Regret: {external_b_default}, Swap Regret: {swap_b_default}")
print("\nResults for matrix A (modified greedy):")
print(f"External Regret: {external_a_mod}, Swap Regret: {swap_a_mod}")
print("\nResults for matrix B (modified greedy):")
print(f"External Regret: {external_b_mod}, Swap Regret: {swap_b_mod}")
