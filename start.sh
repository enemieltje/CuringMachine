python -m venv ./.venv

./.venv/bin/pip install gpiozero    # Button input
./.venv/bin/pip install hx711       # Load cell
./.venv/bin/pip install picamera2   # Camera

./.venv/bin/python ./src/main.py
