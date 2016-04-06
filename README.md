
## Features

- available as CLI and GUI
- cross platform - Windows, OSX, Linux, (potentially Android, iOS also)
- automatically detects devices when they are connected
- ymodem client implementation
- ymodem server implementation
- handles flashing multiple files and the ensuing device resets
- progress notification spans multiple flashes


## Roadmap

- DONE: multi file flash
- DONE: composite progress notification
- DONE: PoC console app to flash to a real device
- DONE: threading for app/UI separation
- DONE: gui app to flash to the device
- DONE: hide button when it's not needed - move widgets offscreen that aren't needed
- DONE: reveal progress bar when it's needed
- DONE: center device image
- DONE: white background
- DONE: particle logo
- DONE: fade in/out device on connection change
- DONE: text displaying device type / port
- DONE: derived properties for updating and other state
- DONE: different button colors for different states
- DONE: on last flash, don't go to complete until the device has rebooted
- DONE: Capture exceptions on the app thread and propagate to UI thread
- DONE: Device text / image pulled from Device config
- DONE: make ymodem more robust to any remaining data in the buffer sent over serial
- DONE: work around USB unreliability in 0.4.9 with large packets
- DONE: Install Serial driver on Windows if needed using either windows standard command line tools or libdwi
- DONE: build a small EXE that installs our certificate to the trusted certificate store. This exe is combined into an installer which is run silently.
- DONE: sign executable/package on OSX and Windows 
- DONE: add Particle icon to packaged executable
- DONE: add Particle icon to launched App
- DONE: busy spinner when progress doesn't update

- Intro page? - tell the user what the tool does. next button swipes to flash page
- Complete page? - page when update is complete. Helps the user have closure - process is done.
    Back button to flash more devices. Close button to close the app.


## Test plan

- device initially listening
- device initially connecting to the cloud
- electron, SIM card removed

### Testing Driver Installation

(Windows only)

Connect the device via USB, then right click and choose uninstall to remove the driver.
Launch "regedit", and delete the key HKLM/Software/Particle/drivers. This will ensure the drivers are installed
on next startup.  Unplug the device and plug in again to refresh the driver status.

Now launch the device updater, and it should install the drivers (with a UAC prompt) and the device automatically detected.


## Todo before Release
- propagate exceptions on actor thread via callback (DONE?)
- ymodem from listening mode
- Add exception handler for app that displays a popup then exits.


## Rough setup notes

- DONT:: install kivy - https://kivy.org/docs/installation/installation-osx.html#using-the-kivy-app
- test by typing `kivy`, then `import kivy` in the REPL
- eh, cannot use Kivy.app because the dlls include @import_path/SDL2_ttf etc.. which fails to work when packaged as an installer.

test the app - `kivy main.py`

Python 3.4

Instead, have to manually install
virtualenv -p /usr/bin/python3.4 venv
source venv/bin/activate

On windows, requires OpenGL 2.0 (found out that this isn't supported on VirtualBox with Windows 8 Guest. Upgraded to Windows 10.)

brew tap Homebrew/python
brew update



brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
pip install -I Cython==0.23
CC=cc CXX=c++ USE_OSX_FRAMEWORKS=0 pip install kivy

brew install pygame

pip install PyInstaller


https://twistedpairdevelopment.wordpress.com/2012/03/19/installing-kivy-on-os-x-from-pip-and-homebrew/


https://groups.google.com/forum/#!msg/kivy-users/MmhoPHBzLhk/oDnxOprSZ5UJ


Android

Need to use Linux - I used Ubuntu 14.0.3

- sudo apt-get install python3, python-pip3, git
- pip3 install virtualenv
- virtualenv py3
- source py3/bin/activate
- git clone https://github.com/spark/device-updater
- pip install -r device-updater/src/requirements.txt
- pip install git+https://github.com/kivy/python-for-android.git
- download python3crystax https://www.crystax.net/en/download
- install android SDK version 15

- installing build dependencies
- cd install && pip install -r requirements.txt && CC=/usr/bin/gcc python2 -m pip install -r requirements_system_python.txt
- ^^ dmgbuild requires python2

https://kivy.org/planet/2016/01/python-for-android-now-supports-python-3%C2%A0apks/


## Silentl Install of Windows Drivers

- the driver installer is built using inno setup, from the file src/resources/windows/*.iss

- the main app checks if HKLM/Software/Particle/drivers/serial/version matches the expected version. If not present or lower, the driver installer is launched.
- the driver installer requires elevated permissions (so the user is presented with a UAC prompt)
- the remainer of the isntaller is silent
- it contains trustedcertstore.exe that contains the particle certificate and adds that certificate to the trusted issuers - this stops windows from prompting the user on each signed driver install
- the installer copies the trustedcertstore.exe and all the drivers to a subfolder under program files.
- the installer launches trustedstore.exe to register particle certificate as trusted
- the installer uses pnputil -i -a %driver% to install each driver
- the installer exits 

## Known Quirks

When the Windows drivers are first installed, if the device was already connected, then the device should be disconnected and reconnected for it to be detected by the application.

For this reason, it's best to connect the device after starting the application.


 
