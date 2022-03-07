import yaml;

with open("./commands.example.yml", "r") as stream:
    user_commands = yaml.safe_load(stream);
    print(user_commands);
    for command in user_commands["commands"]:
        print(f"{command['title']} {command['description']}");
