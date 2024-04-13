import numpy as np
from gymnasium.core import Wrapper


class ActionRepeatWrapper(Wrapper):
    def __init__(self, env, max_repeat):
        super().__init__(env)
        self.max_repeat= max_repeat

        assert max_repeat >= 1

    def _sample_num_repeat(self):
        # FIXME: Bug: I think it should be 1 here
        return int(np.random.randint(1, self.max_repeat))

    def step(self, action):
        # TODO: repeat action a random number of times
        rand_num_repeat_acts = self._sample_num_repeat()
        for _ in range(rand_num_repeat_acts - 1):
            super(ActionRepeatWrapper, self).step(action)
        return super(ActionRepeatWrapper, self).step(action)
