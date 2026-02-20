# Execute this script running 'Install.bat' to bypass Windows ExecutionPolicy 

# request admin access
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    Exit
}

$source = "$PSScriptRoot\intelbras-info"
$destination = $env:ProgramFiles
$newDestination = "$env:ProgramFiles\intelbras-info"

# move path to Program Files
if (Test-Path $source) {
    Copy-Item -Path $source -Destination $destination -Force -Recurse -ErrorAction SilentlyContinue
}

$pathAtual = [Environment]::GetEnvironmentVariable("Path", "Machine")

# put path in system variable to run globally
if (-not $pathAtual.Contains($newDestination)) {
    $newPath = "$pathAtual;$newDestination"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
}

# update atual environment
$env:Path += ";$destination"