from threading import Thread
import re
import subprocess

kill = False
TASKS = []
global TOTAL_TASKS
COUNTER = 0

container_states = {
    "c1": "idle",
    "c2": "idle",
    "c3": "idle"
}


def main():
    process = subprocess.Popen(["powershell", "docker start c1 c2 c3"], stdout=subprocess.PIPE)
    result = process.communicate()[0]
    if result == b'c1\nc2\nc3\n':
        print("Containers are started => {C1, C2, C3}")

    # make a thread that listens to client inputs.
    t = Thread(target=handle_user)
    # start the thread
    t.start()

    # make a thread that assigns existing tasks to free containers.
    t = Thread(target=assign_task)
    # start the thread
    t.start()


def handle_user():
    user_input = ""
    while user_input != "exit":
        user_input = input("Enter operand and path of input file:\n")
        user_input = user_input.strip()
        if re.search("{(<.*>)+}", user_input) is None:
            print("wrong input!\nPlease try again.")
        else:
            user_input = re.findall("<.*?>", user_input)

            for i in user_input:
                yo = i.split(",")
                yo[0] = yo[0].replace("<", "").strip()
                yo[1] = yo[1].replace(">", "").strip()
                TASKS.append(yo)
            global TOTAL_TASKS
            TOTAL_TASKS = len(TASKS)


def assign_task():
    while True:
        if len(TASKS) != 0:
            free_container = ''
            for key in list(container_states.keys()):
                if container_states[key] == 'idle':
                    free_container = key
                    break
            if free_container != '':
                first_task = TASKS.pop(0)
                cmd_input_args = str(first_task[0]) + " " + str(first_task[1])
                # make a thread that runs a task on a container.
                t = Thread(target=run_command, args=(cmd_input_args, free_container))
                # start the thread
                t.start()
                change_container_status_running(free_container)
                print("task: " + str(first_task) + " assigned to: " + free_container)


# handle_user()
# print(tasks[0][0])
# print(tasks[0][1])
def change_container_status_running(containerName):
    container_states[containerName] = "running"


def change_container_status_idle(containerName):
    container_states[containerName] = "idle"


def run_command(command, container_name):
    process = subprocess.Popen(
        ["powershell", f"docker exec {container_name} python container-brain.py {command} /c/shareddata/out/ -c"],
        stdout=subprocess.PIPE)

    result = process.communicate()[0]
    print("task "+ str(command) + " which was assigned to container " + str(container_name) + " finished!!")
    #print(result)
    change_container_status_idle(container_name)
    global COUNTER
    COUNTER += 1
    if COUNTER == TOTAL_TASKS:
        print('All of your tasks executed Successfully.')


if __name__ == '__main__':
    main()

