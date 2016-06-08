pyver=3.5.1

brew update
brew outdated pyenv || brew upgrade pyenv
PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install $pyver -s
pyenv rehash
pyenv local $pyver
