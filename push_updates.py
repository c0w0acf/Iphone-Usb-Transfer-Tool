import os
import subprocess
from pathlib import Path
import sys

project_dir = Path(r"C:\photo-transfer")
if not project_dir.exists():
    print("[-] Error: C:\\photo-transfer directory not found!")
    sys.exit(1)

os.chdir(project_dir)

def run_git(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr and result.returncode != 0:
        print(f"Git Error: {result.stderr.strip()}")
    return result.returncode

print("==================================================")
print(" GitHub Quick Uploader")
print("==================================================")

run_git("git status")

if len(sys.argv) > 1:
    commit_msg = " ".join(sys.argv[1:])
else:
    commit_msg = input("\nEnter commit message (press Enter for default): ").strip()
    if not commit_msg:
        commit_msg = "Update project files and documentation"

run_git("git add .")

status_check = subprocess.run("git diff --cached --quiet", shell=True)
if status_check.returncode == 0:
    print("\n[!] No changes detected to commit. Everything is up-to-date!")
else:
    run_git(f'git commit -m "{commit_msg}"')
    push_result = run_git("git push origin main")
    
    if push_result == 0:
        print("\n[+] Success! Updated files pushed to GitHub successfully.")
    else:
        print("\n[-] Push failed. Check your network or authentication.")
