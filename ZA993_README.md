# ZA993 — Deutscher Sprachroboter

ZA993 ist ein einfacher deutscher Sprachassistent mit Texteingabe und optionalem Mikrofonmodus.

## Installation

```bash
python -m pip install -r requirements.txt
```

Für die Spracherkennung über das Mikrofon wird zusätzlich ein unterstütztes Mikrofon mit passenden Betriebssystem-Treibern benötigt.

## Start

Textmodus:

```bash
python za993_robot.py
```

Mikrofonmodus:

```bash
python za993_robot.py --voice
```

## Befehle

- Hallo
- Wie heißt du?
- Wie spät ist es?
- Welches Datum ist heute?
- Stopp
