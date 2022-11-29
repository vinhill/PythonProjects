import os
import re

def extract_packagename(line):
    reg_fi = r"\Afrom (?P<name>[A-Za-z0-9_]*).* import .*"
    match = re.search(reg_fi, line)
    if match:
        return match.group("name")
        
    reg_i = r"\Aimport (?P<name>[A-Za-z0-9_]*).*"
    match = re.search(reg_i, line)
    if match:
        return match.group("name")

def process_line(filename, line, searchfor, packages):
    pckg = extract_packagename(line)
    if pckg:
        packages.add(pckg)
        if pckg in searchfor:
            print((filename, line))

if __name__ == "__main__":
    packages = set()

    searchfor = input("Which packages should specifically be highlighted? ")
    where = input("Where to search? I.e. ./MA Project/ ")

    for root, dirs, files in os.walk(where, topdown=False):
        for filename in files:
            f = open(root + "/" + filename, "r", encoding="utf8", errors="ignore")
            for line in f:
                if "import" in line:
                    process_line(root + "/" + filename, line, searchfor, packages)
            f.close()

    for pckg in packages:
        print(pckg)