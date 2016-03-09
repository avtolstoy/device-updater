python -m PyInstaller  -y --windowed --icon=resources/particle.icns osx_onefile.spec
rm -rf particle_system_firmware.app
pushd dist
signid="TNJ67X9MQD"
codesign -s $signid particle_system_firmware.app/Contents/MacOS/particle_system_firmware
codesign -s $signid --force --verify --verbose particle_system_firmware.app
rm particle_system_firmware.zip
zip -r particle_system_firmware.zip particle_system_firmware.app

sudo spctl -a -v particle_system_firmware.app
popd 
