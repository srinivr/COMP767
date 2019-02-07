import itertools
import numpy as np


class Env:

    def __init__(self, n, n_actions, p):
        self.n = n
        self.n_actions = n_actions
        self.p = p

    def step(self, state, action):
        state = list(state)
        if action == 0:
            state[0] = max(0, state[0] - 1)
        elif action == 1:
            state[1] = min(self.n-1, state[1] + 1)
        elif action == 2:
            state[0] = min(self.n-1, state[0] + 1)
        elif action == 3:
            state[1] = max(0, state[1] - 1)
        else:
            raise Exception
        return tuple(state)

    def get_all_states(self):
        return list(itertools.product(range(self.n), range(self.n)))

    def get_neighbours(self, state, action):
        neighbours = []
        if state[0] == 0 and (state[1] == 0 or state[1] == self.n-1):
            neighbours.append((state, 1., action))
            return neighbours
        for a in range(self.n_actions):
            p = (1. - self.p)/self.n_actions
            if a == action:
                p += self.p
            neighbours.append((self.step(state, a), p, a))
        return neighbours

    def get_reward(self, state, new_state):
        if state[0] == 0 and (state[1] == 0 or state[1] == self.n-1):
            return 0.
        if new_state[0] == 0 and new_state[1] == 0:
            return 1.
        elif new_state[0] == 0 and new_state[1] == self.n - 1:
            return 10.
        return 0.


class ValueIteration:

    def __init__(self, env, eps, gamma):
        self.env = env
        self.eps = eps
        self.gamma = gamma
        self.value_fn = dict()
        self.policy = dict()
        for s in env.get_all_states():
            self.value_fn[s] = 0.
            self.policy[s] = 0

    def learn(self):
        itr = 0
        while True:
            diff = 0.
            itr += 1
            for s in self.env.get_all_states():
                vals = []
                for a in range(self.env.n_actions):
                    neighbours = self.env.get_neighbours(s, a)
                    val = 0.
                    for n in neighbours:
                        # print('n', n)
                        val += (n[1] * (self.env.get_reward(s, n[0]) + self.gamma * self.value_fn[n[0]]))
                    vals.append(val)
                old_val = self.value_fn[s]
                self.value_fn[s] = np.max(vals)
                self.policy[s] = np.argmax(vals)
                diff = max(diff, np.abs(old_val - np.max(vals)))
            print('iter: {} diff: {}'.format(itr, diff))
            true_value = self.compute_true_value()
            print('TRUE: bottom left:{} bottom right{}'.format(true_value[-1][0], true_value[-1][-1]))
            print('CURRENT: bottom left:{} bottom right{}'.format(self.value_fn[(4, 0)], self.value_fn[(4, 4)]))
            if diff < self.eps:
                break
        value_fn = self._value_fn_dict_to_numpy()
        print('value_fn: {}'.format(value_fn))

    def _value_fn_dict_to_numpy(self):
        value_fn = np.zeros((self.env.n, self.env.n))
        for k in self.value_fn:
            value_fn[k] = self.value_fn[k]
        return value_fn

    def compute_true_value(self):
        P_pi = np.zeros((self.env.n ** 2, self.env.n ** 2))
        r_pi = np.zeros(self.env.n ** 2)
        for s in env.get_all_states():
            for n in env.get_neighbours(s, self.policy[s]):
                r_idx, c_idx = s[0] * self.env.n + s[1], n[0][0] * self.env.n + n[0][1]
                P_pi[r_idx, c_idx] += n[1]
                r_pi[r_idx] += (n[1] * self.env.get_reward(s, n[0]))
        # print('P_pi {} sum:{}'.format(P_pi, np.sum(P_pi, axis=1)))
        # print('r_pi {}'.format(r_pi))
        return np.linalg.solve(np.identity(self.env.n ** 2) - self.gamma * P_pi, r_pi).reshape(self.env.n, self.env.n)


class PolicyIteration:
    def __init__(self, env, eps, gamma):
        print('Policy Iteration')
        self.env = env
        self.eps = eps
        self.gamma = gamma
        self.value_fn = dict()
        self.policy = dict()
        for s in env.get_all_states():
            self.value_fn[s] = 0.
            self.policy[s] = 0

    def learn(self):
        itr = 0
        while True:
            itr += 1
            print('policy iteration:', itr)
            # evaluate policy
            v_itr = 0
            while True:
                v_itr += 1
                diff = 0.
                for s in self.env.get_all_states():
                    action = self.policy[s]
                    val = 0.
                    for n in self.env.get_neighbours(s, action):
                        val += (n[1] * (self.env.get_reward(s, n[0]) + self.gamma * self.value_fn[n[0]]))
                    old_val = self.value_fn[s]
                    self.value_fn[s] = val
                    diff = max(diff, np.abs(old_val - val))
                if diff < self.eps:
                    break
                print('policy evaluation iteration:', v_itr, 'diff:', diff)

            # policy improvement
            optimal_policy = True
            for s in self.env.get_all_states():
                old_action = self.policy[s]
                vals = []
                for a in range(self.env.n_actions):
                    neighbours = self.env.get_neighbours(s, a)
                    val = 0.
                    for n in neighbours:
                        # print('n', n)
                        val += (n[1] * (self.env.get_reward(s, n[0]) + self.gamma * self.value_fn[n[0]]))
                    vals.append(val)
                self.policy[s] = np.argmax(vals)
                if old_action != self.policy[s]:
                    optimal_policy = False

            # print('Policy iteration: {} Policy evaluation: {} diff:'.format(itr, v_itr, diff))
            if optimal_policy:
                break
        value_fn = self._value_fn_dict_to_numpy()
        print('value_fn: {}'.format(value_fn))

    def _value_fn_dict_to_numpy(self):
        value_fn = np.zeros((self.env.n, self.env.n))
        for k in self.value_fn:
            value_fn[k] = self.value_fn[k]
        return value_fn



env = Env(50, 4, 0.9)
learner = ValueIteration(env, 0.0001, 0.9)
learner.learn()
# print(learner.compute_true_value())