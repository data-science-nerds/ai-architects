'''Not yet implemented, only adding as a potential feature.'''

import pandas as pd
from datetime import datetime
import socket

#...in app.py in def demo_customized_chatbot() where
# we process the question and response...

def append_user_questions():
    '''Collects info from user'''
    # Load existing data
    try:
        df = pd.read_csv('chatbot_data.csv')
    except pd.errors.EmptyDataError:
        # If the CSV does not exist or is empty, create a new DataFrame
        df = pd.DataFrame(columns=['Question', 'Answer', 'Datetime', 'IP Address'])

    # Get the current time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get the IP address
    ip_address = socket.gethostbyname(socket.gethostname())

    # Add the new data as a row to the DataFrame
    df = df.append({
        'Question': question,
        'Answer': response,
        'Datetime': current_time,
        'IP Address': ip_address
    }, ignore_index=True)
    return True

# Write the DataFrame to a CSV
df.to_csv('chatbot_data.csv', index=False)

if __name__ == "__main__":
    res = False
    res = append_user_questions()