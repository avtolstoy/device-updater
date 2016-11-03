#!/usr/bin/env bash

# fail pipes and exit on failure
set -e
set -o pipefail

# Use version var if defined, or the first arg
VERSION="${VERSION:-$1}"
export VERSION

# ensure version is defined
if [ -z  "${VERSION}" ]; then
  echo "Error: VERSION is not defined."
  exit 1
fi

# fetch the app name and build a fully qualified name
source appname.sh
export fqname=$appname-$VERSION-osx
echo "Building $fqname"

# clear out the dist directory
rm -rf dist

# build the python installer
appname="$appname" fqname="$fqname" pyinstaller  -y --windowed --icon=resources/particle.icns osx_onefile.spec --clean

pushd dist
security unlock-keychain -p $XCODE_KEYCHAIN_PASSWORD $XCODE_KEYCHAIN
codesign -s $signid --keychain ~/Library/Keychains/$XCODE_KEYCHAIN $fqname.app/Contents/MacOS/$fqname
codesign -s $signid --keychain ~/Library/Keychains/$XCODE_KEYCHAIN --force --verify --verbose $fqname.app

mkdir ../../dist
zip -r ../../dist/$fqname.zip $fqname.app

sudo spctl -a -v $fqname.app

popd 

