import os
import subprocess
from django.core.management.commands.runserver import Command as RunserverCommand


class Command(RunserverCommand):
    def handle(self, *args, **options):
        streamlit_path = os.path.join(os.path.dirname(__file__), '../../../decode/app.py')
        streamlit_process = subprocess.Popen(['streamlit', 'run', streamlit_path], stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)

        try:
            super().handle(*args, **options)
        finally:
            streamlit_process.terminate()

