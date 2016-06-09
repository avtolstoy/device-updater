
call venv/Scripts/activate.bat

REM pip install -I Cython==0.23
pip install -r requirements.txt
pip install -r requirements-win.txt

SET VERSION=%APPVEYOR_REPO_TAG_NAME%
IF "%VERSION%"=="" SET VERSION=%APPVEYOR_REPO_COMMIT%

cd installer
package.bat %VERSION%
cd ..
 
