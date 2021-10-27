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
    method_name: str = m[1]
    method_args: str = m[2]
    p = r'=[^,)]+'
    method_args: str = re.sub(p, '', method_args)
    # if args.verbose is True:
    #     print(f"method name: {method_name}; method args: {method_args}")
    return method_name, method_args


print(f"Updating controller and manager for newly generated server...")
print(f"Processing controller: {args.controller}")
methods_in_controller: List[dict] = []
lines: List[str] = []
lines_total = None
model_includes_in_controller = []
with open(args.controller, "r") as file:
    lines: List[str] = file.readlines()
    lines = [line.rstrip() for line in lines]
    lines_total = len(lines)

    line_i: int = -1
    last_from_i = None
    first_def_i = None
    manager_import_found: bool = False
    manager_import: str = 'from openapi_server.managers.neo4j_manager import Neo4jManager'
    while True:
        line_i += 1
        #print(f"line[{line_i}]: {lines[line_i]}")
        if lines[line_i].find('from ') == 0:
            if lines[line_i].find('from openapi_server.models.') == 0:
                model_includes_in_controller.append(lines[line_i])
            last_from_i = line_i
            if lines[line_i].find(manager_import) == 0:
                manager_import_found = True
            continue
        if lines[line_i].find('def ') == 0:
            first_def_i = line_i
            break
    if last_from_i is None or first_def_i is None:
        print(f"ERROR: Unable to include manager")
        exit(1)
    if manager_import_found is False:
        lines[last_from_i+1: last_from_i+1] = [
            manager_import,
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
            method_args_list = method_args.split(', ')
            methods_in_controller.append({'name': method_name, 'args': method_args_list, 'found': False})
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
lines: List[str] = []
with open(args.manager, "r") as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    lines_total = len(lines)

    line_i: int = -1
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

    lines_total: int = len(lines)
    if args.verbose is True:
        print(f"lines in manager: {lines_total}")
    line_i = -1
    def_found: bool = False
    returns_replaced = 0
    method_name = None
    method_args = None
    while line_i < lines_total-1:
        line_i += 1
        if lines[line_i].find('    def ') == 0:
            #print(f"line[{line_i}]: {lines[line_i]}")
            method_name, method_args = break_method(lines[line_i])
            p = r': *[^,]+'
            method_args_only = re.sub(p, '', method_args, flags=re.IGNORECASE)
            method_args_list = method_args_only.split(', ')
            if method_args_list[0] == 'self':
                method_args_list = method_args_list[1:]
            if args.verbose is True:
                print(f"Method name: {method_name}; Arguments in manager: {method_args_list}")
            try:
                method = next(d for d in methods_in_controller if d['name'] == method_name)
                if args.verbose is True:
                    print(f"Found method in manager: {method}")
                diff = list(set( method_args_list) - set(method['args']))
                if len(diff) == 0:
                    method['found'] = True
                else:
                    print(f"ERROR: Not all arguments found in manager for method {method_name}. Argument in controller: {method['args']}. Arguments in manager: {method_args_list}")
            except StopIteration:
                pass
            continue
    count_methods_found = sum([1 for d in methods_in_controller if d["found"] is True])
    print(f"Count Methods Found: {count_methods_found} count methods total {len(methods_in_controller)}")
    if count_methods_found != len(methods_in_controller):
        print(f"ERROR: Manager methods do not match controller methods by name")
        exit(1)

with open(f"{args.manager}", "w") as file:
    file.writelines(line + '\n' for line in lines)

print("Done!")
