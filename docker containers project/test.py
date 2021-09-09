import docker
client = docker.from_env()
client.containers.run("project", "Wordcount /c/shareddata/in/file2.txt /c/shareddata/out/")
# print(client.containers.list())
