import subprocess
from flask import Flask, request, render_template, jsonify, session
from flask import Flask, render_template, request, session, redirect, url_for
import os
import sys
import signal

import chatbot_things.individuals_customized_chatbot as customized

from chatbot_things.utilities.relative_paths import (
    directory_path_already_to_text,
    directory_path_incoming_pdfs,
)

app = Flask(__name__, template_folder='flask_things/templates', static_folder='flask_things/static')
flask_key = os.getenv("FLASK_KEY")
app.secret_key = flask_key
app.config['SESSION_TYPE'] = 'filesystem'


@app.route("/demo-customized-chatbot", methods=['GET', 'POST'])
def demo_customized_chatbot():
    if 'questions' not in session:
        session['questions'] = []

    if request.method == 'POST':
        question = request.form['question']
        index, documents = customized.construct_index(directory_path_already_to_text)
        question_count = len(session['questions'])
        
        if question_count >= 9:
            return jsonify({'response': 'Maximum number of questions reached.'})

        response, _ = customized.ask_ai(question, index, documents, question_count)
        session['questions'].append((question, response))
        session.modified = True  # Ensures the session is marked for saving
        return redirect(url_for('demo_customized_chatbot'))  # Redirect to GET request
    else:
        questions = session['questions']
        return render_template('chatbot.html', questions=questions)



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
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
