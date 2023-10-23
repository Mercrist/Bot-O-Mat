from __future__ import annotations # to type hint the return for self
from enum import Enum
from Task import Task # for type hinting
from time import sleep, perf_counter

class RobotType(str, Enum):
    """Retrieves the Robot types from
    an enum. Facilitates processing."""
    UNIPEDAL = "Unipedal"
    BIPEDAL = "Bipedal"
    QUADRUPEDAL = "Quadrupedal"
    ARACHNID = "Arachnid"
    RADIAL = "Radial"
    AERONAUTICAL = "Aeronautical"

class Robot:
    def __init__(self, robot_type: str, name: str):
        """Initializes a robot based on the given
        type and given name by the user."""
        if type(robot_type) != str:
            raise TypeError(f"Invalid parameter type given for the robot type. Expected 'str' but got " +
                            f"{type(robot_type)}.")

        if type(name) != str:
            raise TypeError(f"Invalid parameter type given for the robot name. Expected 'str' but got " +
                            f"{type(name)}.")

        if not robot_type or len(robot_type) < 5:
            # Not a valid input or shorter than the shortest type length
            raise ValueError("Invalid input for the given robot type.")

        if not name or len(name) < 1:
            raise ValueError("Invalid input for the given robot name.")

        robot_type = robot_type[0].upper() + robot_type[1:].lower() # facilitate input processing
        self.robot_type = RobotType(robot_type).name  # gets the enum variable instead of just the string
        self.name = name
        self.task_list = [] # Each robot handles a list of assigned tasks
        self.tasks_completed = 0
        self.elapsed = 0

    def __str__(self):
        return f"{self.robot_type}, {self.name}"

    def run_tasks(self) -> Robot:
        """Executes all assigned tasks for the given Robot."""
        start = perf_counter()  # includes sleep time
        while self.task_list:
            to_process = self.task_list.pop(0) # Pick and remove first available task
            self.process_task(to_process)
        self.elapsed = perf_counter() - start
        return self # return the modified object, running process only has a copy of it

    def process_task(self, task: Task) -> None:
        """Processes a task from the task list.
        Each task has a valid ETA in milliseconds."""
        secs = task.eta/1000
        print(f"{self.name} is beginning work on Task#{task.id}...")
        sleep(secs) # Will sleep the current process, not the main process
        print(f"{self.name} has completed work on Task#{task.id}!")
        # Only count tasks fit for this robot type as completed
        if task.rob_type is None or task.rob_type.name == self.robot_type:
            self.tasks_completed += 1