@echo off
setlocal enabledelayedexpansion
title PGP Tool

echo.
echo  ==============================
echo   PGP Tool - Windows Launcher
echo  ==============================
echo.

:: ─── Check Python ───────────────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERREUR] Python n'est pas installe.
    echo.
    echo  Installez Python depuis : https://www.python.org/downloads/
    echo  IMPORTANT : cochez "Add Python to PATH" pendant l'installation !
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo  [OK] %PY_VER% detecte

:: ─── Check GPG ───────────────────────────────────────────────────────────────
gpg --version >nul 2>&1
if errorlevel 1 (
    echo  [ERREUR] GnuPG n'est pas installe.
    echo.
    echo  Installez Gpg4win depuis : https://www.gpg4win.org/
    echo  Redemarrez ce script apres l'installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=3" %%v in ('gpg --version 2^>^&1 ^| findstr /i "GnuPG"') do set GPG_VER=%%v
echo  [OK] GnuPG %GPG_VER% detecte

:: ─── Create venv if missing ──────────────────────────────────────────────────
if not exist "venv" (
    echo.
    echo  Mise en place de l'environnement Python...
    python -m venv venv
    if errorlevel 1 (
        echo  [ERREUR] Impossible de creer l'environnement virtuel.
        pause
        exit /b 1
    )
    echo  [OK] Environnement cree
)

:: ─── Install / update dependencies ──────────────────────────────────────────
echo.
echo  Verification des dependances...
venv\Scripts\python.exe -m pip install -r requirements.txt -q --disable-pip-version-check
if errorlevel 1 (
    echo  [ERREUR] Impossible d'installer les dependances.
    pause
    exit /b 1
)
echo  [OK] Dependances installees

:: ─── Start Flask ─────────────────────────────────────────────────────────────
echo.
echo  ==============================
echo   Serveur demarre !
echo   Ouvre ton navigateur sur :
echo   http://localhost:5000
echo  ==============================
echo.
echo  (Ferme cette fenetre pour arreter le serveur)
echo.

start "" "http://localhost:5000"
venv\Scripts\python.exe app.py

pause
