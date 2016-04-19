# setup virtual environment
# this isn't strictly necessary on a disposable VM build
# but it means we can use this script also for local development/testing

pip install virtualenv
virtualenv venv
source venv/bin/activate

brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer
pip install -I Cython==0.23
CC=cc CXX=c++ USE_OSX_FRAMEWORKS=0 pip install kivy > kivy_install.txt

brew install pygame


pip install -r requirements.txt requirements-osx.txt

KEY_CHAIN=ios-build.keychain
security create-keychain -p travis $KEY_CHAIN
# Make the keychain the default so identities are found
security default-keychain -s $KEY_CHAIN
# Unlock the keychain
security unlock-keychain -p travis $KEY_CHAIN
# Set keychain locking timeout to 3600 seconds
security set-keychain-settings -t 3600 -u $KEY_CHAIN


cd installer
python -m PyInstaller  -y --windowed --icon=resources/particle.icns osx_onefile.spec
rm -rf particle_system_firmware.app
pushd dist
signid=$CODESIGNID
codesign -s $signid particle_system_firmware.app/Contents/MacOS/particle_system_firmware
codesign -s $signid --force --verify --verbose particle_system_firmware.app
rm particle_system_firmware.zip
zip -r particle_system_firmware.zip particle_system_firmware.app

sudo spctl -a -v particle_system_firmware.app
popd 






