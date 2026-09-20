import os
import re
import subprocess
import time
import webbrowser
from urllib.parse import quote_plus


# ==========================================================
# JARVIS TOOLS
# Safe, predefined computer actions only.
# ==========================================================


def find_chrome():
    paths = [
        os.path.expandvars(
            r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
        ),
        os.path.expandvars(
            r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
        ),
        os.path.expandvars(
            r"%LocalAppData%\Google\Chrome\Application\chrome.exe"
        ),
    ]

    for path in paths:
        if os.path.exists(path):
            return path

    return None


def open_chrome(url=None):
    chrome = find_chrome()

    if chrome:
        if url:
            subprocess.Popen([chrome, url])
        else:
            subprocess.Popen([chrome])
        return True

    # Fallback to the Windows default browser.
    if url:
        webbrowser.open(url)
    return False


def open_notepad():
    subprocess.Popen(["notepad.exe"])


def open_calculator():
    subprocess.Popen(["calc.exe"])


def open_explorer():
    subprocess.Popen(["explorer.exe"])


def open_vs_code():
    subprocess.Popen("code", shell=True)


def open_folder(folder_name):
    folders = {
        "downloads": os.path.expanduser("~/Downloads"),
        "documents": os.path.expanduser("~/Documents"),
        "desktop": os.path.expanduser("~/Desktop"),
    }

    path = folders.get(folder_name.lower())

    if path and os.path.exists(path):
        os.startfile(path)
        return True

    return False


def google_search(query):
    query = query.strip()

    if not query:
        return False

    url = "https://www.google.com/search?q=" + quote_plus(query)
    return open_chrome(url)


def youtube_search(query):
    query = query.strip()

    if not query:
        return False

    url = (
        "https://www.youtube.com/results?search_query="
        + quote_plus(query)
    )
    return open_chrome(url)


def run_tool(command):
    """
    Return a short spoken result when a known computer action
    is recognized. Return None when the command should go to AI.
    """

    command = command.strip()
    low = command.lower()

    # ------------------------------------------------------
    # OPEN + SEARCH COMBINATIONS
    # ------------------------------------------------------

    match = re.match(
        r"^open\s+chrome\s+and\s+search(?:\s+for)?\s+(.+)$",
        low,
        flags=re.IGNORECASE,
    )

    if match:
        query = match.group(1).strip()
        google_search(query)
        return f"Opening Chrome and searching for {query}."

    match = re.match(
        r"^open\s+youtube\s+and\s+search(?:\s+for)?\s+(.+)$",
        low,
        flags=re.IGNORECASE,
    )

    if match:
        query = match.group(1).strip()
        youtube_search(query)
        return f"Opening YouTube and searching for {query}."

    # ------------------------------------------------------
    # SEARCH IN CHROME
    # ------------------------------------------------------

    match = re.match(
        r"^search\s+(.+?)\s+(?:in|on)\s+chrome$",
        low,
        flags=re.IGNORECASE,
    )

    if match:
        query = match.group(1).strip()
        google_search(query)
        return f"Searching Chrome for {query}."

    # ------------------------------------------------------
    # GOOGLE
    # ------------------------------------------------------

    match = re.match(
        r"^search\s+google\s+for\s+(.+)$",
        low,
        flags=re.IGNORECASE,
    )

    if match:
        query = match.group(1).strip()
        google_search(query)
        return f"Searching Google for {query}."

    # ------------------------------------------------------
    # YOUTUBE
    # ------------------------------------------------------

    match = re.match(
        r"^search\s+youtube\s+for\s+(.+)$",
        low,
        flags=re.IGNORECASE,
    )

    if match:
        query = match.group(1).strip()
        youtube_search(query)
        return f"Searching YouTube for {query}."

    # ------------------------------------------------------
    # APPLICATIONS
    # ------------------------------------------------------

    if low == "open notepad":
        open_notepad()
        return "Opening Notepad."

    if low == "open calculator":
        open_calculator()
        return "Opening Calculator."

    if low in {"open file explorer", "open explorer"}:
        open_explorer()
        return "Opening File Explorer."

    if low in {"open vs code", "open visual studio code"}:
        open_vs_code()
        return "Opening Visual Studio Code."

    if low == "open chrome":
        open_chrome()
        return "Opening Chrome."

    if low == "open youtube":
        open_chrome("https://www.youtube.com")
        return "Opening YouTube."

    if low == "open google":
        open_chrome("https://www.google.com")
        return "Opening Google."

    # ------------------------------------------------------
    # FOLDERS
    # ------------------------------------------------------

    if low == "open downloads":
        if open_folder("downloads"):
            return "Opening Downloads."
        return "I could not find the Downloads folder."

    if low == "open documents":
        if open_folder("documents"):
            return "Opening Documents."
        return "I could not find the Documents folder."

    if low == "open desktop":
        if open_folder("desktop"):
            return "Opening Desktop."
        return "I could not find the Desktop folder."

    # ------------------------------------------------------
    # TIME / DATE
    # ------------------------------------------------------

    if low in {"what time is it", "what is the current time", "current time"}:
        return f"The current time is {time.strftime('%I:%M %p')}."

    if low in {"what date is it", "what is today's date", "today's date"}:
        return f"Today is {time.strftime('%A, %d %B %Y')}."

    return None
