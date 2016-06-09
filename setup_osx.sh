pyver=3.5.1

brew update
brew outdated pyenv || brew upgrade pyenv
PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install $pyver -s

export PYENV_ROOT=/usr/local/opt/pyenv
export PATH=$PYENV_ROOT:$PATH
eval "$(pyenv init -)"

pyenv rehash
pyenv local $pyver
