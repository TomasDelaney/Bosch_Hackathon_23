import numpy as np
import gym
from gym.utils import seeding
from gym import spaces


class AutoEmergencyBreakEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, max_acceleration, max_deceleration, max_wheel_turn_angle):
        super(AutoEmergencyBreakEnv, self).__init__()
        # car attributes

        # measured attributes from the camera

        # actual values accounting for the RL agents actions

    def init_training_start(self):
        # loads the csv and initialises the state vector
        pass

    def transform_actions(self, actions):
        # transform the actions created by the agent: wheel angle and gas/break
        pass

    def set_seed(self):
        # seed setting for reproducibility’s sake
        pass

    def reset(self):
        # resets the environment
        pass

# low level controller: PID
# high level controller: RL Agent
# output 2 neurons tanh activation, steering wheel angle, acc/dec value, (maybe add honk, light)
