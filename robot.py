import wpilib
import wpilib.drive

# Gamepad axes

LEFT_AXIS = 1
RIGHT_AXIS = 5
LIFT_AXIS = 0  # Should be triggers
ARM_AXIS = 4

# Initiate Deadzone values
DEFAULT_DEADZONE = .3
DEADZONES = {LEFT_AXIS: DEFAULT_DEADZONE, RIGHT_AXIS: DEFAULT_DEADZONE,
             LIFT_AXIS: .3, ARM_AXIS: DEFAULT_DEADZONE}

# Initiate reverse values
DEFAULT_REVERSE = False
REVERSES = {LEFT_AXIS: DEFAULT_REVERSE, RIGHT_AXIS: DEFAULT_REVERSE,
            LIFT_AXIS: DEFAULT_REVERSE, ARM_AXIS: DEFAULT_REVERSE}

# Initiate Speed caps
DEFAULT_SPEED_CAP = [-.5, .5]
SPEED_CAPS = {LEFT_AXIS: DEFAULT_SPEED_CAP, RIGHT_AXIS: DEFAULT_SPEED_CAP,
              LIFT_AXIS: [-1, 1], ARM_AXIS: DEFAULT_SPEED_CAP}

# Controller ports

LEFT_PORT = 0
RIGHT_PORT = 1
LIFT_PORT = 5
ARM_PORT = 3

LIFT_TOP_SWITCH_PORT = 0
ARM_LEFT_RIGHT_SWITCH_PORT = 1

GAMEPAD_NUM = 0  # This should prolly always be zero


# TODO: Add speed caps and scales


class Robot(wpilib.IterativeRobot):

    def __init__(self):
        super().__init__()

        # Initiate up robot drive
        self.left_motor = wpilib.Spark(LEFT_PORT)
        self.right_motor = wpilib.Spark(RIGHT_PORT)

        # Initiate arm and lift
        self.robot_lift = wpilib.PWMTalonSRX(LIFT_PORT)
        self.robot_arm = wpilib.PWMTalonSRX(ARM_PORT)

        # Initiate limit switches
        self.lift_top = wpilib.DigitalInput(LIFT_TOP_SWITCH_PORT)
        self.arm_left_right = wpilib.DigitalInput(ARM_LEFT_RIGHT_SWITCH_PORT)

        self.limits = set()
        self.buttons = set()

        # Initiate gamepad
        self.game_pad = wpilib.Joystick(GAMEPAD_NUM)

    def stop(self):
        """Stops all motors which are currently moving"""
        if self.left_motor.get() != 0:
            self.left_motor.set(0)
        if self.right_motor.get() != 0:
            self.right_motor.set(0)
        if self.robot_lift.get() != 0:
            self.robot_lift.set(0)
        if self.robot_arm.get() != 0:
            self.robot_arm.set(0)

    def disable(self):
        """Disables speed controllers"""
        # TODO: Fix talons not showing the robot is disabled with a solid orange light
        # TODO: Redo drive based on tank-drive example in robotpy examples repo
        #       Use safety and expiration and whatever else, figure them out
        pass

    # Events
    def robotInit(self):
        """Runs at the same time as __init__. Appears to be redundant"""
        pass

    def robotPeriodic(self):
        pass

    def disabledInit(self):
        self.stop()

    def disabledPeriodic(self):
        self.stop()

    def autonomousInit(self):
        self.limits = set()
        print("AUTO INIT")

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.limits = set()
        print("TELE INIT")

    def teleopPeriodic(self):

        # print(self.lift_top.get(), self.arm_left_right.get())

        axes = self.get_axes()

        print(axes)

        # Check limit switches
        # if self.lift_top.get():
        #     # Hit top of lift
        #     self.limits.add("TOP")
        # if self.arm_left_right.get():
        #     # Hit top of lift
        #     self.limits.add("ARM")

        self.left_motor.set(axes[LEFT_AXIS])
        self.right_motor.set(axes[RIGHT_AXIS])

        # Check lift axis position
        lift_value = axes[LIFT_PORT]
        # if lift_value < 0 and "TOP" in self.limits:
            # If the top limit switch is triggered and the lift was lowered,
            # untrigger limit switch
            # self.limits.remove("TOP")
        # if not (lift_value > 0 and "TOP" in self.limits):
        #     pass
            # Only move lift if not going up and at top
        self.robot_lift.set(axes[LIFT_AXIS])
            # print("Moving, not at top or not moving up")
        # print("LIFT", self.robot_lift.get(), "STICK", axes[LIFT_AXIS])

        self.robot_arm.set(axes[ARM_AXIS])

    def get_raw_axes(self):
        """Return a dictionary of controller axes"""
        i = 0
        axes = {}
        while True:
            try:
                value = self.game_pad.getRawAxis(i)
                # if i == 2:
                #     print("TRIGGER", value)
                axes[i] = round(value, 2)
            except IndexError:
                break
            i += 1
        return axes

    def get_axes(self):
        """Returns the current axes and values with deadzones and scaled"""
        axes = self.get_raw_axes()
        # Correct deadzones and scale
        for axis in axes:
            if axis in DEADZONES:
                value = axes[axis]
                neg = -1 if axes[axis] < 0 else 1
                deadzone = DEADZONES[axis]
                if abs(value) > deadzone:
                    value -= deadzone * neg
                    value /= 1 - deadzone
                    value *= SPEED_CAPS[axis][1]
                else:
                    value = 0
                if REVERSES[axis]:
                    value *= -1
                axes[axis] = value
        # if LIFT_PORT in axes:
        #     print("SCALED TRIGGER", axes[LIFT_PORT])
        return axes


if __name__ == '__main__':
    wpilib.run(Robot)
