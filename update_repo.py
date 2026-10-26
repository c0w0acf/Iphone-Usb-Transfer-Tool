import os
import subprocess
from pathlib import Path

# Set target directory
project_dir = Path(r"C:\photo-transfer")
project_dir.mkdir(parents=True, exist_ok=True)
os.chdir(project_dir)

# 1. Updated PowerShell Script with Duplicate Checking
script_content = r"""<#
.SYNOPSIS
    iPhone to Windows USB Photo Transfer Tool with Duplicate Checking & Stop Key.
.DESCRIPTION
    Connects to an iOS device via USB, accesses internal storage, 
    and copies media files recursively while skipping duplicates based on name and size.
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
Write-Host " Internal Storage accessed! Starting smart transfer..." -ForegroundColor Yellow
Write-Host " TIP: Press 'Q' or 'ESC' between folders to stop." -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Yellow

$copiedCount = 0
$skippedCount = 0

# Loop through date folders (e.g., 202602__)
foreach ($subFolder in $internalStorage.GetFolder().Items()) {
    
    # Check if user pressed a stop key before starting the next folder
    if ([Console]::KeyAvailable) {
        $key = [Console]::ReadKey($true)
        if ($key.Key -eq 'Q' -or $key.Key -eq 'Escape') {
            Write-Host "`n[!] Transfer aborted by user." -ForegroundColor Red
            break
        }
    }

    Write-Host "Scanning folder: $($subFolder.Name)..." -ForegroundColor Cyan
    
    # Create matching subfolder in destination if it doesn't exist
    $targetSubDirPath = Join-Path $destPath $subFolder.Name
    if (-not (Test-Path $targetSubDirPath)) {
        New-Item -ItemType Directory -Path $targetSubDirPath | Out-Null
    }
    $targetSubDir = $shell.NameSpace($targetSubDirPath)

    # Iterate through files inside the iPhone subfolder for smart duplicate checking
    foreach ($file in $subFolder.GetFolder().Items()) {
        # Skip if it's another folder nested inside
        if ($file.IsFolder) { continue }

        $destFileCheck = Join-Path $targetSubDirPath $file.Name
        
        # Duplicate check: If file already exists with same name, skip copying
        if (Test-Path $destFileCheck) {
            $existingItem = Get-Item $destFileCheck
            # Optional extra check: Match size if available
            if ($existingItem.Length -eq $file.Size) {
                Write-Host "  [SKIP] Duplicate found: $($file.Name)" -ForegroundColor DarkGray
                $skippedCount++
                continue
            }
        }

        # Copy individual file if not a duplicate
        $targetSubDir.CopyHere($file, 16)
        Write-Host "  [COPY] $($file.Name)" -ForegroundColor Green
        $copiedCount++
    }
}

Write-Host "`n==================================================" -ForegroundColor Yellow
Write-Host " Transfer Complete!" -ForegroundColor Green
Write-Host " Copied: $copiedCount new file(s)" -ForegroundColor Cyan
Write-Host " Skipped: $skippedCount duplicate(s)" -ForegroundColor DarkCyan
Write-Host "==================================================" -ForegroundColor Yellow
pause
"""

# 2. Updated README Content including Duplicate Checking documentation
readme_content = """# 📱 iPhone to Windows USB Photo Transfer Tool

A lightweight, native PowerShell script designed to bypass cloud syncs, Wi-Fi bottlenecks, and browser restrictions by copying photos and videos directly from an iPhone to a Windows PC over a USB-C cable.

## 📌 Summary
Transferring media from an iPhone to Windows via USB can often be frustrating due to nested MTP storage structures and iOS date-coded folders (`YYYYMM__`). This tool solves these challenges by:
- Automatically detecting your iPhone connected via USB.
- Directly traversing iOS internal storage directories (such as `202602__`, `202203__`, etc.).
- **Smart Duplicate Prevention:** Automatically checks destination filenames and sizes, skipping already-backed-up photos to save time and storage.
- Providing an interruptible workflow where you can press **`Q`** or **`ESC`** between folder copies to stop the process gracefully.
- Requiring **zero third-party apps**, relying entirely on native Windows COM automation (`Shell.Application`).

---

## 🚀 Features
- **Smart Duplicate Check:** Prevents re-downloading existing media by verifying name and file size.
- **Native Automation:** Uses built-in Windows shell features with no extra software needed.
- **Smart Folder Traversal:** Seamlessly parses iOS date-based storage directories.
- **Graceful Stop Key:** Press **`Q`** or **`ESC`** between folder transfers to halt safely.
- **Privacy First:** Configured with a `.gitignore` to keep your personal photo library local and off GitHub.

---

## 📋 Prerequisites
1. **Windows 10 or 11** PC.
2. An **iPhone** connected via a high-speed USB-C data cable.
3. Your iPhone must be **unlocked** with the screen awake, and you must tap **"Trust This Computer"** if prompted.

---

## ⚙️ How to Use

1. **Clone or Download** this repository to your local machine (e.g., `C:\photo-transfer`).
2. Connect your iPhone to your PC via USB and unlock your screen.
3. Open **PowerShell** and navigate to your project directory:
   ```powershell
   cd C:\photo-transfer