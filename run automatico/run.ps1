# run.ps1 - Script para descargar y ejecutar Biblea

param(
    [switch]$Ayuda,
    [switch]$Version2
)

# Función para mostrar ayuda
function Mostrar-Ayuda {
    Write-Host "=== Script de Biblea - Ayuda ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Uso: .\run.ps1 [opciones]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opciones:" -ForegroundColor Green
    Write-Host "  -Ayuda      : Muestra esta ayuda" -ForegroundColor White
    Write-Host "  -Version2   : Ejecuta la versión 2 (por defecto ejecuta la versión 1)" -ForegroundColor White
    Write-Host ""
    Write-Host "Ejemplos:" -ForegroundColor Green
    Write-Host "  .\run.ps1              # Ejecuta Biblea versión 1" -ForegroundColor White
    Write-Host "  .\run.ps1 -Version2     # Ejecuta Biblea versión 2" -ForegroundColor White
    Write-Host "  .\run.ps1 -Ayuda        # Muestra esta ayuda" -ForegroundColor White
}

# Verificar si se solicita ayuda
if ($Ayuda) {
    Mostrar-Ayuda
    exit 0
}

Write-Host "=== Biblea - Script de Ejecución Automática ===" -ForegroundColor Cyan
Write-Host ""

# Verificar si Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python detectado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "  Por favor, instala Python desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  Asegúrate de marcar 'Add Python to PATH' durante la instalación" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar si pip está instalado
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ Pip detectado" -ForegroundColor Green
} catch {
    Write-Host "✗ Pip no está instalado o no está en el PATH" -ForegroundColor Red
    exit 1
}

# Verificar si existe requirements.txt e instalar dependencias
if (Test-Path "requirements.txt") {
    Write-Host "Instalando dependencias desde requirements.txt..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Error al instalar dependencias" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Dependencias instaladas correctamente" -ForegroundColor Green
} else {
    Write-Host "No se encontró requirements.txt. Instalando dependencias comunes..." -ForegroundColor Yellow
    pip install colorama
    Write-Host "✓ Dependencias básicas instaladas" -ForegroundColor Green
}

Write-Host ""

# Determinar qué versión ejecutar
if ($Version2) {
    if (Test-Path "BibleaV2.py") {
        Write-Host "Ejecutando Biblea Versión 2..." -ForegroundColor Yellow
        python BibleaV2.py
    } else {
        Write-Host "✗ No se encontró BibleaV2.py" -ForegroundColor Red
        Write-Host "  Verificando si existe BibleaV2.py en el directorio actual" -ForegroundColor Yellow
        exit 1
    }
} else {
    if (Test-Path "bibleaV1.py") {
        Write-Host "Ejecutando Biblea Versión 1..." -ForegroundColor Yellow
        python bibleaV1.py
    } else {
        Write-Host "✗ No se encontró bibleaV1.py" -ForegroundColor Red
        Write-Host "  Verificando si existe bibleaV1.py en el directorio actual" -ForegroundColor Yellow
        exit 1
    }
}

# Verificar el código de salida
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Ejecución completada exitosamente" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "✗ La ejecución finalizó con errores (código: $LASTEXITCODE)" -ForegroundColor Red
}

Write-Host ""
Read-Host "Presiona Enter para salir"
