# ============================================================
# Ollama Benchmark Launcher
#
# Checks/creates the Python virtual environment, ensures the
# Ollama Python package is installed, and launches driver.py.
# ============================================================

$ErrorActionPreference = "Stop"

# Always run relative to the directory containing this script.
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ProjectRoot

$VenvPath = Join-Path $ProjectRoot ".venv"
$PythonPath = Join-Path $VenvPath "Scripts\python.exe"
$DriverPath = Join-Path $ProjectRoot "driver.py"


Write-Host ""
Write-Host "============================================================"
Write-Host " Ollama Local LLM Benchmark"
Write-Host "============================================================"
Write-Host ""


# ------------------------------------------------------------
# Check for Python
# ------------------------------------------------------------

Write-Host "Checking Python..."

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host "ERROR: Python was not found on this computer." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.10 or newer and make sure"
    Write-Host "Python is available from the command line."
    Write-Host ""
    exit 1
}

$PythonVersion = python --version
Write-Host "Found: $PythonVersion"


# ------------------------------------------------------------
# Create virtual environment if necessary
# ------------------------------------------------------------

if (-not (Test-Path $PythonPath)) {

    Write-Host ""
    Write-Host "Virtual environment not found."
    Write-Host "Creating .venv..."

    python -m venv .venv

    if (-not (Test-Path $PythonPath)) {
        Write-Host ""
        Write-Host "ERROR: Failed to create the virtual environment." -ForegroundColor Red
        Write-Host ""
        exit 1
    }

    Write-Host "Virtual environment created."
}
else {
    Write-Host "Virtual environment found."
}


# ------------------------------------------------------------
# Make sure pip is available
# ------------------------------------------------------------

Write-Host ""
Write-Host "Checking pip..."

& $PythonPath -m ensurepip --upgrade --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Could not initialize pip." -ForegroundColor Red
    Write-Host ""
    exit 1
}


# ------------------------------------------------------------
# Check/install Ollama Python package
# ------------------------------------------------------------

Write-Host "Checking Python Ollama package..."

$OllamaInstalled = & $PythonPath -c @"
try:
    import ollama
    print("yes")
except ImportError:
    print("no")
"@

if ($OllamaInstalled.Trim() -ne "yes") {

    Write-Host "Ollama Python package not found."
    Write-Host "Installing ollama..."

    & $PythonPath -m pip install ollama

    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "ERROR: Failed to install the Ollama Python package." -ForegroundColor Red
        Write-Host ""
        exit 1
    }

    Write-Host "Ollama Python package installed."
}
else {
    Write-Host "Ollama Python package found."
}


# ------------------------------------------------------------
# Check driver.py
# ------------------------------------------------------------

if (-not (Test-Path $DriverPath)) {
    Write-Host ""
    Write-Host "ERROR: driver.py was not found." -ForegroundColor Red
    Write-Host ""
    Write-Host "Expected location:"
    Write-Host "  $DriverPath"
    Write-Host ""
    exit 1
}


# ------------------------------------------------------------
# Launch benchmark driver
# ------------------------------------------------------------

Write-Host ""
Write-Host "Launching benchmark..."
Write-Host ""

& $PythonPath $DriverPath

$ExitCode = $LASTEXITCODE


# ------------------------------------------------------------
# Exit
# ------------------------------------------------------------

Write-Host ""

if ($ExitCode -eq 0) {
    Write-Host "Benchmark finished." -ForegroundColor Green
}
else {
    Write-Host "Benchmark exited with code $ExitCode." -ForegroundColor Yellow
}

exit $ExitCode
