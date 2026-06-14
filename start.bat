@echo off
setlocal enabledelayedexpansion
title Avvio Intelligente NO BR NO PARTY Engine

echo =======================================================
echo    AVVIO SOLIDO REALE CON RICERCA PORTA AUTOMATICA
echo =======================================================
echo.

:: 1. Controllo presenza .venv
if not exist .venv (
    echo [X] ERRORE: Cartella .venv non trovata.
    echo     Esegui prima il file 'setup.bat' per configurare l'ambiente.
    echo.
    pause
    exit
)

:: 2. Attivazione dell'ambiente virtuale
echo [1/3] Attivazione ambiente virtuale (.venv)...
call .venv\Scripts\activate.bat

echo [2/3] Verifica versione di Python reale in uso:
python --version
echo.

:: 3. Algoritmo di ricerca porta libera (da 5050 a 5100)
echo [3/3] Ricerca automatica di una porta libera nel sistema...
set "START_PORT=5050"
set "END_PORT=5100"
set "FOUND_PORT="

for /L %%P in (%START_PORT%, 1, %END_PORT%) do (
    :: Usa netstat per vedere se la porta corrente ha connessioni attive o ascolti
    netstat -ano | findstr /R /C:":%%P " >nul 2>&1
    if !errorlevel! equ 1 (
        :: Se il comando restituisce 1, significa che la porta e LIBERA!
        set "FOUND_PORT=%%P"
        goto :porta_trovata
    ) else (
        echo     ⚠️ Porta %%P occupata, controllo la successiva...
    )
)

if "%FOUND_PORT%"=="" (
    echo [X] ERRORE CRITICO: Nessuna porta libera trovata nel range %START_PORT%-%END_PORT%.
    echo     Prova a chiudere qualche applicazione o riavviare il PC.
    echo.
    pause
    exit
)

:porta_trovata
echo.
echo =======================================================
echo 🔥 PORTA LIBERA IDENTIFICATA: !FOUND_PORT!
echo 🚀 Lancio di Streamlit con 'app.py' su porta !FOUND_PORT!...
echo =======================================================
echo.

:: Avvia Streamlit forzando la porta dinamica appena scoperta
streamlit run app.py --server.port !FOUND_PORT!

pause

