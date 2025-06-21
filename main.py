import json  # For reading and writing to a JSON file
from datetime import datetime, timedelta  # For working with dates and times
import os  # To check if the file exists

# File where tasks will be stored
TASKS_FILE = "tasks.json"


# Function to load tasks from the file

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []  # If file doesn't exist, return empty list
    with open(TASKS_FILE, "r") as file:
        return json.load(file)


# Function to save tasks to the file

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


# Function to get the next task ID

def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task["ID"] for task in tasks) + 1


# Function to check and update overdue tasks

def update_overdue(tasks):
    today = datetime.today().date()
    for task in tasks:
        if task["Status"] == "Pending":
            due = datetime.strptime(task["Due Date"], "%Y-%m-%d").date()
            if due < today:
                task["Status"] = "Overdue"


# Function to add a new task

def add_task(tasks):
    print("\n--- Add New Task ---")
    title = input("Title: ")
    desc = input("Description: ")
    due = input("Due Date (YYYY-MM-DD): ")
    priority = input("Priority (High/Medium/Low): ").capitalize()

    new_task = {
        "ID": get_next_id(tasks),
        "Title": title,
        "Description": desc,
        "Due Date": due,
        "Priority": priority,
        "Status": "Pending",  # Default status
        "Created At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Completed At": ""
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print("Task added successfully!")


# Function to mark a task as completed

def mark_completed(tasks):
    print("\n--- Mark Task as Completed ---")
    task_id = int(input("Enter Task ID: "))
    for task in tasks:
        if task["ID"] == task_id:
            task["Status"] = "Completed"
            task["Completed At"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            print("Task marked as completed!")
            return
    print("Task not found.")



# Function to delete a task

def delete_task(tasks):
    print("\n--- Delete Task ---")
    task_id = int(input("Enter Task ID to delete: "))
    updated_tasks = [task for task in tasks if task["ID"] != task_id]
    if len(updated_tasks) == len(tasks):
        print("Task not found.")
    else:
        save_tasks(updated_tasks)
        print("Task deleted successfully!")


# Function to show all tasks

def display_tasks(tasks):
    update_overdue(tasks)
    tasks.sort(key=lambda task: (priority_order(task["Priority"]), task["Due Date"]))

    print("\n--- All Tasks ---")
    for task in tasks:
        print(f"[{task['ID']}] {task['Title']} - {task['Priority']} - {task['Status']}")
        print(f"Due: {task['Due Date']} | Created: {task['Created At']} | Completed: {task['Completed At']}")
        print(f"Description: {task['Description']}")
        print("-" * 40)



# Helper function to sort by priority

def priority_order(priority):
    return {"High": 1, "Medium": 2, "Low": 3}.get(priority, 4)


# Function to filter tasks based on criteria


def filter_tasks(tasks):
    print("\n--- Filter Tasks ---")
    print("1. Pending\n2. Completed\n3. Due Today\n4. Due Tomorrow\n5. Overdue")
    choice = input("Select option: ")

    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)
    filtered = []

    if choice == "1":
        filtered = [t for t in tasks if t["Status"] == "Pending"]
    elif choice == "2":
        filtered = [t for t in tasks if t["Status"] == "Completed"]
    elif choice == "3":
        filtered = [t for t in tasks if t["Due Date"] == str(today)]
    elif choice == "4":
        filtered = [t for t in tasks if t["Due Date"] == str(tomorrow)]
    elif choice == "5":
        filtered = [t for t in tasks if t["Status"] == "Overdue"]

    if filtered:
        display_tasks(filtered)
    else:
        print("ℹNo tasks found for the selected filter.")


# Main program loop

def main():
    tasks = load_tasks()
    update_overdue(tasks)

    while True:
        print("\n=== TO-DO LIST MENU ===")
        print("1. Add Task")
        print("2. Mark Task as Completed")
        print("3. Delete Task")
        print("4. View All Tasks")
        print("5. Filter Tasks")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_task(tasks)
            tasks = load_tasks()
        elif choice == "2":
            mark_completed(tasks)
            tasks = load_tasks()
        elif choice == "3":
            delete_task(tasks)
            tasks = load_tasks()
        elif choice == "4":
            display_tasks(tasks)
        elif choice == "5":
            filter_tasks(tasks)
        elif choice == "0":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


# Run the program

if __name__ == "__main__":
    main()
