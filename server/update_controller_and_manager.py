#!/usr/bin/env python

import argparse
import re
from typing import List


class RawTextArgumentDefaultsHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawTextHelpFormatter
):
    pass


# https://docs.python.org/3/howto/argparse.html
parser = argparse.ArgumentParser(
    description='Update the controller and manager as a result of a new build of the server',
    formatter_class=RawTextArgumentDefaultsHelpFormatter)
parser.add_argument("-c", '--controller', type=str, default='./openapi_server/controllers/default_controller.py',
                    help='the controller to update')
parser.add_argument("-m", '--manager', type=str, default='./openapi_server/managers/neo4j_manager.py',
                    help='the manager to update')
parser.add_argument("-v", "--verbose", action="store_true",
                    help='increase output verbosity')

args = parser.parse_args()


def break_method(line: str):
    m = re.match(r' *def ([a-z_]+)\(([^)]+)\)', line)
    method_name = m[1]
    method_args = m[2]
    p = r'=[^,)]+'
    method_args = re.sub(p, '', method_args)
    # if args.verbose is True:
    #     print(f"method name: {method_name}; method args: {method_args}")
    return method_name, method_args


print(f"Processing controller: {args.controller}")
methods_in_controller: List[dict] = []
lines = None
lines_total = None
model_includes_in_controller = []
with open(args.controller, "r") as file:
    lines: List[str] = file.readlines()
    lines = [line.rstrip() for line in lines]
    lines_total = len(lines)

    line_i = -1
    last_from_i = None
    first_def_i = None
    while True:
        line_i += 1
        #print(f"line[{line_i}]: {lines[line_i]}")
        if lines[line_i].find('from ') == 0:
            if lines[line_i].find('from openapi_server.models.') == 0:
                model_includes_in_controller.append(lines[line_i])
            last_from_i = line_i
            continue
        if lines[line_i].find('def ') == 0:
            first_def_i = line_i
            break
    if last_from_i is None or first_def_i is None:
        print(f"ERROR: Unable to include manager")
        exit(1)

    lines[last_from_i+1: last_from_i+1] = [
        'from openapi_server.managers.neo4j_manager import Neo4jManager',
        '',
        '',
        'neo4jManager = Neo4jManager()'
    ]

    lines_total = len(lines)
    if args.verbose is True:
        print(f"lines in controller: {lines_total}")
    line_i = -1
    def_found = False
    returns_replaced = 0
    method_name = None
    method_args = None
    while line_i < lines_total-1:
        line_i += 1
        #print(f"line[{line_i}]: {lines[line_i]}")
        if lines[line_i].find('def ') == 0:
            method_name, method_args = break_method(lines[line_i])
            methods_in_controller.append({'name': method_name, 'args': method_args, 'found': False})
            def_found = True
            continue
        if lines[line_i].find("    return 'do some magic!'") == 0:
            if def_found is False:
                print(f"ERROR: Unable to find def associated with return")
                exit(1)
            if method_name is None or method_args is None:
                print(f"ERROR: Unable to parse def line")
                exit(1)
            lines[line_i] = f"    return neo4jManager.{method_name}({method_args})"
            returns_replaced += 1
            def_found = False
            method_name = None
            method_args = None
            continue

if args.verbose is True:
    print(f"Done reading: {args.controller}; lines in file {lines_total}; returns replaced: {returns_replaced}")
    print(f"Method names in controller: {list(map(lambda m : m['name'], methods_in_controller))}")
    #print(f"Model includes in controller: {model_includes_in_controller}")

with open(f"{args.controller}", "w") as file:
    file.writelines(line + '\n' for line in lines)


print(f"Processing manager: {args.manager}")
lines = []
with open(args.manager, "r") as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    lines_total = len(lines)

    line_i = -1
    first_from_i = None
    last_from_i = None
    while True:
        line_i += 1
        #print(f"line[{line_i}]: {lines[line_i]}")
        if lines[line_i].find('from openapi_server.models.') == 0:
            if first_from_i is None:
                first_from_i = line_i
            last_from_i = line_i
        else:
            if first_from_i is not None:
                break
    lines[first_from_i:last_from_i+1] = model_includes_in_controller

    lines_total = len(lines)
    if args.verbose is True:
        print(f"lines in manager: {lines_total}")
    line_i = -1
    def_found = False
    returns_replaced = 0
    method_name = None
    method_args = None
    while line_i < lines_total-1:
        line_i += 1
        if lines[line_i].find('    def ') == 0:
            #print(f"line[{line_i}]: {lines[line_i]}")
            method_name, method_args = break_method(lines[line_i])
            if args.verbose is True:
                print(f"Method name: {method_name}")
            try:
                found = next(d for d in methods_in_controller if d['name'] == method_name)
                if args.verbose is True:
                    print(f"Found method name in manager: {found}")
                # if found['args'].sort() != method_args.sort():
                #     print(f"ERROR: Not all arguments found in manager for method {method_name}. Argument in controller: {found['args']}. Arguments in manager: {method_args}")
                #     exit(1)
                found['found'] = True
            except StopIteration:
                pass
            continue
    count_methods_found = sum([1 for d in methods_in_controller if d["found"] is True])
    if args.verbose is True:
        print(f"Count Methods Found: {count_methods_found} count methods total {len(methods_in_controller)}")
    if count_methods_found != len(methods_in_controller):
        print(f"ERROR: Manager methods do not match controller methods by name")
        exit(1)

with open(f"{args.manager}", "w") as file:
    file.writelines(line + '\n' for line in lines)

print("Done!")
