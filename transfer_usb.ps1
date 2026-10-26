# 📱 iPhone to Windows USB Photo Transfer Tool

A lightweight, native PowerShell script designed to bypass cloud syncs, Wi-Fi bottlenecks, and browser restrictions by copying photos and videos directly from an iPhone to a Windows PC over a USB-C cable.

## 🚀 Features
- **Zero Third-Party Apps Required:** Uses native Windows Shell automation (`Shell.Application`) to interface with iOS Media Transfer Protocol (MTP).
- **Direct Folder Traversal:** Automatically navigates iPhone internal storage directories (handling iOS-structured folders like `202602__`, `202203__`, etc.).
- **Graceful Stop Key:** Press **`Q`** or **`ESC`** between folder transfers to safely halt the script at any time.
- **Duplicate Safety:** Built-in Windows file-handling integration skips or manages conflicts cleanly.

---

## 📋 Prerequisites
1. **Windows 10 or 11** PC.
2. An **iPhone** connected via a high-speed USB-C data cable.
3. Your iPhone must be **unlocked** with the screen awake, and you must tap **"Trust This Computer"** when prompted.

---

## ⚙️ How to Use

1. Ensure your files are in `C:\photo-transfer`.
2. Connect your iPhone to your PC via USB and unlock your screen.
3. Open **PowerShell** and navigate to your directory:
   ```powershell
   cd C:\photo-transfer
New-Item -ItemType Directory -Force -Path "C:\photo-transfer" | Out-Null; Set-Location "C:\photo-transfer";

@'
<#
.SYNOPSIS
    iPhone to Windows USB Photo Transfer Tool with Stop Key Support.
.DESCRIPTION
    Connects to an iOS device via USB, accesses internal storage, 
    and copies media folders recursively to a local PC directory.
    Includes support for halting the process gracefully.
#>

$shell = New-Object -ComObject Shell.Application

Write-Host "Searching for connected iPhone..." -ForegroundColor Cyan

# Locate iPhone under 'This PC'
$pc = $shell.NameSpace(17)
$iphone = $pc.Items() | Where-Object { $_.Name -match "iPhone" }

if (-not $iphone) {
    Write-Host "Error: iPhone not found! Make sure it's plugged in, unlocked, and trusted." -ForegroundColor Red
    pause
    exit
}

Write-Host "Found device: $($iphone.Name)" -ForegroundColor Green

# Locate Internal Storage
$internalStorage = $null
foreach ($item in $iphone.GetFolder().Items()) {
    if ($item.Name -match "Internal Storage") {
        $internalStorage = $item
        break
    }
}

if (-not $internalStorage) {
    $internalStorage = $iphone.GetFolder().Items() | Select-Object -First 1
}

if (-not $internalStorage) {
    Write-Host "Error: Could not access Internal Storage. Is your iPhone locked?" -ForegroundColor Red
    pause
    exit
}

# Set destination folder on PC
$destPath = "C:\photo-transfer\transferred_photos"
if (-not (Test-Path $destPath)) {
    New-Item -ItemType Directory -Path $destPath | Out-Null
}

$destFolder = $shell.NameSpace($destPath)

Write-Host "==================================================" -ForegroundColor Yellow
Write-Host " Internal Storage accessed! Starting transfer..." -ForegroundColor Yellow
Write-Host " TIP: Press 'Q' or 'ESC' between folders to stop." -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Yellow

# Loop through all folders inside Internal Storage (e.g., year/month media folders)
foreach ($subFolder in $internalStorage.GetFolder().Items()) {
    
    # Check if user pressed a stop key before starting the next folder
    if ([Console]::KeyAvailable) {
        $key = [Console]::ReadKey($true)
        if ($key.Key -eq 'Q' -or $key.Key -eq 'Escape') {
            Write-Host "`n[!] Transfer aborted by user." -ForegroundColor Red
            break
        }
    }

    Write-Host "Copying folder: $($subFolder.Name)..." -ForegroundColor Green
    $destFolder.CopyHere($subFolder, 16)
}

Write-Host "`nTransfer process completed or stopped." -ForegroundColor Green
pause
