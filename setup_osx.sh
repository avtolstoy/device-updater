pyver=3.5.1

brew update
brew outdated pyenv || brew upgrade pyenv

export PYENV_ROOT=/usr/local/opt/pyenv
export PATH=$PYENV_ROOT:$PATH
eval "$(pyenv init -)"

PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install $pyver -s

pyenv rehash
pyenv local $pyver
