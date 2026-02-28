# =====================================================
# run.ps1 - Lanzador Biblea con MENU interactivo
# =====================================================

Clear-Host
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "        BIBLEA - MENU DE EJECUCION       " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# ===============================
# IR A CARPETA DEL SCRIPT
# ===============================
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# ===============================
# BUSCAR CARPETA CODIGO
# ===============================
if (Test-Path "..\Codigo") {
    Set-Location "..\Codigo"
}
elseif (Test-Path "Codigo") {
    Set-Location "Codigo"
}
else {
    Write-Host "[ERROR] No se encontro carpeta Codigo" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit
}

Write-Host "[OK] Carpeta Codigo cargada" -ForegroundColor Green
Write-Host ""

# ===============================
# VERIFICAR PYTHON
# ===============================
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python detectado: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Python no instalado" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit
}

Write-Host ""

# ===============================
# INSTALAR DEPENDENCIAS
# ===============================
if (Test-Path "requirements.txt") {
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt | Out-Null
}

# ===============================
# BUSCAR ARCHIVOS PYTHON
# ===============================
$files = Get-ChildItem -Filter *.py

if ($files.Count -eq 0) {
    Write-Host "[ERROR] No se encontraron archivos Python" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit
}

Write-Host ""
Write-Host "Selecciona la version que deseas ejecutar:" -ForegroundColor Yellow
Write-Host ""

# Mostrar menu
for ($i = 0; $i -lt $files.Count; $i++) {
    Write-Host "[$($i+1)] $($files[$i].Name)" -ForegroundColor White
}

Write-Host "[0] Salir"
Write-Host ""

# ===============================
# LEER OPCION
# ===============================
do {
    $choice = Read-Host "Ingresa el numero"
} until ($choice -match '^\d+$' -and [int]$choice -ge 0 -and [int]$choice -le $files.Count)

if ($choice -eq 0) {
    exit
}

$selectedFile = $files[$choice - 1].Name

Write-Host ""
Write-Host "Ejecutando: $selectedFile" -ForegroundColor Cyan
Write-Host ""

# ===============================
# EJECUTAR ARCHIVO
# ===============================
python "$selectedFile"

# ===============================
# RESULTADO FINAL
# ===============================
Write-Host ""

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Programa finalizado correctamente" -ForegroundColor Green
}
else {
    Write-Host "[ERROR] El programa termino con codigo: $LASTEXITCODE" -ForegroundColor Red
}

Write-Host ""
Read-Host "Presiona Enter para salir"
