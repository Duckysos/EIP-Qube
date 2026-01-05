# EIP Qube

Voice-driven “Qube” assistant that wakes on a custom Picovoice Porcupine keyword, records speech until silence with Cobra VAD, sends the audio to a remote `/audio_to_audio` API, and plays back the returned response alongside looping character videos. A FastAPI layer exposes endpoints to start/stop the lesson loop.

## Features
- Wake word (“Hello Cube”) detection via Picovoice Porcupine.
- Voice activity detection to capture speech until silence (Cobra).
- Sends recorded WAV to a backend (`/audio_to_audio`) and plays the returned audio.
- Lesson control endpoints (`/start_lesson`, `/end_lesson`) for kiosk-style operation.
- Video playback and audio cues (PowerOn/PowerOff, character animations).

## Project Layout
- `Qube/Qube.py` — FastAPI app + full lesson loop (Raspberry Pi paths).
- `Qube/QubeLaptop.py` — Laptop variant of the conversation loop.
- `Qube/GPT CUbe.py`, `Qube/pvcobrademo.py`, `Qube/porcupinedemo.py`, `Qube/audio_recording.py`, `Qube/playsound.py`, `Qube/playvideo.py`, `Qube/playveedeo.py` — demos/utilities for audio/video, wake word, and VAD.
- `Qube/Hello-Cube_en_*.ppn` — Picovoice custom keyword files.
- `videos/*`, `PowerOn.wav`, `PowerOff.wav`, `audio.wav` — media assets used in the experience.

## Prerequisites
- Python 3.9+ recommended.
- System deps: PortAudio (for PyAudio), ffmpeg (for pydub), VLC (for python-vlc).
- Microphone and speakers.
- Picovoice access key and the custom keyword `.ppn` file.
- Backend that accepts `POST /audio_to_audio` with `multipart/form-data` audio and returns WAV.

## Installation
```bash
pip install pvcobra pvporcupine pyaudio pydub python-vlc fastapi uvicorn requests numpy
# Ensure ffmpeg and VLC are installed on the system
