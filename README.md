# 🤖 JARVIS – Local Windows Voice Assistant

A local-first, voice-controlled AI assistant for Windows built with **Python, Ollama, Llama 3.2, Whisper, OpenWakeWord, and Windows automation**.

JARVIS can listen for a wake word, understand spoken commands, generate responses locally, speak back, and perform predefined actions on the Windows desktop.

## ✨ Features

- 🎤 Voice input through the microphone
- ⚡ “Hey Jarvis” wake-word detection
- 🧠 Local AI using Llama 3.2 3B with Ollama
- 🗣️ Speech-to-text using Whisper
- 🔊 Voice responses using pyttsx3
- 💻 Windows application and folder automation
- 🌐 Chrome, Google, and YouTube search
- 📦 Windows executable packaging with PyInstaller
- 🔒 Local-first AI processing

## 🧠 How It Works

```text
🎤 Voice
   ↓
⚡ Wake Word Detection
   ↓
🗣️ Whisper Speech-to-Text
   ↓
🧠 JARVIS Core
   ↓
┌───────────────┬───────────────┐
│               │
💻 Computer     🧠 Ollama
   Tools         Llama 3.2
│               │
└───────┬───────┘
        ↓
   🔊 Voice Response
````

## 🛠️ Tech Stack

| Technology   | Purpose                      |
| ------------ | ---------------------------- |
| Python       | Core application logic       |
| Ollama       | Local LLM runtime            |
| Llama 3.2 3B | AI model                     |
| Whisper      | Speech-to-text               |
| OpenWakeWord | Wake-word detection          |
| pyttsx3      | Text-to-speech               |
| SoundDevice  | Microphone input             |
| SoundFile    | Audio recording              |
| Requests     | Ollama API communication     |
| PyInstaller  | Windows executable packaging |

## 🚀 Example Commands

After saying **“Hey Jarvis”**, try:

```text
Open Chrome
```

```text
Open Notepad
```

```text
Open Calculator
```

```text
Open Downloads
```

```text
Search Google for Python tutorials
```

```text
Search YouTube for machine learning tutorials
```

```text
What is artificial intelligence?
```

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/nithishedward/jarvis-local-windows-assistant.git
cd jarvis-local-windows-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama

Install Ollama for Windows, then download the required model:

```bash
ollama pull llama3.2:3b
```

### 4. Run JARVIS

```bash
python jarvis_main.py
```

## 📦 Build the Windows Executable

JARVIS can be packaged as a Windows application using PyInstaller:

```bash
pyinstaller --noconfirm --clean --onedir --name JARVIS --collect-all openwakeword --collect-data whisper jarvis_main.py
```

The executable will be created inside:

```text
dist/JARVIS/
```

## 🔐 Privacy

JARVIS follows a **local-first architecture**.

Core components such as:

* Speech recognition
* Wake-word detection
* LLM inference

can run locally on the user's Windows machine through **Whisper, OpenWakeWord, and Ollama**.

Internet access is used for features such as web searches and downloading dependencies or models.

## 🗺️ Roadmap

* [x] Voice input
* [x] Speech-to-text
* [x] Local LLM integration
* [x] Text-to-speech
* [x] Wake-word detection
* [x] Windows automation
* [x] Web search
* [x] Windows executable
* [ ] Smarter intent and tool system
* [ ] Structured persistent memory
* [ ] Computer vision
* [ ] Advanced desktop interaction
* [ ] JARVIS-style graphical interface
* [ ] Modular skill system

## 🎯 Project Goal

The goal of JARVIS is to explore how **local AI, voice interfaces, automation, and AI agents** can work together to create a practical desktop assistant.

## 🤝 Contributing

Ideas, suggestions, improvements, and contributions are welcome.

Feel free to open an issue or submit a pull request.

## 👨‍💻 Developer

**Nithish Edward**

Artificial Intelligence & Machine Learning Student

🔗 GitHub: [https://github.com/nithishedward](https://github.com/nithishedward)

---
