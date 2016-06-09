# This script sets up the python environment
# When developing, this is typically only run once, and then install_osx.sh used thereafter.

pyver=3.5.1

brew update
brew outdated pyenv || brew upgrade pyenv

export PYENV_ROOT=/usr/local/opt/pyenv
export PATH=$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PYENV_ROOT:$PATH

eval "$(pyenv init -)"

PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install $pyver -s

pyenv rehash
pyenv global $pyver

echo "path is $PATH" 
which python
pyenv which python
