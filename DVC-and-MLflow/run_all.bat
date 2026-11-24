@echo off
REM Run from inside the project folder containing prepare_data.py and train.py
REM Usage (Command Prompt):  run_all.bat

python -m pip install dvc mlflow scikit-learn pandas pyyaml || goto :error

REM ---------- Initialisation (DVCtutorial.docx) ----------
git init || goto :error
dvc init || goto :error
git commit -m "Initialize DVC" || goto :error

REM Commit the scripts so they exist at every tag
git add prepare_data.py train.py || goto :error
git commit -m "Add scripts" || goto :error
for /f "delims=" %%i in ('git rev-parse --abbrev-ref HEAD') do set BRANCH=%%i

REM ---------- Version 1 of the data ----------
python prepare_data.py 1 || goto :error
dvc add data/train.csv || goto :error
git add data/train.csv.dvc data/.gitignore || goto :error
git commit -m "Add version 1 of data" || goto :error
git tag -a "v1.0" -m "Data version 1.0" || goto :error

REM ---------- Version 2 of the data ----------
python prepare_data.py 2 || goto :error
dvc add data/train.csv || goto :error
git add data/train.csv.dvc || goto :error
git commit -m "Update data to version 2" || goto :error
git tag -a "v2.0" -m "Data version 2.0" || goto :error

REM ---------- Train on each version (double checkout) ----------
git checkout v1.0 || goto :error
dvc checkout || goto :error
python train.py || goto :error

git checkout v2.0 || goto :error
dvc checkout || goto :error
python train.py || goto :error

REM Return to the latest state
git checkout %BRANCH% || goto :error
dvc checkout || goto :error

echo.
echo Done. Now run:  mlflow ui   and open http://localhost:5000
exit /b 0

:error
echo.
echo FAILED at the step above. Fix the error and see the notes before re-running.
exit /b 1
