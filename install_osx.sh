# setup virtual environment
# this isn't strictly necessary on a disposable VM build
# but it means we can use this script also for local development/testing

pip install virtualenv
virtualenv venv
source venv/bin/activate

echo "Virtual Env installed"
which python
pyenv which python

brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer
pip install -I Cython==0.23
CC=cc CXX=c++ USE_OSX_FRAMEWORKS=0 pip install kivy > kivy_install.txt

brew install pygame

pip install -r requirements.txt -r requirements-osx.txt

# use the tag if available, otherwise fallback to the commit hash
VERSION="${TRAVIS_TAG:-${TRAVIS_COMMIT:-`date "+%F-%T"`}}"

pushd installer
./add_key.sh
./package.sh $VERSION 
popd

