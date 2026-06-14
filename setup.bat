@echo off
title Configurazione Ambiente Virtuale Python 3.13
echo =======================================================
echo    RESET E CONFIGURAZIONE .VENV CON PYTHON 3.13
echo =======================================================
echo.

:: 1. Rimozione vecchia venv se esiste per evitare conflitti
if exist .venv (
    echo [1/4] Rimozione della vecchia cartella .venv in corso...
    rmdir /s /q .venv
) else (
    echo [1/4] Nessuna vecchia .venv da rimuovere. Procedo.
)

echo.
echo [2/4] Ricerca di Python 3.13 nel sistema...

:: Controlla se py launcher puo forzare la 3.13
py -3.13 -c "import sys; print('Rilevato Python:', sys.version)" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python 3.13 trovato tramite l'eseguibile 'py'!
    echo Creazione della nuova .venv...
    py -3.13 -m venv .venv
    goto venv_creata
)

:: Tentativo alternativo se il comando precedente fallisce
python3.13 -c "import sys; print('Rilevato Python:', sys.version)" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python 3.13 trovato tramite il comando 'python3.13'!
    echo Creazione della nuova .venv...
    python3.13 -m venv .venv
    goto venv_creata
)

echo ❌ ERRORE CRITICO: Python 3.13 non e stato trovato sul tuo computer!
echo Assicurati di aver scaricato e installato Python 3.13 da python.org
echo e di aver spuntato l'opzione "Add python.exe to PATH" durante l'installazione.
pause
exit

:venv_creata
echo.
echo [3/4] Attivazione della nuova .venv...
call .venv\Scripts\activate.bat

echo.
echo [4/4] Aggiornamento pip e installazione librerie di trading/app...
python -m pip install --upgrade pip
pip install streamlit ccxt pandas numpy plotly

echo.
echo =======================================================
echo 🎉 CONFIGURAZIONE COMPLETATA CON SUCCESSO!
echo Ora la tua .venv usa stabilmente Python 3.13.
echo Puoi chiudere questa finestra e lanciare lo 'start.bat'.
echo =======================================================
echo.
pause