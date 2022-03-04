import netifaces as ni;

print(ni.interfaces());

for i in ["wwan0", "eth0", "docker1"]:
    iface = ni.ifaddresses(i);
    if ni.AF_INET in iface:
        print(i + ":", iface[ni.AF_INET][0]["addr"]);
    else:
        print(i + ":", "DOWN");

query = "w";

for i in ni.interfaces():
    if i.startswith(query):
        print("match", i);
