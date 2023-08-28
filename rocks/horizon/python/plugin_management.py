#!/usr/bin/env python3
# Copyright 2023 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from pathlib import Path

OS_DASHBOARD = Path("/usr/lib/python3/dist-packages/openstack_dashboard/")
ENABLED = OS_DASHBOARD / "enabled"
AVAILABLE = OS_DASHBOARD / "available"


def _get_plugin_files(plugin: str) -> list[str]:
    files = AVAILABLE / plugin
    if not files.exists():
        raise Exception(
            f"No plugin files at {str(files)!r}, is {plugin!r} a supported plugin?"
        )
    return files.read_text().splitlines()


def enable_plugin(plugin: str):
    files = _get_plugin_files(plugin)
    for file in files:
        enabled = ENABLED / file
        available = AVAILABLE / file
        if enabled.exists():
            continue
        if not available.exists():
            raise Exception(f"Plugin file {str(available)!r} does not exist")
        enabled.symlink_to(available)
        print(f"Enabled {file!r}")


def disable_plugin(plugin: str):
    files = _get_plugin_files(plugin)
    for file in files:
        enabled = ENABLED / file
        if not enabled.exists():
            continue
        enabled.unlink()
        print(f"Disabled {file!r}")


COMMANDS = {
    "enable": enable_plugin,
    "disable": disable_plugin,
}


def main(cmd: str, plugins: list[str]):
    command = COMMANDS.get(cmd)
    if not command:
        print(f"Unknown command {cmd!r}")
        sys.exit(1)

    for plugin in plugins:
        command(plugin)


def _usage():
    print("Usage: plugin_management.py <command> <plugin>...")
    print("Commands: " + ", ".join(COMMANDS.keys()))


if __name__ == "__main__":
    args = sys.argv[1:]
    if "-h" in args or "--help" in args:
        _usage()
    else:
        if len(args) < 2:
            _usage()
            sys.exit(1)
        cmd, *plugins = args
        main(cmd, plugins)
