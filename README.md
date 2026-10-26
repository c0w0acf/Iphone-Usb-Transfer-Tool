# 📱 iPhone to Windows USB Photo Transfer Tool

A lightweight, native PowerShell script designed to bypass cloud syncs, Wi-Fi bottlenecks, and browser restrictions by copying photos and videos directly from an iPhone to a Windows PC over a USB-C cable.

## 📌 Summary
Transferring media from an iPhone to Windows via USB can often be frustrating due to nested MTP storage structures and iOS date-coded folders (`YYYYMM__`). This tool solves these challenges by:
- Automatically detecting your iPhone connected via USB.
- Directly traversing iOS internal storage directories (such as `202602__`, `202203__`, etc.).
- Providing an interruptible workflow where you can press **`Q`** or **`ESC`** between folder copies to stop the process gracefully.
- Requiring **zero third-party apps**, relying entirely on native Windows COM automation (`Shell.Application`).

---

## 🚀 Features
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
