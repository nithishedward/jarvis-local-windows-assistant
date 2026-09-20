# Upload JARVIS to GitHub

1. Create a new empty repository on GitHub. Example name: `jarvis-local-windows-assistant`.
2. Do not add a README, `.gitignore`, or license during GitHub repository creation because they already exist in this project folder.
3. Open PowerShell in this project folder.
4. Run:

```powershell
git init
git add jarvis_main.py jarvis_tools.py requirements.txt README.md .gitignore run_jarvis.bat
git commit -m "Initial JARVIS assistant"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPOSITORY` with your GitHub username and repository name.

Do not commit:

- `facts.json`
- `memory.json`
- `.wav` files
- `build/`
- `dist/`
- `.venv/`
- API keys or `.env` files

The `.gitignore` in this project already excludes those local/private files.
