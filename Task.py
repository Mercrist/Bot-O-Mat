from enum import Enum
from typing import Union
import random

class Task:
    def __init__(self, description: str, eta: int, rob_type: Union[Enum, None]):
        """Initializes a task, for a robot to complete, and its
         estimated time to completion."""
        if type(description) != str:
            raise TypeError(f"Invalid parameter type given for the task description. Expected 'str' but got " +
                f"{type(description)}.")

        if type(eta) != int:
            raise TypeError(f"Invalid parameter type given for the task ETA. Expected 'int' but got " +
                f"{type(eta)}.")

        if not isinstance(rob_type, Enum) and type(rob_type) != type(None):
            raise TypeError(f"Invalid parameter type given for the robot type. Expected Enum or None but got " +
                f"{type(rob_type)}.")

        if not description:
            raise ValueError("Invalid input for the task description.")

        if not eta or eta < 1:
            raise ValueError("Invalid input for the task's ETA. Must be a positive integer value.")

        self.description = description
        self.eta = eta
        self.rob_type = rob_type
        self.id = self.__generate_id()

    def __generate_id(self) -> str:
        """Generates a random, unique 6 digit ID.
        These values uniquely identify a task once it
        has been assigned to a robot. This makes it easier to refer
        to tasks based on an ID rather than a description."""
        # Don't include 0s in the first digit.
        # 6 digits largely decreases P(same ids)
        seed = random.randint(1, 1000) # uniqueness (random is pseudorandom)
        random.seed(seed)
        return str(random.randint(1, 9)) + ''.join(random.sample("0123456789", 5))

    def __str__(self):
        return f"Task: {self.description}. ID#{self.id}. ETA: {self.eta}."