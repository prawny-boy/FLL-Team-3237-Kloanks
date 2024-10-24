from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color, Axis, Direction, Button
from pybricks.tools import wait, Matrix, StopWatch, hub_menu
from pybricks.robotics import DriveBase
from pybricks.hubs import PrimeHub

# Constants
DRIVEBASE_WHEEL_DIAMETER = 56
DRIVEBASE_AXLE_TRACK = 105 # confirm this value
LOW_VOLTAGE = 7000
HIGH_VOLTAGE = 8000
MENU_OPTIONS = ["1", "2", "3", "4", "5", "6", "7", "C"]
ROBOT_SPEED = 500
ROBOT_ACCELERATION = 500
ROBOT_TURN_RATE = 500
ROBOT_TURN_ACCELERATION = 500

# Variables
battery_status_light = Color.GREEN

# Define the Robot
class Robot:
    def __init__(self):
        # DRIVE MOTORS: Left (A ) Right (B) Big (E) Small (F)
        self.leftDrive = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        self.rightDrive = Motor(Port.B)
        self.big = Motor(Port.E)
        self.small = Motor(Port.F)

        # Defines the drivebase
        self.driveBase = DriveBase(self.leftDrive, self.rightDrive, DRIVEBASE_WHEEL_DIAMETER, DRIVEBASE_AXLE_TRACK)
        self.driveBase.use_gyro(False)
        self.driveBase.settings(
            straight_speed=ROBOT_SPEED, 
            straight_acceleration=ROBOT_ACCELERATION, 
            turn_rate=ROBOT_TURN_RATE, 
            turn_acceleration=ROBOT_TURN_ACCELERATION
        )

        # Defines the hub
        self.hub = PrimeHub(front_side=-Axis.Y)
        self.hub.system.set_stop_button(Button.BLUETOOTH)
    
    # add wait parameter to plug in to functions for these below
    def MoveSmallMotorInDegrees(self, degrees:float, speed:float=ROBOT_TURN_RATE, wait:bool = True):
        self.driveBase.use_gyro(True)
        self.small.run_angle(speed, degrees, wait=wait)
        self.driveBase.use_gyro(False)
    
    def MoveBigMotorInDegrees(self, degrees:float, speed:float=ROBOT_TURN_RATE, wait:bool = True):
        self.driveBase.use_gyro(True)
        self.big.run_angle(speed, degrees, wait=wait)
        self.driveBase.use_gyro(False)
    
    def MoveSmallMotorUntilStalled(self, speed:float=ROBOT_TURN_RATE, duty_limit:int=50):
        self.small.run_until_stalled(speed, duty_limit=duty_limit)

    def MoveBigMotorUntilStalled(self, speed:float=ROBOT_TURN_RATE, duty_limit:int=50):
        self.big.run_until_stalled(speed, duty_limit=duty_limit)
    
    def DriveForDistance(self, distance:float, wait:bool = True):
        self.driveBase.use_gyro(True)
        self.driveBase.straight(distance, wait=wait)
        self.driveBase.use_gyro(False)
    
    def DriveForMilliseconds(self, milliseconds:float, speed:float=ROBOT_SPEED):
        self.driveBase.drive(speed, 0)
        wait(milliseconds)
        self.driveBase.stop()
    
    def TurnInPlace(self, degrees:float, wait:bool=True):
        self.driveBase.use_gyro(True)
        self.driveBase.turn(degrees, wait=wait)
        self.driveBase.use_gyro(False)
    
    def Curve(self, radius:float, angle:float, wait:bool=True):
        self.driveBase.use_gyro(True)
        self.driveBase.curve(radius, angle, wait=wait)
        self.driveBase.use_gyro(False)

    def DisplayNumber(self, number:int):
        self.hub.display.off()
        self.hub.display.number(number)

    def StatusLight(self, color:Color):
        self.hub.light.off()
        self.hub.light.on(color)
    
    def BatteryDisplay(self):
        # display battery of hub
        v = self.hub.battery.voltage()
        vPct = Rescale(v, LOW_VOLTAGE, HIGH_VOLTAGE, 1, 100)
        print(f"Battery %: {vPct}, Voltage: {v}")
        if vPct < 70:
            if vPct < 40:
                print("EMERGENCY: BATTERY LOW!")
                battery_status_light = Color.RED
            else:
                print("Battery is below 70% Please charge!")
                battery_status_light = Color.YELLOW
            self.StatusLight(battery_status_light)
        else:
            self.StatusLight(battery_status_light)
    
    def CleanMotors(self):
        self.leftDrive.run_angle(999, 1000, wait=False)
        self.rightDrive.run_angle(999, 1000, wait=False)
        self.big.run_angle(999, 1000, wait=False)
        self.small.run_angle(999, 1000)

class Animations:
    running = [
        Matrix([
            [0, 0, 100, 100, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 100, 100, 0, 0]
        ]), Matrix([
            [100, 0, 0, 100, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 100, 0, 0, 100]
        ]), Matrix([
            [100, 100, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 100, 100]
        ]), Matrix([
            [100, 100, 100, 0, 0],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [0, 0, 100, 100, 100]
        ]), Matrix([
            [100, 100, 100, 100, 0],
            [100, 0, 0, 0, 0],
            [100, 0, 0, 0, 100],
            [0, 0, 0, 0, 100],
            [0, 100, 100, 100, 100]
        ]), Matrix([
            [100, 100, 100, 100, 100],
            [100, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 100],
            [100, 100, 100, 100, 100]
        ]), Matrix([
            [100, 100, 100, 100, 100],
            [0, 0, 0, 0, 100],
            [0, 0, 0, 0, 0],
            [100, 0, 0, 0, 0],
            [100, 100, 100, 100, 100]
        ]), Matrix([
            [0, 100, 100, 100, 100],
            [0, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 0],
            [100, 100, 100, 100, 0]
        ])
    ]

