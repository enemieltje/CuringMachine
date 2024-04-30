mkdir logs
mv logs/latest.log logs/old.log
touch logs/latest.log

python -m venv --system-site-packages ./.venv

./.venv/bin/pip install numpy --upgrade
./.venv/bin/pip install lgpio pigpio gpio
./.venv/bin/pip install gpiozero    # Button input
./.venv/bin/pip install hx711       # Load cell
./.venv/bin/pip install picamera2   # Camera

./.venv/bin/python ./src/main.py
