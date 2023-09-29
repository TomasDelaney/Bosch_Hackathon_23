import numpy as np
import random
import torch
import gym
from gym.utils import seeding
from gym import spaces
from preprocess_for_RL import load_csv


class AutoEmergencyBreakEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, max_acceleration, max_deceleration, max_wheel_turn_angle):
        super(AutoEmergencyBreakEnv, self).__init__()

        # car attributes
        self.max_acc = max_acceleration
        self.max_dec = max_deceleration
        self.max_wheel_turn_angle = max_wheel_turn_angle

        # measured attributes from the camera
        self.processed_data = load_csv()

        # actual values accounting for the RL agents actions
        self.episode_data = self.processed_data

        # reinforcement learning environment definition
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)

        low = np.array([
            min(self.processed_data[""]),

        ])

        high = np.array([
            max(self.processed_data[""]),

        ])

        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float64)

        self.state = self.init_training_start()

        # PID controller values

    def init_training_start(self):
        # loads the csv and initialises the state vector
        pass

    def transform_actions(self, actions):
        # transform the actions created by the agent: wheel angle and gas/break
        pass

    def set_seed(self, seed):
        # seed setting for reproducibility’s sake
        torch.manual_seed(seed)  # Sets seed for PyTorch RNG
        torch.cuda.manual_seed_all(seed)  # Sets seeds of GPU RNG
        np.random.seed(seed)  # Set seed for NumPy RNG
        random.seed(seed)  # Set seed for random RNG
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
        print("Seed successfully set")

    def step(self, action):
        # take a step in the simulation
        pass

    def reset(self):
        # resets the environment
        pass

    def close(self):
        # close the simulation
        pass

# low level controller: PID
# high level controller: RL Agent
# output 2 neurons tanh activation, steering wheel angle, acc/dec value, (maybe add honk, light)
