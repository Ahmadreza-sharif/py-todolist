import click
import os
import redis

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379,
                           db=0, decode_responses=True, password='secret')


@click.group()
def cli():
    pass


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


@cli.command()
def addTask():
    clearScreen()
    click.echo("Add task:")
    task = input("> ").strip()
    if task:
        redis_client.rpush('tasks', task)
        click.echo(f"Added task: {task}")
    else:
        click.echo("Task cannot be empty.")
    input("\nPress Enter to continue...")
    main_menu()


@click.command()
def updateTask():
    clearScreen()

    click.echo("List Of Task For Update:")

    tasks = redis_client.lrange('tasks', 0, -1)
    ids = []
    for i, task in enumerate(tasks, 1):
        click.echo(f"{i}. {task}")
        ids.append(i)

    click.echo("Which one do you want update?!")
    selectedTask = input('> ').strip()
    while not selectedTask.isdigit():
        click.echo("Please enter number!")
        selectedTask = input('> ').strip()

    while int(selectedTask) not in ids:
        click.echo("Task Doesn't Exists!")
        selectedTask = input('> ').strip()

    click.echo("So what is your new description?!")
    newDescription = input('> ').strip()

    redis_client.lset('tasks', int(selectedTask) - 1, newDescription)

    input("\nPress Enter to continue...")
    main_menu()


@click.command()
def deleteTask():
    clearScreen()

    click.echo("List Of Task For Delete:")

    tasks = redis_client.lrange('tasks', 0, -1)
    ids = []
    for i, task in enumerate(tasks, 1):
        click.echo(f"{i}. {task}")
        ids.append(i)

    click.echo("Which one do you want Delete?!")
    selectedTask = input('> ').strip()
    while not selectedTask.isdigit():
        click.echo("Please enter number!")
        selectedTask = input('> ').strip()

    while int(selectedTask) not in ids:
        click.echo("Task Doesn't Exists!")
        selectedTask = input('> ').strip()

    redis_client.delete('tasks', int(selectedTask) - 1)

    input("\nPress Enter to continue...")
    main_menu()


@click.command()
def listTask():
    clearScreen()
    tasks = redis_client.lrange('tasks', 0, -1)
    if tasks:
        click.echo("List of tasks:")
        for i, task in enumerate(tasks, 1):
            click.echo(f"{i}. {task}")
    else:
        click.echo("No tasks found.")
    input("\nPress Enter to continue...")
    main_menu()


def main_menu():
    clearScreen()
    click.echo("Welcome to the To-Do List CLI!")
    click.echo(
        "Available commands:\n List of tasks = [1]\n Add Task = [2]\n Update Task = [3]\n Delete Task = [4]\n exit = [0]\n")
    while True:
        command = input("> ").strip().lower()
        if command == "1":
            listTask()
        elif command == "2":
            addTask()
        elif command == "3":
            updateTask()
        elif command == "4":
            deleteTask()
        elif command == "0":
            click.echo("Exiting the CLI. Goodbye!")
            break
        else:
            click.echo(f"Unknown command: {
                       command}. Available commands: List of tasks = [1]\n Add Task [2]\n exit[0]\n ")


if __name__ == "__main__":
    main_menu()
