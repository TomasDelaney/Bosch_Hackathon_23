# Bosch_Hackathon_23

A Github repository containing the available source code and solution documentation for the 2023 Code #LikeABosch hybrid hackathon software challenge.

Visualization created using pygame.

---
## Guide to running the code

```bash
pip install pandas
pip install pygame
```

```python

python main.py

python simulation.py
```

-----

## Functional layer implementation:
The purpose of the functional layer is to control the Automatic Emergency Brake (AEB) inorder to avoid or mitigate collisions. Our functional layer solution involves a reinforcement learning based PID controller hybrid controller which aims to address the following challenges: 1) Addressing the dynamic, complex environments which commonly occur during driving, 2) Ability to deploy different types of risk averse behaviours specified to the drivers need, 3) Sensor fusion capacities and deep learning based embeddings learning of the environment characteristics, 4) Safe implementation through a simulation based learning environment which then can be transferred safely to real life cars, based on minimal sensor recordings.

# 1) Addressing the dynamic, complex environments which commonly occur during driving
Everyday driving situations are one of the most complex situations people find themselves throughout their day. The fact that there are multiple other drivers, types of vehicles, oncoming/incoming traffic, traffic signs and driving signs associated with each person makes it an increadibly complex and stochastic environment. Therefore creating an accurate model which takes all these different factors into account is an almost impossible task. No wonder why so many companies like Waymo, Tesla and Almotive turn to reinforcement learning based solutions to handle self driving and why this field is such a hot topic for self driving research.

Our solution aim to encorporate the ability of reinforcement learning to accurately traverse complex environments, with the stability of a traditional PID controller to ensure a highly stable and accurate emergency breaking system. This solution serves as a proof of concept that given a dangerous driving situation occuring the controller is able to mitigate the effects of a crash or is able to completely avoid it. This controller is able to learn a robust control policy despite minimal data available through simulation. We can think of the given dataset as a reference "level" which displays certain situations which our controller should handle, therefore even though we have limited amount of data our simulation is able to create distinct datapoints using these references, and eventually through exploration it is able to solve this environment. This solution serves as a proof of concept that if this controller can adapt to an optimal AEB control thorough modest amounts of real world recordings, it therefore can adapt to different situations given the relevant data.

The controller is able to control the throttle/brake pedal and the wheel of the car therefore not only being able to stop a car to avoid a colission, but actually to make a collision avoidance maneuver if braking is not an option.

Our solution is based on a model-free reinforcement learning algorithm, which does not rely on complex model of the environment, traffic and other drivers behaviour, but can learn from different collected and simulated driving situations. One of the main advantages of reinforcement learning is the fact that we can create a reward function which the RL-controller aims to achieve in all simulation timesteps, without extensive modeling of how to achieve such state. Our control promotes collission avoidance by using the minimal change in speed and wheel angle, while maximizing the safety of the passengers and promoting the avoidance of these dangerous situations all together.

# 2) Ability to deploy different types of risk averse behaviours specified to the drivers need
Through the different weight settings of this reward function we can customize the AEB-s behaviour to suit different driving styles of the driver, such as was done by Tesla fielding multiple styles of self-driving modes in their cars.

# 3) Sensor fusion capacities and deep learning based embeddings learning of the environment characteristics
This approach supports the use of additional, somewhat redundant sensory information fusion since it can make connections between these through the help of underlying neural networks. The algorithm used in our reinforcement learning based controller relies on the TD7 algorithm, which is capable of learning the underlying structure of the sensory and environment information through the use of an encoder network. Therefore solving the problem which arises from the lack of input features which is a common occurence when creating a reinforcement learning agent in a driving related environment.

# 4) Safe implementation through a simulation based learning environment which then can be transferred safely to real life cars, based on minimal sensor recordings
Through the use of simulation we can safely allow our controller to train and explore a wide set of possible controller behaviours, which then can be implemented in real worl cars as done by: https://www.nature.com/articles/s41586-023-06419-4, where through the residual modeling of sensor noise, even 50 seconds of real life recordings were enough to teach world champion level drone control through a reinforcement learning based controller.  

