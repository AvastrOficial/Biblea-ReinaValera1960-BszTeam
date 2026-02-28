# run.ps1 - Script para descargar y ejecutar Biblea (Version Windows estable)

param(
    [switch]$Ayuda,
    [switch]$Version2
)

# ===============================
# FUNCION AYUDA
# ===============================
function Mostrar-Ayuda {
    Write-Host "=== Script de Biblea - Ayuda ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Uso: .\run.ps1 [opciones]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opciones:" -ForegroundColor Green
    Write-Host "  -Ayuda      : Muestra esta ayuda"
    Write-Host "  -Version2   : Ejecuta la version 2 (por defecto version 1)"
    Write-Host ""
    Write-Host "Ejemplos:"
    Write-Host "  .\run.ps1"
    Write-Host "  .\run.ps1 -Version2"
    Write-Host "  .\run.ps1 -Ayuda"
}

# ===============================
# MOSTRAR AYUDA
# ===============================
if ($Ayuda) {
    Mostrar-Ayuda
    exit 0
}

Write-Host ""
Write-Host "=== Biblea - Script de Ejecucion Automatica ===" -ForegroundColor Cyan
Write-Host ""

# ===============================
# VERIFICAR PYTHON
# ===============================
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python detectado: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Python no esta instalado o no esta en PATH" -ForegroundColor Red
    Write-Host "Descargar desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# ===============================
# VERIFICAR PIP
# ===============================
try {
    $pipVersion = pip --version 2>&1
    Write-Host "[OK] Pip detectado" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Pip no esta disponible" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

# ===============================
# INSTALAR DEPENDENCIAS
# ===============================
Write-Host ""

if (Test-Path "requirements.txt") {
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt

    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Fallo al instalar dependencias" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }

    Write-Host "[OK] Dependencias instaladas" -ForegroundColor Green
}
else {
    Write-Host "requirements.txt no encontrado. Instalando colorama..." -ForegroundColor Yellow
    pip install colorama
}

Write-Host ""

# ===============================
# EJECUTAR VERSION
# ===============================
if ($Version2) {

    if (Test-Path "BibleaV2.py") {
        Write-Host "Ejecutando Biblea Version 2..." -ForegroundColor Yellow
        python BibleaV2.py
    }
    else {
        Write-Host "[ERROR] No se encontro BibleaV2.py" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }

}
else {

    if (Test-Path "bibleaV1.py") {
        Write-Host "Ejecutando Biblea Version 1..." -ForegroundColor Yellow
        python bibleaV1.py
    }
    else {
        Write-Host "[ERROR] No se encontro bibleaV1.py" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }

}

# ===============================
# RESULTADO FINAL
# ===============================
Write-Host ""

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Ejecucion completada correctamente" -ForegroundColor Green
}
else {
    Write-Host "[ERROR] El programa finalizo con codigo: $LASTEXITCODE" -ForegroundColor Red
}

Write-Host ""
Read-Host "Presiona Enter para salir"
