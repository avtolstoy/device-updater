set PATH=%PYTHON%;%PYTHON%/scripts;%PATH%
pip install --disable-pip-version-check --user --upgrade pip
pip install virtualenv
virtualenv venv
call venv/Scripts/activate.bat

pip install -I Cython==0.23
pip install kivy==1.9.1
pip install pyinstaller==3.1.1
pip install pywin32==

cd installer
python -m PyInstaller -y --onefile win_onefile.spec
%SIGNTOOL_PATH%\signtool sign /v /f cert.p12 /p %cer_secret% /tr http://tsa.starfieldtech.com dist\particle_system_firmware.exe
cd ..
 
