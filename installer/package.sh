#!/usr/bin/env bash
set -e
set -o pipefail

VERSION="${VERSION:-$1}"
export VERSION

if [ -z  "${VERSION}" ]; then
  echo "Error: VERSION is not defined."
  exit 1
fi

export appname=particle_device_upgrader
export fqname=$appname-$VERSION
echo "Building $fqname"

rm -rf dist

appname="$appname" fqname="$fqname" python -m PyInstaller  -y --windowed --icon=resources/particle.icns osx_onefile.spec

pushd dist
signid="TNJ67X9MQD"
codesign -s $signid $fqname.app/Contents/MacOS/$fqname
codesign -s $signid --force --verify --verbose $fqname.app

zip -r $fqname.zip $fqname.app

sudo spctl -a -v $fqname.app
popd 
