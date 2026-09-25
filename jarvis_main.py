import time

import numpy as np
import pyttsx3
import requests
import sounddevice as sd
import soundfile as sf
import whisper
from openwakeword.model import Model

from jarvis_tools import run_tool


# ==========================================================
# SETTINGS
# ==========================================================

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2:3b"

WHISPER_MODEL = "base"

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280

COMMAND_AUDIO = "command.wav"

# Higher = fewer false wake-ups.
WAKE_THRESHOLD = 0.60

# Stop command recording after this much silence.
SILENCE_LIMIT = 1.0

# Maximum time allowed for a spoken command.
MAX_COMMAND_SECONDS = 12.0

# Minimum microphone level considered speech.
SPEECH_THRESHOLD = 700


# ==========================================================
# SPEAK
# ==========================================================

def speak(text):
    print()
    print("JARVIS:", text)
    print("[Speaking...]")

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        print("[Speech finished]")
    except Exception as error:
        print("[Voice error]", error)


# ==========================================================
# LOAD WHISPER
# ==========================================================

print("========================================")
print("        LOADING JARVIS SYSTEM")
print("========================================")
print()

print("Loading Whisper...")
whisper_model = whisper.load_model(WHISPER_MODEL)
print("Whisper ready.")
print()


# ==========================================================
# LOAD WAKE WORD
# ==========================================================

print("Loading wake-word detector...")

wake_model = Model(
    wakeword_models=["hey_jarvis"],
    inference_framework="onnx",
    vad_threshold=0.5,
)

print("Wake-word detector ready.")
print()


# ==========================================================
# SPEECH TO TEXT
# ==========================================================

def understand_command(audio_file):
    print("Understanding your command...")

    try:
        result = whisper_model.transcribe(
            audio_file,
            fp16=False,
            language="en",
        )
        return result["text"].strip()

    except Exception as error:
        print("[Whisper error]", error)
        return ""


# ==========================================================
# RECORD COMMAND UNTIL SILENCE
# ==========================================================

def record_command(stream):
    print()
    print("🎤 Listening... Speak naturally.")
    print("I will stop after you finish speaking.")
    print()

    frames = []

    frame_duration = 0.03
    frame_size = int(SAMPLE_RATE * frame_duration)

    silence_time = 0.0
    elapsed_time = 0.0
    speech_started = False

    while elapsed_time < MAX_COMMAND_SECONDS:

        audio, overflowed = stream.read(frame_size)

        if overflowed:
            print("\n[Microphone overflow]")

        audio = np.asarray(
            audio,
            dtype=np.int16,
        ).flatten()

        frames.append(audio.copy())

        volume = float(
            np.sqrt(
                np.mean(
                    audio.astype(np.float32) ** 2
                )
            )
        )

        if volume >= SPEECH_THRESHOLD:
            speech_started = True
            silence_time = 0.0

        elif speech_started:
            silence_time += frame_duration

        elapsed_time += frame_duration

        if speech_started and silence_time >= SILENCE_LIMIT:
            break

    if not frames:
        return

    audio_data = np.concatenate(frames)

    sf.write(
        COMMAND_AUDIO,
        audio_data,
        SAMPLE_RATE,
    )

    print()
    print("Recording finished.")


# ==========================================================
# ASK LOCAL AI
# ==========================================================

def ask_ai(question):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are JARVIS, Edward's personal AI assistant. "
                            "Help with learning, coding, projects and general "
                            "questions. Never mention Tony Stark or the Stark "
                            "household. Answer clearly and briefly because "
                            "your answers are spoken aloud. Never invent "
                            "personal facts about Edward."
                        ),
                    },
                    {
                        "role": "user",
                        "content": question,
                    },
                ],
                "stream": False,
                "options": {
                    "num_predict": 128,
                },
            },
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        answer = data["message"]["content"].strip()

        # Defensive cleanup if a model emits a think block.
        if "</think>" in answer.lower():
            parts = answer.lower().split("</think>", 1)
            original = answer
            answer = original[original.lower().find("</think>") + 8:].strip()

        return answer

    except requests.exceptions.ConnectionError:
        return (
            "I cannot connect to my AI brain. "
            "Please make sure Ollama is running."
        )

    except requests.exceptions.Timeout:
        return "My AI brain took too long to respond."

    except Exception as error:
        print("[AI error]", error)
        return "I encountered a problem while processing your request."


# ==========================================================
# START
# ==========================================================

print("========================================")
print("             JARVIS ONLINE")
print("========================================")
print()

speak(
    "Good day, Edward. JARVIS is online."
)

print()
print('Say "Hey Jarvis" to wake me.')
print()


# ==========================================================
# CONTINUOUS LISTENING
# ==========================================================

try:

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        blocksize=CHUNK_SIZE,
    ) as stream:

        while True:

            # ----------------------------------------------
            # LISTEN FOR WAKE WORD
            # ----------------------------------------------

            audio, overflowed = stream.read(CHUNK_SIZE)

            if overflowed:
                print("\n[Microphone overflow]")

            audio = np.asarray(
                audio,
                dtype=np.int16,
            ).flatten()

            predictions = wake_model.predict(audio)

            wake_score = predictions.get(
                "hey_jarvis",
                0.0,
            )

            # ----------------------------------------------
            # WAKE
            # ----------------------------------------------

            if wake_score >= WAKE_THRESHOLD:

                print()
                print("========================================")
                print("       JARVIS WAKE WORD DETECTED")
                print("========================================")

                wake_model.reset()

                speak("Yes, Edward?")

                # Give TTS time to finish before recording.
                time.sleep(0.8)

                # ------------------------------------------
                # RECORD COMMAND
                # ------------------------------------------

                record_command(stream)

                # ------------------------------------------
                # UNDERSTAND COMMAND
                # ------------------------------------------

                command = understand_command(
                    COMMAND_AUDIO
                )

                print()
                print("YOU:", command)

                if not command:
                    speak("I didn't understand that.")
                    continue

                # ------------------------------------------
                # EXIT
                # ------------------------------------------

                if command.lower().strip() in {
                    "exit",
                    "quit",
                    "shutdown",
                    "shutdown jarvis",
                    "goodbye jarvis",
                }:
                    speak(
                        "Shutting down. Goodbye, Edward."
                    )
                    break

                # ------------------------------------------
                # COMPUTER TOOLS
                # ------------------------------------------

                tool_result = run_tool(command)

                if tool_result is not None:

                    speak(tool_result)

                    time.sleep(1.5)

                    wake_model.reset()

                    print()
                    print('Listening for "Hey Jarvis"...')

                    continue

                # ------------------------------------------
                # NORMAL AI QUESTION
                # ------------------------------------------

                answer = ask_ai(command)

                speak(answer)

                time.sleep(1.5)

                wake_model.reset()

                print()
                print('Listening for "Hey Jarvis"...')


except KeyboardInterrupt:

    print()
    print()
    print("JARVIS stopped.")
