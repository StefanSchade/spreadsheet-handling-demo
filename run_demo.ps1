# run_demo.ps1 -- ACME demo launcher for Windows
#
# Usage:  .\run_demo.ps1 <pipeline.yaml> [extra flags]
# Flag:   -RefreshVenv  force venv recreate
#
# Examples:
#   .\run_demo.ps1 pipelines\acme_01_plain_forward.yaml
#   .\run_demo.ps1 pipelines\acme_01_plain_reverse.yaml
#
# Requires: Python 3.10+ on PATH (no WSL needed)

param(
    [Parameter(Position = 0)]
    [string] $Pipeline,

    [switch] $RefreshVenv,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $Extra
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir
$Venv      = Join-Path $ScriptDir ".venv"
$Python    = Join-Path $Venv "Scripts\python.exe"
$Pip       = Join-Path $Venv "Scripts\pip.exe"

if (-not $Pipeline) {
    Write-Host "Usage: .\run_demo.ps1 [pipeline.yaml] [-RefreshVenv] [extra flags]"
    Write-Host ""
    Write-Host "  .\run_demo.ps1 pipelines\acme_01_plain_forward.yaml"
    Write-Host "  .\run_demo.ps1 pipelines\acme_01_plain_reverse.yaml"
    exit 1
}

# Create venv and install once; skip on subsequent runs to avoid uncontrolled upgrades
if ($RefreshVenv -or -not (Test-Path $Python)) {
    Write-Host "Setting up .venv (use -RefreshVenv to force update) ..."
    python -m venv $Venv
    & $Pip install -e $ScriptDir
    Write-Host "Done."
}

& $Python -m spreadsheet_handling.cli.apps.run --config $Pipeline @Extra
