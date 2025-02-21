import subprocess
import os

class builder():
    def convert(input_file, output_file):
        if not os.path.exists(input_file):
            print(".cpp file was successfully located.")
            return

        command = [
            "g++", "-shared", "-o", output_file, "-fPIC", input_file
        ]

        try:
            print('compiling file...')
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(f'successfully compiled .cpp file as {output_file}')
        except subprocess.CalledProcessError as e:
            print(f'error, problem, :     {e}')


"""
the "builder" converts the .cpp files into a .dll file.
"""