# ai-architects
chatbots and such


### LOCAL DEVELOPMENT AND DEBUGGING
to run Flask app:
# ssh into ec2 instance on aws
ssh -i /Users/elsa/Documents/CODE/aiarchitects/ai-architects-flask-key-pair.pem ubuntu@ec2-3-92-237-8.compute-1.amazonaws.com

# make sure there are no current instances
lsof -i :5000
# if there are, kill them
kill -9 <pid>

# run from root
```
python3 app.py --port 5000
```


To run as code, run entire process by command line :

```
python3 customized-by-user-chatbot.py
```


# fixes for common bugs

## permissions
## would use sudo in aws instance
chmod u+rwx /Users/elsa/Documents/CODE/aiarchitects/data-science-nerds