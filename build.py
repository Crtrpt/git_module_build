# !/usr/bin/env python

import subprocess
import json
import os

build_file = open("build.json", "r")

if not os.path.exists("build.lock"):
    open("build.lock", "w").close()
build_lock_file = open("build.lock", "r+")


def get_object_last_commit_hash(obj):
    cmd = "git log -1 --format=%H " + obj
    hash = subprocess.check_output(cmd).decode("utf-8").replace("\n", "")
    return hash


build_file_json = json.loads(build_file.read())

try:
    build_lock_json = json.loads(build_lock_file.read())
except (Exception) as e:
    build_lock_json = build_file_json

# build_file_json.

for i, m in enumerate(build_file_json['module']):
    build_lock_last_commit = ""
    try:
        build_lock_last_commit = build_lock_json['module'][m]['last_commit']
    except Exception as e:
        build_lock_json['module'].update({m: build_file_json['module'][m]})
    last_commit = get_object_last_commit_hash(build_file_json['module'][m]['source'])
    if build_lock_last_commit == last_commit:
        print("nothing")
    else:
        if "last_commit" in build_lock_json['module'][m]:
            build_lock_json['module'][m]['last_commit'] = last_commit
        else:
            build_lock_json['module'][m].update({"last_commit": last_commit})
        print("do build")

build_lock_file.seek(0)
build_lock_file.truncate(0)
build_lock_file.write(json.dumps(build_lock_json))

build_file.close()
build_lock_file.close()
# print(build_file_json['module'])
