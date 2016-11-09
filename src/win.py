import os
import subprocess
from distutils.version import LooseVersion

import sys
from winreg import *

from gui import Gui, setup_working_dir


def needs_install(required_version):
    result = True
    try:
        aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
        aKey = OpenKey(aReg, r"Software\Particle\Drivers", 0, KEY_READ | KEY_WOW64_64KEY)
        qValue = QueryValueEx(aKey, r"Version")
        installed_version = qValue[0] if qValue else "0"
        result = LooseVersion(installed_version) < LooseVersion(required_version)
        print("installed driver version %s: required version %s" % (installed_version, required_version))
    except WindowsError as e:
        print(e)
    return result

"""
def install_driver():
    # add cert to store
    exe = 'resources/windows/trustcertregister.exe'
    subprocess.run(exe)
    install_inf_file("photon.inf")
    install_inf_file("electron.inf")


def install_inf_file(name):
    winpath = os.environ['WINDIR']

    try:
        pnputil = os.path.join(winpath, 'SYSNATIVE\\PNPUTIL.exe')
        subprocess.run(pnputil, '-1', '-a', name, shell=True)
    except Exception as e:
        print(e)
        try:
            pnputil = os.path.join(winpath, 'System32\\PNPUTIL.exe')
            subprocess.run(pnputil, '-1', '-a', name, shell=True)
        except Exception as e:
            print(e)
"""


current_drivers_version = "6.1.0.63"

def windows_setup():
    if needs_install(current_drivers_version):
        drivers_installer = "resources\windows\particle_drivers_{}.exe".format(current_drivers_version)
        print("launching", drivers_installer)
        subprocess.call([drivers_installer, "/S"], shell=True)

if __name__ == '__main__':
    setup_working_dir()
    windows_setup()
    Gui().run()
