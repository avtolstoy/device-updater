python -m PyInstaller  -y --windowed --icon=resources/particle.icns osx_onefile.spec
rm -rf particle_updater.app
pushd dist
signid="TNJ67X9MQD"
codesign -s $signid particle_updater.app/Contents/MacOS/particle_updater
codesign -s $signid --force --verify --verbose particle_updater.app
rm particle_updater.zip
zip -r particle_updater.zip particle_updater.app

sudo spctl -a -v particle_updater.app
popd 
