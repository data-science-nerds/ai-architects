# import subprocess
from flask import (
    Flask, request, render_template, jsonify, session, redirect, url_for, g)
from flask_session import Session
# from flask_cognito import cognito_auth_required, CognitoAuthManager, current_cognito_jwt

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
app.config['PERMANENT_SESSION_LIFETIME'] = 300  # session timeout in seconds
app.config['SESSION_REFRESH_EACH_REQUEST'] = False
Session(app)



@app.before_request
def before_request_func():
    session.permanent = True
    if 'documents_contents' not in session:
        g.documents_contents = customized.load_documents_contents(directory_path_already_to_text)

        session['documents_contents'] = g.documents_contents

@app.route("/demo-customized-chatbot", methods=['GET', 'POST'])
def demo_customized_chatbot():
    if 'questions' not in session:
        session['questions'] = []

    # Initialize documents here
    documents = session.get('documents', [])  # Use the documents from the session if available, otherwise default to an empty list
    # list unique user's session info despite GET or POST methods
    session['documents'] = documents  # Store the documents in the session for use in subsequent requests

    # Use the documents_contents from the g object
    # documents_contents = g.get('documents_contents', [])
    # # Load the documents_contents here
    documents_contents = customized.load_documents_contents(directory_path_already_to_text)



    if request.method == 'POST':
        question = request.form['question']
        
        # Write the question to a file as a simple way to store types of questions
        # For a production environment depending on client use case, could save
        # using SQLAlchemy
        with open('chatbot_things/data_handling/collect_user_input/user_questions.txt', 'a') as f:
            f.write(question + '\n')
        # limit user input to protect api calls, only answer questions relevant to topic
        # Append additional instructions to the question, but 
        # do not make it visible to user
        instructions = " Only respond regarding information related to the CONTEXT INFORMATION."
        question += instructions
        
        index, documents, directory_path, documents_contents = customized.construct_index(directory_path_already_to_text)
        question_count = len(session['questions'])
        
        if question_count >= 9:
            session.permanent = True
            return jsonify({'response': 'Maximum number of questions reached. Session is inactive as one line of defense for the use of this demo api.'})

        response, _ = customized.ask_ai(question, index, documents, question_count)
        session['questions'].append((question, response))
        session['documents'] = documents
        session['documents_contents'] = documents_contents  # Store the documents_contents in the session for use in subsequent requests
        session.modified = True  # Ensures the session is marked for saving
        return redirect(url_for('demo_customized_chatbot', directory_path=directory_path))
    else:
        questions = session['questions']
        directory_path = request.args.get('directory_path', '')  # Get the directory_path from the URL if available
        session.permanent = True
        return render_template('chatbot.html', questions=questions, documents=documents, directory_path=directory_path, documents_contents=documents_contents)


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