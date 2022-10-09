import os
from colorama import Fore
from geoip import geolite2


def ask_name():
    name = input("User IGN: ")
    start(name)


def start(name: str):
    print(Fore.CYAN + "Loading log files")
    main = os.listdir('logs/main')
    print(Fore.LIGHTGREEN_EX + "Loaded main logs")

    ips = []

    search_logs(main, ips, name, "main")

    print(Fore.WHITE + "---------------------------")
    print(Fore.YELLOW + "Found a total of " + Fore.WHITE + str(len(ips)) + " IPs")
    print(Fore.WHITE + "---------------------------")
    if len(ips) > 0:
        ip_file = open(f"{name}.txt", "w")
        ip_file.write(f"IPs of {name}:\n\n" + "\n".join(ips))
        ip_file.close()


def search_logs(folder: list[str], ips: list[str], name: str, server: str):
    print(Fore.CYAN + f"Starting to read {server.upper()} logs")
    for file in folder:
        try:
            f = open(f"logs/{server}/{file}")
            lines = f.readlines()
            for line in lines:
                words = line.split(" ")
                find_name(name, words, ips, server)

            f.close()
        except (UnicodeDecodeError, KeyError):
            continue
    print(Fore.CYAN + f"Finished reading {server.upper()} logs")


def find_name(name: str, words: list[str], ips: list[str], server: str):
    for word in words:

        if name not in word:
            continue

        if "[" not in word or "]" not in word or "GameProfile" in word:
            continue
        ip = word[word.find("[") + 1:word.find("]")][1:]

        if ip in ips:
            continue
        no_port = ip[0:ip.find(":")]
        match = geolite2.lookup(no_port)

        if match is not None:
            full_info = match.get_info_dict()
            country = full_info["country"]["names"]["en"]
            ips.append(f"{ip} : {country}")
        else:
            ips.append(ip)
        print(Fore.LIGHTMAGENTA_EX + f"Name found in {server} " + Fore.LIGHTYELLOW_EX +
              "(" + Fore.WHITE + ip + Fore.LIGHTYELLOW_EX + ")")


if __name__ == '__main__':
    ask_name()
