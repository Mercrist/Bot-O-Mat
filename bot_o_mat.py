from multiprocessing import Pool
from Task import Task
from Robot import *
from typing import List, Tuple
from tabulate import tabulate
from os import system, name
import random

def clear_screen() -> None:
    """Clears the screen from the CLI for easier presentation."""
    # Taken from: https://www.geeksforgeeks.org/clear-screen-python/
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")

def initialize_tasks() -> List[Tuple]:
    """Initializes and randomizes the
    list of tasks that the robots can undertake."""
    # (description, ETA, type that can complete the task)
    # None = any robot type can complete it
    possible_tasks = list([
        ("Do the dishes", 1000, RobotType.UNIPEDAL),
        ("Sweep the house", 3000, None),
        ("Do the laundry", 10000, None),
        ("Take out the recycling", 4000, RobotType.BIPEDAL),
        ("Make a sandwich", 7000, None),
        ("Mow the lawn", 20000, None),
        ("Rake the leaves", 18000, None),
        ("Give the dog a bath", 14500, RobotType.QUADRUPEDAL),
        ("Bake some cookies", 8000, None),
        ("Wash the car", 20000, RobotType.RADIAL),
        ("Buy some groceries", 30000, RobotType.BIPEDAL),
        ("Look for good Black Friday deals", 10000, None),
        ("Chase the house dog", 1000, RobotType.ARACHNID),
        ("Fly around the woods", 10000, RobotType.AERONAUTICAL)])
    random.shuffle(possible_tasks)  # randomize task selection
    return possible_tasks

def assign_tasks(robots: List[Robot], tasks: List[Task]) -> None:
    """Assigns robots to 5 tasks
    from a given list of tasks that can be completed."""
    # Assigns 5 tasks per robot
    for robot in robots:
        for _ in range(5):
            desc, eta, rob_type = random.choice(tasks)
            task = Task(desc, eta, rob_type)
            robot.task_list.append(task)

def generate_leaderboard(robots: List[Tuple]) -> None:
    """Tabulates a leaderboard showing
    the best performing robots. Robots are
    sorted based on the completion time for
    each task. More tasks completed in less
    time will net a robot a higher position
    on the leaderboard. This is calculated as
    #tasks performed/total task execution time.
    Throughput is measured in minutes to get a
    better approximation of how many tasks
    are completed in that amount of time. Also
    represented as an integer since tasks can't be
    partially completed."""
    # Sort robots based on number of tasks completed/time
    leaderboard = []
    for robot in robots:
        throughput = robot.tasks_completed/(robot.elapsed/60)
        leaderboard.append((throughput, robot))  # tuple to sort based on throughput
    leaderboard.sort(key=lambda x: x[0], reverse=True) # sort in descending order

    # Make the table: Robot Name | Robot Type | #Tasks completed | Time taken (s) | Throughput (#tasks/min)
    leaderboard_table = []
    position = 1 # position on the table
    for throughput, robot in leaderboard:
        time_taken = f"{robot.elapsed:.2f}"
        throughput = int(throughput)
        leaderboard_table.append([str(position) + ". " + robot.name, robot.robot_type,
                                  robot.tasks_completed, time_taken, throughput])
        position += 1
    # Format and print the table
    headers = ["Name", "Type", "Tasks Completed", "Time Taken (s)", "Est. Throughput (tasks/min)"]
    print(tabulate(leaderboard_table, headers=headers, tablefmt="heavy_outline"))

def main():
    # Randomly select tasks from a (randomized) preset list of tasks
    clear_screen()
    tasks = initialize_tasks()
    robots = []

    # Main loop begins
    print("Welcome to BOT-O-MAT!\n---------------------")
    print("In this CLI program, several bots will simulate chores from a list of tasks.")
    print("You must first select the desired number of robots.")
    num_bots = 0
    MAX_BOTS = 10  # put a cap on the number of bots that can run
    while num_bots < 1 or num_bots > MAX_BOTS:
        try:
            num_bots = int(input("Enter the desired number of bots to create: "))
        except:
            num_bots = 0

        if num_bots < 1:
            print("Invalid, need to create at least one robot.")

        elif num_bots > MAX_BOTS:
            print("Invalid, creating an excessive number of robots is strongly discouraged.")

    print("\nPerfect, time to initialize the bots!")
    print(f"Robots are created based on both a name and type. The supported types are: ")
    print(f"Robot Types\n-----------")
    for rob_type in RobotType:
        print(rob_type.value)

    while num_bots > 0:
        robot_name = input(f"\nSelect a name for Robot#{len(robots)+1}: ")
        robot_type = input(f"Select a robot type from the list above for Robot#{len(robots)+1}: ")
        try:
            robot = Robot(robot_type, robot_name)
        except Exception as e:
            print(e)
        else:
            robots.append(robot)
            num_bots -= 1

    # Assigns tasks before processing them
    assign_tasks(robots, tasks)
    clear_screen()
    print("Below are the robots and their assigned tasks:")
    for robot in robots:
        print(robot)
        for task in robot.task_list:
            print(task)
        print("\n")
    input("Press any key to continue and begin work...")
    clear_screen()

    # Main loop of processing the divided work
    # Each robot is a process: fully parallelized at the cost of requiring more memory
    temp_results = []  # can only access values after all processes finish
    process_pool = Pool(len(robots)) # For data parallelism
    for robot in robots:
        temp_results.append(process_pool.apply_async(robot.run_tasks))
    process_pool.close() # Stops accepting new processes
    process_pool.join()  # Waits for processes to finish
    input("\nPress any key to view the results screen...")

    robot_results = []
    for res in temp_results:
        robot_results.append(res.get())  # get results of parallelization
    # Show the leaderboard
    clear_screen()
    generate_leaderboard(robot_results)
    retry = input("\nRobots finished their duty! Enter 'Y' to play again: ")
    if type(retry) != str:
        return "n"
    return retry.lower()

if __name__ == "__main__":
    retry = "y"
    while retry == "y":
        retry = main()
