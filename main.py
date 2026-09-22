import os
import subprocess
import sys


def run(command):
    subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    port = os.getenv("PORT", "80")
    run(f"{sys.executable} manage.py migrate --noinput")
    run(f"{sys.executable} manage.py collectstatic --noinput")
    os.execvp(sys.executable, [sys.executable, "-m", "gunicorn", "app_manager.wsgi:application", "--bind", f"0.0.0.0:{port}"])
