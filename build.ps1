# Build.ps1 for clean FSBestPNG

# Default option is to run build, like a Makefile
param(
    [string]$Task = "build"
)

$buildFSBestPNG = {
    Write-Host "正在打包FSBestPNG..."
    python -m nuitka --show-progress --assume-yes-for-downloads app.py
}

$cleanFSBestPNG = {
    Write-Host "Cleaning..."
    Remove-Item -Recurse -Force app.exe, ./app.build/, ./app.dist/, ./app.onefile-build/ ,/build/ ,/dist/ ,FSBestPNG.spec
}

switch ($Task.ToLower()) {
    "build" {
        & $buildFSBestPNG
        break
    }
    "clean" {
        & $cleanFSBestPNG
        break
    }
    default {
        Write-Host "Unknown task: $Task" -ForegroundColor Red
        Write-Host "Available tasks: build, clean"
        break
    }
}