class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, error):
        # Proportional term
        P = self.kp * error

        # Integral term
        self.integral += error
        I = self.ki * self.integral

        # Derivative term
        derivative = error - self.prev_error
        D = self.kd * derivative

        # PID output
        output = P + I + D

        # Update previous error for the next iteration
        self.prev_error = error

        return output

if __name__ == "__main__":
    # Example usage:
    # Setpoint is the desired value you want the system to reach
    setpoint = 100.0

    # PID gains (you may need to adjust these depending on your system)
    kp = 0.1
    ki = 0.01
    kd = 0.05

    # Create a PID controller instance
    pid_controller = PIDController(kp, ki, kd, setpoint)

    # Simulate a process (e.g., temperature control)
    current_value = 50.0

    # Run the PID controller for a number of iterations
    for _ in range(100):
        # Compute the control signal
        control_signal = pid_controller.compute(current_value)

        # Simulate the process response (you need to replace this with your actual system)
        current_value += control_signal

        print(f"Current Value: {current_value}, Control Signal: {control_signal}")
