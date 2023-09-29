import gym
import numpy as np
from Car_controll_environment import AutoEmergencyBreakEnv
from TD7 import Agent


if __name__ == "__main__":
    # constants for the training
    max_acceleration = 10  # m/s^2
    max_deceleration = 9  # m/s^2
    max_wheel_turn_angle = np.pi / 2  # rad
    safe_stop_distance = 3  # m
    speed_offset = 10  # m/s

    # environment
    env = AutoEmergencyBreakEnv(max_acceleration=max_acceleration, max_deceleration=max_deceleration,
                                max_wheel_turn_angle=max_wheel_turn_angle, safe_stop_distance=safe_stop_distance,
                                speed_offset=speed_offset)
    env.set_seed(1)

    # values for training
    env_max_action = 1
    current_ep_step_counter = 0
    n_steps = 300000
    steps_count = 0
    training_scores = []
    length_of_training_episodes = []

    # agent
    agent = Agent(state_dim=env.observation_space.shape[0], action_dim=env.action_space.shape[0], max_action=env_max_action)

    while steps_count < n_steps:
        done = False
        score = 0
        episode_length = 0
        observation = env.reset()[0]
        while not done:
            # choose action
            action = agent.select_action(observation)

            # env
            observation_, reward, done = env.step(action)
            score += reward
            steps_count += 1
            current_ep_step_counter += 1
            episode_length += 1

            # transition
            agent.replay_buffer.add(observation, action, observation_, reward, done)
            observation = observation_

        # using checkpoints so run when each episode terminates
        agent.maybe_train_and_checkpoint(ep_timesteps=episode_length, ep_return=score)

        # give console feedback
        training_scores.append(score)
        avg_score = np.mean(training_scores[-100:])
        std_of_scores = np.std(training_scores[-100:])
        max_score = np.max(training_scores)
        print('steps ', steps_count, 'score %.2f' % score, 'average score %.2f' % avg_score, 'max score %.2f' % max_score, 'std of score values %.4f' % std_of_scores, 'episode length %.1f' % episode_length)
        print()
        current_ep_step_counter = 0
