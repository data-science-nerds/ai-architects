import subprocess
from flask import Flask, request, render_template
import os
import sys
import signal

# use customization code
# from . import individuals_customized_chatbot as customized
import chatbot_things.individuals_customized_chatbot as customized

from chatbot_things.utilities.relative_paths import (
    directory_path_already_to_text,
    directory_path_incoming_pdfs,
)

from flask import Flask, request, render_template, jsonify
# other imports...

app = Flask(__name__, template_folder='flask_things/templates', static_folder='flask_things/static')

@app.route("/demo-customized-chatbot", methods=['GET', 'POST'])
def demo_customized_chatbot():
    if request.method == 'POST':
        question = request.form['question']
        index, documents = customized.construct_index(directory_path_already_to_text)
        question_count = 0  # Define question_count here
        response, question_count = customized.ask_ai(question, index, documents, question_count)
        return jsonify({'response': response})
    else:
        return render_template('chatbot.html')



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

@app.route('/')
def index():
    # Your other Flask app logic
    return render_template('index.html')

@app.route('/command', methods=['GET', 'POST'])
def command_line_interface():
    if request.method == 'POST':
        command = request.form['command']
        try:
            output = subprocess.check_output(command, shell=True).decode('utf-8')
        except subprocess.CalledProcessError as e:
            output = str(e)
    else:
        output = ''
    return render_template('command_line.html', output=output)




if __name__ == '__main__':
    app.run(debug=True)
