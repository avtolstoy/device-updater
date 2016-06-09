# when runnign this for local development, you probably want to have a virtualenv already setup and activated

which python
pyenv which python
which pip
pyenv which pip

brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer
pip install -I Cython==0.23
CC=cc CXX=c++ USE_OSX_FRAMEWORKS=0 pip install kivy > kivy_install.txt

brew install pygame

python -m pip install -r requirements.txt -r requirements-osx.txt

# use the tag if available, otherwise fallback to the commit hash
VERSION="${TRAVIS_TAG:-${TRAVIS_COMMIT:-`date "+%F-%T"`}}"

pushd installer
./add_key.sh
./package.sh $VERSION 
popd

