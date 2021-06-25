#
# Copyright 2018-2021 Elyra Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import subprocess
import os
import sys
import argparse

from abc import ABC, abstractmethod
from packaging import version
from pathlib import Path
from tempfile import TemporaryFile
from typing import Optional, Any, Type, TypeVar
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlunparse

# Inputs and Outputs separator character.  If updated,
# same-named variable in _notebook_op.py must be updated!
INOUT_SEPARATOR = ';'

parser = argparse.ArgumentParser (description="'bootstrapper.py' argument parser.", \
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter )

parser.add_argument ('--work-dir', default="/examples", help="Path for base container working directory.")

parser.add_argument ('--file-name', default="Train.py", help="Python Training Script file name.")

# parser.add_argument ()

class PythonFileOp () :
    ''' Perform Python File Operation. '''

    def execute(self, filename="Train.py") -> None :
        subprocess.run (['python3', filename], check=True)

def package_list_to_dict (filename: str) -> dict:
    
    package_dict = {}

    with open (filename) as f_base_package :
        for line in f_base_package :
            if line[0] != '#' :
                if " @ " in line:
                    package_name, package_version = line.strip('\n').split(sep=" @ ")
                elif "===" in line:
                    package_name, package_version = line.strip('\n').split(sep="===")
                else:
                    package_name, package_version = line.strip('\n').split(sep="==")
            
                package_dict [package_name] = package_version

    return package_dict


def package_install () :

    platform_packages = package_list_to_dict ("requirements-platform.txt")
    current_packages = package_list_to_dict ("requirements-current.txt")

    to_install_list = []
    for package, version in platform_packages.items() :
        if package in current_packages :
            # Handling something
            pass

        else :
            to_install_list.append (package + "==" + version)

    if to_install_list :
        to_install_list.append ('--no-cache-dir')

        subprocess.run([sys.executable, '-m', 'pip', 'install'] + to_install_list, check=True)
    
    with open ("InstallationEnd.txt", "wt") as f :
        f.writelines("Installation End.")

def main () :
    args = parser.parse_args()

    package_install ()

    PythonFileOp.execute (args.file_name)



if __name__ == "__main__" :
    main ()
