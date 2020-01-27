import numpy as np
import operator


class MDP:

    def __init__(self, init, actlist, terminals, gamma=0.9):
        self.init = init
        self.actlist = actlist
        self.terminals = terminals
        self.gamma = gamma
        self.states = set()
        self.policy = {}
        self.guide = []
        self.reward = {}

    def R(self, state):
        return self.reward[state]

    def T(state, action):
        pass

    def actions(self, state):
        if state in self.terminals:
            return [None]
        else:
            return self.actlist


class GridMDP(MDP):
    def __init__(self, grid, terminals, init=(0, 0), gamma=0.9):
        MDP.__init__(self, init, actlist=orientations,
                     terminals=terminals, gamma=gamma)
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        for x in range(self.cols):
            for y in range(self.rows):
                self.reward[x, y] = grid[y][x]
                if grid[y][x] is not None:
                    self.states.add((x, y))

    def T(self, state, action):
        if action == None:
            return [(0.0, state)]
        else:
            return [(0.7, self.go(state, action)),
                    (0.1, self.go(state, turn_right(action))),
                    (0.1, self.go(state, turn_left(action))),
                    (0.1, self.go(state, turn_left(turn_left(action))))]

    def go(self, state, direction):
        state1 = vector_add(state, direction)
        return if_(state1 in self.states, state1, state)

    def to_grid(self, mapping):
        return list(reversed([[mapping.get((x, y), None)
                               for x in range(self.cols)]
                              for y in range(self.rows)]))

    def to_arrows(self, policy):
        chars = {(1, 0): '>', (0, 1): '^', (-1, 0): '<', (0, -1): 'v', None: '.'}
        return self.to_grid(dict([(s, chars[a]) for (s, a) in policy.items()]))


def value_iteration(mdp, epsilon=0.1):
    U1 = dict([(s, 0) for s in mdp.states])
    R, T, gamma = mdp.R, mdp.T, mdp.gamma
    while True:
        U = U1.copy()
        delta = 0
        for s in mdp.states:
            U1[s] = R(s) + gamma * max([sum([p * U[s1] for (p, s1) in T(s, a)])
                                        for a in mdp.actions(s)])
            delta = max(delta, abs(U1[s] - U[s]))
        if delta < epsilon * (1 - gamma) / gamma:
            return U


orientations = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def turn_right(orientation):
    return orientations[orientations.index(orientation) - 1]


def turn_left(orientation):
    return orientations[(orientations.index(orientation) + 1) % len(orientations)]


def vector_add(a, b):
    return tuple(map(operator.add, a, b))


def if_(test, result, alternative):
    if test:
        return result
    else:
        return alternative


def expected_utility(a, s, U, mdp):
    return sum([p * U[s1] for (p, s1) in mdp.T(s, a)])


def argmin(seq, fn):
    best = seq[0];
    best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best


def argmax(seq, fn):
    return argmin(seq, lambda x: -fn(x))


def best_policy(mdp, U):
    for s in mdp.states:
        mdp.policy[s] = argmax(mdp.actions(s), lambda a: expected_utility(a, s, U, mdp))


def to_grid(self, mapping):
    return list([[mapping.get((x, y), None)
                  for x in range(self.cols)]
                 for y in range(self.rows)])


# def to_arrows(self, policy):
# chars = {(1, 0):'>', (0, 1):'v', (-1, 0):'<', (0, -1):'^', None: '.'}
# return self.to_grid(dict([(s, chars[a]) for (s, a) in policy.items()]))


if __name__ == '__main__':
    read = open('input.txt', 'r')
    s = int(read.readline())
    n = int(read.readline())
    o = int(read.readline())
    obstacles = [[] for i in range(o)]
    for i in range(o):
        row = read.readline().split(',')
        obstacles[i].append(int(row[0]))
        obstacles[i].append(int(row[1]))
    cars = [[] for i in range(n)]
    for i in range(n):
        row = read.readline().split(',')
        cars[i].append(int(row[0]))
        cars[i].append(int(row[1]))
    ends = [[] for i in range(n)]
    for i in range(n):
        row = read.readline().split(',')
        ends[i].append(int(row[0]))
        ends[i].append(int(row[1]))
    read.close()

    rewards_lists = []

    for i in range(n):
        rewards_lists.append(np.full(shape=(s, s), fill_value=(-1)))

    for i in range(o):
        for j in range(n):
            rewards_lists[j][obstacles[i][1]][obstacles[i][0]] = -101

    for i in range(n):
        rewards_lists[i][ends[i][1]][ends[i][0]] = 99

    print("Generating policies for cars...")

    parking_grid = []

    for i in range(n):
        g = GridMDP(rewards_lists[i], terminals=[(ends[i][0], ends[i][1])])
        parking_grid.append(g)
        U = value_iteration(g)
        print(U)
        best_policy(g, U)
        print(g.policy)
        # final_res=g.to_arrows(g,policy)
        # print(final_res)
        # final_res.reverse();
        # g.guide=list(final_res)
        # print(g.guide)

    for j in range(n):
        total_rewards = [0 for i in range(10)]
        for i in range(10):
            pos = list(cars[j])
            np.random.seed(i)
            swerve = np.random.random_sample(1000000)
            # print(swerve)
            k = 0
            while ((pos[0] != ends[j][0]) or (pos[1] != ends[j][1])):
                move = parking_grid[j].policy[(pos[0], pos[1])]
                if (swerve[k] > 0.7):
                    if (swerve[k] > 0.8):
                        if (swerve[k] > 0.9):
                            move = turn_left(turn_left(move))
                        else:
                            move = turn_left(move)
                    else:
                        move = turn_right(move)

                a = pos[0] + move[0]
                b = pos[1] + move[1]

                if (a >= 0 and b >= 0 and a < s and b < s):
                    pos[0] = a
                    pos[1] = b

                total_rewards[i] += parking_grid[j].R((pos[0], pos[1]))

                k += 1

        print(total_rewards)
        avg = int(sum(total_rewards) / len(total_rewards))
        print("Average rewards for car", j, ":", avg)
