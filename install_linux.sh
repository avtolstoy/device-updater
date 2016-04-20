sudo apt-get install -y \
    build-essential \
    python3-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev

curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

export PATH="/home/travis/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv update

pyenv install 3.4.3
pyenv rehash
pyenv local 3.4.3

git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
pyenv virtualenv kivy
pyenv activate kivy

pip install Cython==0.23 > cython.txt

pip install -r requirements.txt

cd installer
python -m PyInstaller  -y --windowed linux_onefile.spec
