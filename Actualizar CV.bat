@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  set "CV_PYTHON=py"
) else (
  set "CV_PYTHON=python"
)

%CV_PYTHON% -c "import openpyxl, reportlab" >nul 2>nul
if errorlevel 1 (
  echo Instalando las dependencias necesarias...
  %CV_PYTHON% -m pip install -r "scripts\requirements.txt"
  if errorlevel 1 goto :error
)

echo Actualizando HTML y PDF en ambos idiomas...
%CV_PYTHON% "scripts\generar_cv.py"
if errorlevel 1 goto :error

call :publicar_github
if errorlevel 1 goto :git_error

echo.
echo CV actualizado correctamente.
pause
exit /b 0

:publicar_github
where git >nul 2>nul
if errorlevel 1 (
  echo.
  echo Git no esta instalado. Se omite la publicacion en GitHub.
  exit /b 0
)

git rev-parse --is-inside-work-tree >nul 2>nul
if errorlevel 1 (
  echo.
  echo La carpeta todavia no es un repositorio Git. Se omite la publicacion.
  exit /b 0
)

echo.
echo Preparando la actualizacion para GitHub...
git add -A
if errorlevel 1 exit /b 1

git diff --cached --quiet --no-ext-diff
if errorlevel 2 exit /b 1
if not errorlevel 1 (
  echo No hay cambios nuevos que publicar.
  exit /b 0
)

git commit -m "Actualiza CV"
if errorlevel 1 exit /b 1

git rev-parse --abbrev-ref --symbolic-full-name "@{u}" >nul 2>nul
if errorlevel 1 (
  for /f "delims=" %%B in ('git branch --show-current') do set "CV_GIT_BRANCH=%%B"
  if not defined CV_GIT_BRANCH exit /b 1
  git remote get-url origin >nul 2>nul
  if errorlevel 1 exit /b 1
  git push --set-upstream origin "%CV_GIT_BRANCH%"
) else (
  git push
)
if errorlevel 1 exit /b 1

echo CV publicado correctamente en GitHub.
exit /b 0

:error
echo.
echo No se pudo actualizar el CV. Revisa el mensaje anterior.
pause
exit /b 1

:git_error
echo.
echo El CV se ha actualizado en el equipo, pero no se pudo publicar en GitHub.
echo Revisa la conexion, el inicio de sesion y la configuracion del repositorio.
pause
exit /b 1
