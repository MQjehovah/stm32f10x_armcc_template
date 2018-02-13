import argparse
import os

def explore(pathname):
    if not os.path.isdir(pathname):
        print(pathname + "is not a dir")
        return
    for i in os.listdir(pathname):
        i = os.path.join(pathname, i)
        if os.path.isfile(i):
            if os.path.splitext(i)[1] == '.c' or os.path.splitext(i)[1] == '.h':
                os.system("@tool\\AStyle\\AStyle.exe --style=ansi --delete-empty-lines -n " + i)
        else:
            explore(i)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--path", help="path")
    parser.add_argument(
        "-f", "--file", help="file")
    args = parser.parse_args()
    if args.path:
        explore(args.path)
    if args.file:
        os.system(".\\tool\\AStyle\\AStyle.exe --style=ansi --delete-empty-lines -n " + args.file)
