class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp  # Proportional gain
        self.Ki = Ki  # Integral gain
        self.Kd = Kd  # Derivative gain

        self.prev_error = 0
        self.integral = 0

    def update(self, setpoint, pv, dt):
        error = setpoint - pv

        # Proportional term
        P = self.Kp * error

        # Integral term
        self.integral += error * dt
        I = self.Ki * self.integral

        # Derivative term
        derivative = (error - self.prev_error) / dt
        D = self.Kd * derivative

        # Calculate the control output
        output = P + I + D

        # Update previous error for the next iteration
        self.prev_error = error

        return output