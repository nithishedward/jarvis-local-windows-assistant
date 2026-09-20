# JARVIS - Local Windows Voice Assistant

A beginner-friendly, local-first JARVIS-style desktop assistant for Windows.

JARVIS currently combines:

- **Llama 3.2 3B** through Ollama for local AI responses
- **Whisper** for speech-to-text
- **OpenWakeWord** for the `Hey Jarvis` wake phrase
- **pyttsx3** for spoken responses
- Predefined Windows tools for apps, folders, Chrome, Google, YouTube, date, and time

## How it works

```text
Microphone
    ↓
OpenWakeWord ("Hey Jarvis")
    ↓
Whisper
    ↓
JARVIS Python controller
    ├── Safe computer tools
    └── Ollama → Llama 3.2 3B
    ↓
pyttsx3
    ↓
Speakers
```

## Requirements

- Windows 10/11
- Python 3.13 (the current development setup uses Python 3.13)
- Ollama
- Llama 3.2 3B model
- FFmpeg
- Working microphone and speakers

## Setup

### 1. Install Ollama

Install Ollama for Windows from:

https://ollama.com/download/windows

Then download the model:

```powershell
ollama pull llama3.2:3b
```

### 2. Install FFmpeg

With WinGet:

```powershell
winget install --id Gyan.FFmpeg
```

Close and reopen PowerShell after installation, then verify:

```powershell
ffmpeg -version
```

### 3. Create a Python virtual environment

From the project folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 4. Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 5. Start JARVIS

```powershell
python jarvis_main.py
```

On first use, Whisper and OpenWakeWord may download their model files.

## Usage

Wait for:

```text
JARVIS ONLINE
```

Then say:

> Hey Jarvis

JARVIS will answer:

> Yes, Edward?

Then try:

> Open Chrome

> Search Python tutorial in Chrome

> Search YouTube for machine learning tutorials

> Open Downloads

> What time is it?

For normal questions, JARVIS sends the request to the local Llama model through Ollama.

## Safety

JARVIS uses a predefined set of computer tools. It does **not** provide the AI with unrestricted PowerShell, command execution, or file deletion abilities.

Personal memory files and audio recordings are ignored by Git so they are not accidentally committed.

## Project structure

```text
JARVIS/
├── jarvis_main.py       # Main voice assistant
├── jarvis_tools.py      # Predefined computer actions
├── requirements.txt     # Python dependencies
├── .gitignore           # Files that should not be committed
└── README.md            # Project documentation
```

## Current limitations

- Wake phrase is currently `Hey Jarvis`.
- Whisper transcription accuracy depends on the microphone, environment, and speech.
- The assistant currently focuses on Windows desktop actions and local AI chat.
- The project is designed for local use; Ollama must be running on the same PC.

## Roadmap

- [ ] Custom `Jarvis` wake word
- [ ] Better conversational memory
- [ ] Screen vision
- [ ] Safer multi-step agent/tool execution
- [ ] Better Windows application control
- [ ] Desktop GUI / JARVIS HUD
- [ ] Windows startup integration
- [ ] Packaged Windows installer
