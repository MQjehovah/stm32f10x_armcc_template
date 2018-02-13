# -*- coding:utf-8 -*-
__author__ = 'MQjehovah'

import os
import sys
import chardet
import argparse
import codecs


def explore(pathname):
    if not os.path.isdir(pathname):
        print(pathname + "is not a dir")
        return
    for i in os.listdir(pathname):
        i = os.path.join(pathname, i)
        if os.path.isfile(i):
            # if os.path.splitext(i)[1] == '.c':
            convert(i)
        else:
            explore(i)


def convert(filename):
    try:
        if not os.path.isfile(filename):
            print(filename + "is not a file")
            return
        with open(filename, "rb") as fp:
            content = fp.read()
            if content:
                ftype = chardet.detect(content).get("encoding")
                if not ftype in ["utf-8","ascii"]:
                    print("正在将%s从%s转换为utf8" % (filename, ftype))
                    codecs.open(filename, 'w', encoding='utf8').write(
                        content.decode(ftype, 'ignore'))
    except IOError as e:  # except:
        print("error")


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
        convert(args.file)
