from django.core.management.base import BaseCommand
import subprocess
from pathlib import Path

class Command(BaseCommand):
    help = 'Run multiple Streamlit apps'

    def handle(self, *args, **options):
        apps = [
            ("decode/streamlit_apps/g1.py", 8501),
            ("decode/streamlit_apps/g3.py", 8502),
            ("decode/streamlit_apps/g4.py", 8503),
            ("decode/streamlit_apps/g5.py", 8504),
            ("decode/streamlit_apps/g6.py", 8505),
            ("decode/streamlit_apps/g7.py", 8506),
            ("decode/streamlit_apps/g8.py", 8507),
            # Add more apps as needed
        ]

        for app, port in apps:
            subprocess.Popen(['streamlit', 'run', app, '--server.port', str(port)])

        self.stdout.write(self.style.SUCCESS('Successfully started all Streamlit apps'))


