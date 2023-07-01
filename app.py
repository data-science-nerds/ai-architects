import subprocess
from flask import Flask, request, render_template
import os
import sys
import signal

# use customization code
# from . import individuals_customized_chatbot as customized
import individuals_customized_chatbot as customized

from utilities.relative_paths import (
    directory_path_already_to_text,
    directory_path_incoming_pdfs,
)

app = Flask(__name__)


def handle_child_termination(signum, frame):
    while True:
        try:
            # Reap the exit status of child processes
            pid, status = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break  # No more child processes to reap
            # Handle the exit status as needed
            print(f"Child process {pid} terminated with exit status {status}")
        except ChildProcessError:
            break

# Register the signal handler to handle child termination
signal.signal(signal.SIGCHLD, handle_child_termination)

# Flask route for spawning child process
@app.route('/spawn_child_process')
def spawn_child_process():
    # Spawn a child process
    child_pid = os.fork()
    if child_pid == 0:
        # Child process logic
        sys.exit(0)  # Terminate the child process

    return 'Child process spawned successfully.'

# Flask route for other functionality
@app.route('/')
def index():
    # Your other Flask app logic
    return 'Hello, World!'

@app.route('/')
def command_line_interface():
    command = request.args.get('command')
    if command:
        output = subprocess.check_output(command, shell=True)
    else:
        output = None
    return render_template('command_line.html', output=output)


@app.route("/demo-customized-chatbot")
def demo_customized_chatbot():
    index, documents = customized.construct_index(directory_path_already_to_text)
    customized.ask_ai(documents)
    


if __name__ == '__main__':
    app.run(debug=True)
