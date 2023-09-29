import numpy as np
import random
import torch
import gym
from gym import spaces
from preprocess_for_RL import load_csv
from PID_controller import PIDController


class AutoEmergencyBreakEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, max_acceleration, max_deceleration, max_wheel_turn_angle, safe_stop_distance, speed_offset):
        super(AutoEmergencyBreakEnv, self).__init__()

        # car attributes
        self.max_acc = max_acceleration  # m/s^2
        self.max_dec = max_deceleration  # m/s^2
        self.max_wheel_turn_angle = max_wheel_turn_angle  # in radians
        self.safe_stop_distance = safe_stop_distance  # meters
        self.speed_offset = speed_offset  # meters

        # measured attributes from the camera
        self.processed_data = load_csv()

        # actual values accounting for the RL agents actions
        self.episode_data = self.processed_data

        # reinforcement learning environment definition
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)

        low = np.array([
            min(self.processed_data["FirstObjectDistance_X"]),
            min(self.processed_data["FirstObjectDistance_Y"]),
            min(self.processed_data["SecondObjectDistance_X"]),
            min(self.processed_data["SecondObjectDistance_Y"]),
            min(self.processed_data["ThirdObjectDistance_X"]),
            min(self.processed_data["ThirdObjectDistance_Y"]),
            min(self.processed_data["FourthObjectDistance_X"]),
            min(self.processed_data["FourthObjectDistance_Y"]),
            min(self.processed_data["VehicleSpeed"]),
            min(self.processed_data["FirstObjectSpeed_X"]),
            min(self.processed_data["FirstObjectSpeed_Y"]),
            min(self.processed_data["SecondObjectSpeed_X"]),
            min(self.processed_data["SecondObjectSpeed_Y"]),
            min(self.processed_data["ThirdObjectSpeed_X"]),
            min(self.processed_data["ThirdObjectSpeed_Y"]),
            min(self.processed_data["FourthObjectSpeed_X"]),
            min(self.processed_data["FourthObjectSpeed_Y"]),
            min(self.processed_data["YawRate"])
        ])

        high = np.array([
            max(self.processed_data["FirstObjectDistance_X"]),
            max(self.processed_data["FirstObjectDistance_Y"]),
            max(self.processed_data["SecondObjectDistance_X"]),
            max(self.processed_data["SecondObjectDistance_Y"]),
            max(self.processed_data["ThirdObjectDistance_X"]),
            max(self.processed_data["ThirdObjectDistance_Y"]),
            max(self.processed_data["FourthObjectDistance_X"]),
            max(self.processed_data["FourthObjectDistance_Y"]),
            max(self.processed_data["VehicleSpeed"]) + speed_offset,
            max(self.processed_data["FirstObjectSpeed_X"]),
            max(self.processed_data["FirstObjectSpeed_Y"]),
            max(self.processed_data["SecondObjectSpeed_X"]),
            max(self.processed_data["SecondObjectSpeed_Y"]),
            max(self.processed_data["ThirdObjectSpeed_X"]),
            max(self.processed_data["ThirdObjectSpeed_Y"]),
            max(self.processed_data["FourthObjectSpeed_X"]),
            max(self.processed_data["FourthObjectSpeed_Y"]),
            max(self.processed_data["YawRate"])
        ])

        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float64)

        self.state = [value[0] if isinstance(value, (list, tuple, str)) else value for value in self.processed_data.values()]
        self.timestep = 0
        self.dt = np.mean([self.processed_data["Timestamp"][i + 1] - self.processed_data["Timestamp"][i] for i in range(len(self.processed_data["Timestamp"]) - 1)])
        self.max_distance_from_reference_movement = 5  # the maximum amount of distance the agent is abel to travel from the reference movements origo laterally

        # PID controller values
        self.proportional_gait = 0.9
        self.integral_gait = 0.1
        self.derivative_gait = 0.05

        self.wheel_PID = PIDController(kp=self.proportional_gait, ki=self.integral_gait, kd=self.derivative_gait)
        self.pedal_PID = PIDController(kp=self.proportional_gait, ki=self.integral_gait, kd=self.derivative_gait)

        # previous control values
        self.previous_wheel_angle = 0
        self.previous_pedal_value = 0
        self.second_previous_wheel_angle = 0
        self.second_previous_pedal_value = 0

        # variable to keep check how far it has strayed away from the initial position-> keeps the sim bounded
        self.distance_from_origo =0
        self.max_ep_len = self.processed_data["FourthObjectSpeed_Y"].size

    def transform_actions(self, actions):
        # transform the actions created by the agent: wheel angle and gas/break
        wheel_action = actions[0] * (self.max_wheel_turn_angle - -self.max_wheel_turn_angle) / 2 + (self.max_wheel_turn_angle + -self.max_wheel_turn_angle) / 2
        acceleration_values = actions[1] * (self.max_acc - -self.max_dec) / 2 + (self.max_acc + -self.max_dec) / 2

        return wheel_action, acceleration_values

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

    def calculate_change_in_sensor_readings(self, wheel_angle, change_in_acceleration):
        # calculate the change in the observation vector compared to the original sensory readings
        self.episode_data["YawRate"][self.timestep] = (wheel_angle - self.episode_data["YawRate"][self.timestep-1]) / self.dt
        self.episode_data["VehicleSpeed"][self.timestep] = self.episode_data["VehicleSpeed"][self.timestep-1] + change_in_acceleration * (self.dt**2)

        # change in object distances todo

    def check_if_crashed(self):
        if self.episode_data["FirstObjectDistance_X"][self.timestep] == self.episode_data["FirstObjectDistance_Y"][self.timestep] == 0:
            return True
        if self.episode_data["SecondObjectDistance_X"][self.timestep] == self.episode_data["SecondObjectDistance_Y"][self.timestep] == 0:
            return True
        if self.episode_data["ThirdObjectDistance_X"][self.timestep] == self.episode_data["ThirdObjectDistance_Y"][self.timestep] == 0:
            return True
        if self.episode_data["FourthObjectDistance_X"][self.timestep] == self.episode_data["FourthObjectDistance_Y"][self.timestep] == 0:
            return True

    def calculate_distance_from_origo(self):
        pass

    def step(self, action):
        # take a step in the simulation
        wheel_angle, pedal_value = self.transform_actions(action)

        wheel_angle = self.wheel_PID.compute(wheel_angle - self.previous_wheel_angle)
        pedal_value = self.pedal_PID.compute(pedal_value - self.previous_pedal_value)

        # increment the timestep and how the simulation changes based on the RL agents action
        self.timestep += 1
        self.calculate_change_in_sensor_readings(wheel_angle, pedal_value)

        # take a step in the simulation

        # check if the simulation is over and return the reward functions value
        reward = 0
        done = False
        crashed = self.check_if_crashed()
        in_danger_zone = False

        if crashed:
            done = True
            reward = -10
            print("Car crashed")

        if self.timestep+1 >= self.max_ep_len:
            done = True
        elif self.distance_from_origo > self.max_distance_from_reference_movement:
            done = True
            reward = -10
            print("Car went off the road")

        # define the reward function
        # sub-reward weights
        weigth_action_smoothness = 0.05
        weight_control_force = 0.05

        # divide the reward function into 2 parts (out of the danger zone and in danger zone)
        if in_danger_zone:
            # calculate how the breaking computes a reward
            pass
        else:
            # alive no issues this is the optimal state
            reward = 1

        return self.state, reward, done

    def reset(self):
        # resets the environment
        self.state = [value[0] if isinstance(value, (list, tuple, str)) else value for value in self.processed_data.values()]
        score = 0

        return self.state, score

    def close(self):
        # close the simulation -> call the internal functions of the sim
        print("Closing the simulation")
        pass

# low level controller: PID
# high level controller: RL Agent
# output 2 neurons tanh activation, steering wheel angle, acc/dec value, (maybe add honk, light)


if __name__ == "__main__":
    max_acceleration = 10  # m/s^2
    max_deceleration = 9  # m/s^2
    max_wheel_turn_angle = np.pi/2  # rad
    safe_stop_distance = 3  # m
    speed_offset = 10  # m/s

    env = AutoEmergencyBreakEnv(max_acceleration=max_acceleration, max_deceleration=max_deceleration,
                                max_wheel_turn_angle=max_wheel_turn_angle, safe_stop_distance=safe_stop_distance,
                                speed_offset=speed_offset)
    scores = []
    # test the running of the environment
    for i in range(1):
        observation, score = env.reset()
        done = False
        ep_len = score
        while not done:
            action = np.array([0, 0])  # random action
            observation_, reward, done = env.step(action)
            score += reward
            ep_len += 1

        scores.append(score)
        print("Score: ", score, ", Episode length: ", ep_len, ", Score in percent to max: ", score / ep_len * 100, " Average score: ", np.mean(scores))

    env.close()



