"""ZA993 — deutscher Sprachassistent."""

from __future__ import annotations

import sys
from datetime import datetime


def say(text: str) -> None:
    """Text ausgeben und wenn möglich mit pyttsx3 vorlesen."""
    print(f"ZA993: {text}")
    try:
        import pyttsx3

        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass


def answer(command: str) -> str:
    text = command.strip().lower()

    if not text:
        return "Bitte gib einen Befehl ein."
    if any(word in text for word in ("hallo", "hey", "guten tag")):
        return "Hallo! Ich bin ZA993. Womit kann ich dir helfen?"
    if "wie heißt" in text:
        return "Ich heiße ZA993."
    if "wie spät" in text or "welche zeit" in text:
        return f"Es ist {datetime.now().strftime('%H:%M')} Uhr."
    if "datum" in text or "welcher tag" in text:
        return f"Heute ist der {datetime.now().strftime('%d.%m.%Y')}"
    if any(word in text for word in ("beenden", "stopp", "tschüss")):
        return "__STOP__"

    return "Ich habe verstanden: " + command


def listen(timeout: int = 5) -> str | None:
    """Sprache über das Mikrofon in deutschen Text umwandeln."""
    try:
        import speech_recognition as sr
    except ImportError:
        return None

    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as microphone:
            recognizer.adjust_for_ambient_noise(microphone, duration=0.5)
            audio = recognizer.listen(microphone, phrase_time_limit=timeout)
            return recognizer.recognize_google(audio, language="de-DE")
    except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
        return None


def main() -> None:
    voice_mode = "--voice" in sys.argv
    say("ZA993 gestartet. Sage oder tippe „Stopp“, um mich zu beenden.")

    while True:
        if voice_mode:
            command = listen()
            if command:
                print(f"Du: {command}")
        else:
            try:
                command = input("Du: ")
            except EOFError:
                break

        if not command:
            continue

        response = answer(command)
        if response == "__STOP__":
            say("Auf Wiedersehen!")
            break
        say(response)


if __name__ == "__main__":
    main()
