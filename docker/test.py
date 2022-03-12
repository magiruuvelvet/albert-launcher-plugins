import docker;

client = docker.from_env();

images = client.images.list();

for image in images:
    print(image.tags, image.id);

print("===");

containers = client.containers.list(all=True);

def sortByRunning(status: int) -> int:
    if status == "running": return 0;
    else: return 1;
containers.sort(key=lambda container: sortByRunning(container.status));

for container in containers:
    print(container.name, container.attrs["Config"]["Image"], container.status);
