# -*- coding:utf-8 -*-

'''
stm32-cli
'''
__author__ = 'MQjehovah'

import os
import sys
import re
import argparse
import time


def main():
    pass


def render(tpl, a):
    pass


def create_func(args):
    if args.m:
        def render(match):
            str = match.group(1)
            if str == 'name':
                return args.name
            elif str == 'NAME':
                return args.name.upper()
            elif str == 'date':
                return time.strftime("%Y/%m/%d")
            else:
                return str
        if not args.o:
            args.o = os.getcwd()
        if not os.path.exists(args.o):
            os.mkdir(args.o)
        all_text = open(sys.path[0] + '/templates/template.c').read()
        all_text = re.sub("{{(\w+)}}", render, all_text)
        file_ptr = open('%s/%s.c' % (args.o, args.name), 'w')
        file_ptr.write(all_text)
        file_ptr.close()
        all_text = open(sys.path[0] + '/templates/template.h').read()
        all_text = re.sub("{{(\w+)}}", render, all_text)
        file_ptr = open('%s/%s.h' % (args.o, args.name), 'w')
        file_ptr.write(all_text)
        file_ptr.close()


def module_func(args):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='stm32-cli', description='stm32 develop tool')
    parser.add_argument('-t', help='for arg test')
    parser.set_defaults(func=main)
    subparsers = parser.add_subparsers(title='subcommands', help='commands')
    # 创建子命令
    create_parser = subparsers.add_parser('create', help='create sub command')
    create_parser.add_argument("name", help='project name')
    create_parser.add_argument('-p', help='clone to path')
    create_parser.add_argument(
        '-m', help='create a stm32 module', action="store_true")
    create_parser.add_argument('-o', help='out path')
    create_parser.set_defaults(func=create_func)
    # 运行子命令
    run_parser = subparsers.add_parser(
        'run', help='run a script defined in mq.json')
    run_parser.add_argument('command', help='create a model')
    run_parser.set_defaults(func=module_func)

    args = parser.parse_args()
    args.func(args)
