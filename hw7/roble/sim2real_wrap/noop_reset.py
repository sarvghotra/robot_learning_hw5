from typing import Tuple

import numpy as np
from gymnasium.core import Wrapper

class RandomActResetEnv(Wrapper):
    def __init__(self, env, max_num_random_act=4):
        """Sample initial states by taking random number of no-ops on reset.
        No-op is assumed to be action 0.
        """
        super().__init__(env)
        self.max_num_random_act=max_num_random_act
        self._action_space = env.action_space

    def _sample_num_repeat(self):
        return int(np.random.randint(0, self.max_num_random_act))

    def _sample_rand_action(self):
        low = self._action_space.low
        high = self._action_space.high
        return np.random.uniform(low=low, high=high)

    def reset(self, **kwargs) -> Tuple[np.ndarray, dict]:
        obs, ORIG_INFO = super(RandomActResetEnv, self).reset(**kwargs)

        num_random_act = self._sample_num_repeat()
        # TODO: sample random action and step, possibly resetting env in the process
        for _ in range(num_random_act):
            rand_act = self._sample_rand_action()
            obs, reward, done, trunc, ORIG_INFO = self.step(rand_act)
            if done:
                self.reset(**kwargs)

        return obs, ORIG_INFO

    def step(self, ac):
        return self.env.step(ac)