class Missions:
    # Sorted in order of what we are doing

    def Boat(r:Robot): # Start with the robot facing the boat in the middle about 7 cm away
        # Reset the angle
        r.MoveSmallMotorUntilStalled(500)
        r.MoveSmallMotorInDegrees(-60, 500)
        r.DriveForDistance(80)
        r.MoveSmallMotorInDegrees(-180, 500)
    
    def Seaweed(r:Robot):
        r.MoveBigMotorInDegrees(45)

    def Whales(r:Robot):
        r.MoveSmallMotorInDegrees(-90, 500)
        r.DriveForDistance(-100)
        r.TurnInPlace(-90)
        r.DriveForDistance(100)
        r.TurnInPlace(90)
        r.MoveSmallMotorInDegrees(180, 500)
        r.DriveForDistance(100)
        r.MoveSmallMotorInDegrees(90, 500)

    def Octopus(r:Robot): # start with the robot facing the pusher in the middle
        r.DriveForDistance(-300, 800)

    def Boxes(r:Robot):
        pass

    def CoralNursery(r:Robot):
        pass

    def Shark(r:Robot):
        pass

    def CoralReef(r:Robot):
        pass
    
    def ResearchShip(r:Robot):
        # add putting the things into the research ship here
        pass

    def AnglerFish(r:Robot):
        pass

    def Submarine(r:Robot):
        pass

# run functions
def Run1(r:Robot):
    # Home location
    r.DriveForDistance(350)
    r.TurnInPlace(45)
    # Boat mission
    Missions.Boat(r)
    r.DriveForDistance(-50)
    r.MoveSmallMotorInDegrees(90, 500)
    r.TurnInPlace(-45)
    r.DriveForDistance(300)
    r.TurnInPlace(-90)
    r.DriveForDistance(-80)
    # Seaweed mission
    Missions.Seaweed(r)
    r.DriveForDistance(50)
    r.TurnInPlace(-90)
    r.DriveForDistance(700)
    # Home location

def Run2(r:Robot):
    # Home location
    r.DriveForDistance(1000)
    r.TurnInPlace(180)
    # Whales mission
    Missions.Whales(r)
    r.DriveForDistance(50)
    r.TurnInPlace(-90)
    r.DriveForDistance(100)
    r.TurnInPlace(90)
    r.DriveForDistance(200)
    r.TurnInPlace(-45)
    # Octopus mission
    Missions.Octopus(r)
    r.DriveForDistance(300)

    # Home location

def Run3(r:Robot):
    # Home location

    # Boxes mission
    Missions.Boxes(r)

    # Away Location

def Run4(r:Robot):
    # Away Location

    # Shark mission
    Missions.Shark(r)

    # Coral Nursery mission
    Missions.CoralNursery(r)

    # Away Location

def Run5(r:Robot):
    # Away Location

    # Coral Reef Mission
    Missions.CoralReef(r)

    # Away Location

def Run6(r:Robot):
    # Away Location

    # Research Ship Mission
    Missions.ResearchShip(r)

    # Home Location

def Run7(r:Robot):
    # Home Location

    # Angler Fish Mission
    Missions.AnglerFish(r)

    # Submarine Mission
    Missions.Submarine(r)

# Utility functions
def Rescale(value, in_min, in_max, out_min, out_max):
    neg = value / abs(value) # will either be 1 or -1
    value = abs(value)
    if value < in_min: value = in_min
    if value > in_max: value = in_max
    retvalue = (value - in_min) * (out_max / (in_max - in_min))
    if retvalue > out_max: retvalue = out_max
    if retvalue < out_min: retvalue = out_min
    return retvalue * neg

def RunMission(r:Robot, selected):
    # run current selection
    r.StatusLight(Color.YELLOW)
    r.hub.display.animate(Animations.running, 30)
    print(f"Running #{selected}...")
    start_time = stopwatch.time()
    if selected == "1":
        Run1(r)
        all_start_time = stopwatch.time()
    elif selected == "2":
        Run2(r)
    elif selected == "3":
        Run3(r)
    elif selected == "4":
        Run4(r)
    elif selected == "5":
        Run5(r)
    elif selected == "6":
        Run6(r)
    elif selected == "7":
        Run7(r)
        print("All missions complete.\n---------------------------------------\nRESULTS:")
        try:
            alltotaltime = round((stopwatch.time() - all_start_time)/ 1000, 1)
            print(f"Total time: {alltotaltime} seconds. This is {round(alltotaltime/150*100, 1)}% of the time")
            if alltotaltime > 150:
                print(f"Time exceeded by {150-alltotaltime} seconds.")
            print("---------------------------------------")
        except UnboundLocalError:
            print("You didn't run everything.")
    print(f"Done running #{selected}. Time: {round((stopwatch.time() - start_time)/ 1000, 1)} seconds.")
    r.StatusLight(battery_status_light)
    return selected

# create robot
my_robot = Robot()

# create stopwatch
stopwatch = StopWatch()

# display battery
my_robot.BatteryDisplay()

# run menu
last_run = "C"
while True:
    # Test this later
    current_menu = []
    for i in range(len(MENU_OPTIONS)):
        current_menu.append(MENU_OPTIONS[(i+MENU_OPTIONS.index(last_run)+1) % len(MENU_OPTIONS)])
    selected = hub_menu(*current_menu)
    if not selected == "C":
        last_run = RunMission(my_robot, selected)
    else:
        my_robot.CleanMotors()