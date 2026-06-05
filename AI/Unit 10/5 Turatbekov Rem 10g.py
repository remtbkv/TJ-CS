import random
import numpy as np

def trials(n_trials = 10):
    policies = [0, 0.001, 0.01, 0.1, 0.5, 1, "Greedy w/ UCB", "0.1-Greedy w/ UCB"]
    avg_scores, ideals = [[] for _ in range(len(policies))], []
    text = {0: "Greedy", 1: "Random"}
    for _ in range(n_trials):
        n_b = 10
        bandits = [random.normalvariate(0, 1) for _ in range(n_b)]
        ideals.append(max(bandits)*2000)
        for ind, epsilon in enumerate(policies):
            policy_scores = []
            for game in range(200):
                Q_vals, selected  = np.zeros(n_b), np.zeros(n_b)
                game_score = 0
                for move in range(1,2001):
                    if "UCB" in str(epsilon):
                        e = 0
                        if "0.1" in str(epsilon):
                            e = 0.1
                        chosen = random.choice(range(n_b)) if random.random() < e else np.argmax(Q_vals + 2*np.log(move)/(selected+1e-10))
                        game_score += (score := random.normalvariate(bandits[chosen], 1))
                        selected[chosen] += 1
                        Q_vals[chosen] += (score - Q_vals[chosen])/selected[chosen]
                    else:
                        chosen = random.choice(range(n_b)) if random.random() < epsilon else np.argmax(Q_vals)
                        game_score += (score := random.normalvariate(bandits[chosen], 1))
                        selected[chosen] += 1
                        Q_vals[chosen] += (score - Q_vals[chosen])/selected[chosen]
                policy_scores.append(game_score)
            avg_scores[ind].append(np.mean(policy_scores))
    for ind, pol in enumerate(policies):
        pol = text[pol] if pol in text else pol
        print(f"Policy {pol} - avg score: {np.mean(avg_scores[ind])}")
    print(f"Average ideal score: {np.mean(ideals)}")


def submit():
    policies = [0, 0.001, 0.01, 0.1, 0.5, 1, "Greedy w/ UCB", "0.1-Greedy w/ UCB"]
    text = {0: "Greedy", 1: "Random"}
    n_b = 10
    bandits = [random.normalvariate(0, 1) for _ in range(n_b)]
    for epsilon in policies:
        policy_scores = []
        for game in range(200):
            Q_vals, selected  = np.zeros(n_b), np.zeros(n_b)
            game_score = 0
            for move in range(1,2001):
                if "UCB" in str(epsilon):
                    e = 0
                    if "0.1" in str(epsilon):
                        e = 0.1
                    chosen = random.choice(range(n_b)) if random.random() < e else np.argmax(Q_vals + 2*np.log(move)/(selected+1e-10))
                    game_score += (score := random.normalvariate(bandits[chosen], 1))
                    selected[chosen] += 1
                    Q_vals[chosen] += (score - Q_vals[chosen])/selected[chosen]
                else:
                    chosen = random.choice(range(n_b)) if random.random() < epsilon else np.argmax(Q_vals)
                    game_score += (score := random.normalvariate(bandits[chosen], 1))
                    selected[chosen] += 1
                    Q_vals[chosen] += (score - Q_vals[chosen])/selected[chosen]
            policy_scores.append(game_score)
        pol = text[epsilon] if epsilon in text else epsilon
        print(f"Policy {pol} - avg score: {np.mean(policy_scores)}")
    print(f"Average ideal score: {max(bandits)*2000}")

submit()