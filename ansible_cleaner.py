import os
import sys

filename, file_extension = os.path.splitext(sys.argv[1])
filename += "-cleaned"
fout = open(filename + file_extension, 'w')

ansible = open(os.path.join(sys.argv[1])).readlines()

last_keyword = "VALUE"
last_keyword_stripped = "VALUE"
i = 0
for line in ansible:
    i += 1
    old = line
    if line.startswith("BREAKS HERE"):
        last_keyword = "VALUE"
        last_keyword_stripped = "VALUE"
        print("BREAKS HERE", file=fout)
        continue
    if "#" in line:
        line = line.split("#")[0]
    line = line[1:]
    line = line.replace("{", "")
    line = line.replace("}", "")
    if not line.strip():
        continue
    sides = line.split(":")
    if len(sides) > 1:
        left = sides[0]
        right = ":".join(sides[1:])
        if i == 4257:
            print(repr(left))
        if left.strip() == "module":
            pass
        elif "\"" in right or "'" in right:
            right = "VAR"
        elif not right.strip():
            right = ""
        else:
            right = left.upper().strip()
            if right.startswith("- "):
                right = right[2:]
        line = ": ".join([left, right])
        last_keyword = left
        last_keyword_stripped = left.strip()
    elif "-" in line:
        if "\"" in line or "'" in line:
            line = "- VAR"
        else:
            elem = last_keyword.split(last_keyword_stripped)
            line = elem[0] + "- " + last_keyword_stripped.upper()
    else:
        line = "VALUE"
    print(line, file=fout)
