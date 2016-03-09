python -m PyInstaller  -y --windowed --icon=resources/particle.icns osx_onefile.spec
dmg(){
  hdiutil create -fs HFS+ -srcfolder "$1" -volname "$2" "$2.dmg"
}
pushd dist

# http://stackoverflow.com/questions/96882/how-do-i-create-a-nice-looking-dmg-for-mac-os-x-using-command-line-tools
# how to programmatically set the dmg icon


# build the DMG file from the .app dir
dmg particle_updater.app particle_updater


# sign it
codesign -s "TNJ67X9MQD" particle_updater.dmg



popd
