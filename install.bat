
call venv/Scripts/activate.bat

REM pip install -I Cython==0.23
pip install -r requirements.txt
pip install -r requirements-win.txt

cd installer
package.bat
cd ..
 
