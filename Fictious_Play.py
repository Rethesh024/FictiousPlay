import numpy as np
import matplotlib.pyplot as plt

def fictitious_play(A, B, iterations):
    """
    Simulates fictitious play for a two-player game.
    
    A: Payoff matrix for player 1 (row player)
    B: Payoff matrix for player 2 (column player)
    iterations: Number of steps to simulate
    """
    n, m = A.shape  # n strategies for player 1, m for player 2
    
    # Count how many times each action has been played
    player1_counts = np.zeros(n)
    player2_counts = np.zeros(m)

    # Store empirical frequencies
    player1_history = []
    player2_history = []

    # Random initial actions
    # i = np.random.randint(n)
    # j = np.random.randint(m)
    i=1
    j=2

    for t in range(1, iterations + 1):
        # Update counts
        player1_counts[i] += 1
        player2_counts[j] += 1

        # Store normalized empirical strategies
        player1_strategy = player1_counts / t
        player2_strategy = player2_counts / t
        player1_history.append(player1_strategy.copy())
        player2_history.append(player2_strategy.copy())

        # Best response to opponent's empirical strategy
        expected_payoff1 = A @ player2_strategy
        expected_payoff2 = B.T @ player1_strategy
        i = np.argmax(expected_payoff1)  # Best response of Player 1
        j = np.argmax(expected_payoff2)  # Best response of Player 2

    return np.array(player1_history), np.array(player2_history)


def plot_strategies(history, player_name):
    plt.figure(figsize=(10, 5))
    for i in range(history.shape[1]):
        plt.plot(history[:, i], label=f"{player_name} strategy {i}")
    plt.xlabel("Iterations")
    plt.ylabel("Probability")
    plt.title(f"Empirical strategy of {player_name} over time")
    plt.legend()
    plt.grid(True)
    plt.show()


# Example: Rock, Paper, Scissor
A = np.array([[0, 0, 1],
              [1, 0, 0],
              [0, 1, 0]])  # Player 1 payoff matrix 

B = np.array([[0, 1, 0],
              [0, 0, 1],
              [1, 0, 0]])  # Player 2 payoff matrix 

# Run simulation
player1_history, player2_history = fictitious_play(A, B, iterations=1000)

# Plot results
plot_strategies(player1_history, "Player 1")
plot_strategies(player2_history, "Player 2")
