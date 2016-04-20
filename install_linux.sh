curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
pyenv update

pyenv install 3.4.3
pyenv rehash
pyenv local 3.4.3

git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
pyenv virtualenv kivy
pyenv activate kivy

pip install Cython==0.23 > cython.txt

pip install -r requirements.txt

