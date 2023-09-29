# Bosch_Hackathon_23

A Github repository containing the available source code and solution documentation for the 2023 Code #LikeABosch hybrid hackathon software challenge.

Visualization created using pygame.

## Break Distance calculation
The AASHTO stopping distance formula is as follows:

s = (0.278 × t × v) + v² / (254 × (f + G))

where:

s – Stopping distance in meters;
t – Perception-reaction time in seconds;
v – Speed of the car in km/h;
G – Grade (slope) of the road, expressed as a decimal. Positive for an uphill grade and negative for a downhill road; and
f – Coefficient of friction between the tires and the road. It is assumed to be 0.7 on a dry road and between 0.3 and 0.4 on a wet road.
This formula is taken from the book "A Policy on Geometric Design of Highways and Streets". It is commonly used in road design for establishing the minimum stopping sight distance required on a given road. With correct parameters, it's a perfect equation for the accurate calculation of the stopping distance of your car. Clearly, it's different than the typical formula used in the speed calculator.

[https://www.omnicalculator.com/physics/stopping-distance](https://www.omnicalculator.com/physics/stopping-distance)
