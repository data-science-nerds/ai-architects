# ai-architects
chatbots and such

http://127.0.0.1:5000/demo-customized-chatbot
# RUNNING EC2  IN AWS (CLOUD)
```gunicorn wsgi:app```

<!-- RUN WITH DAEMON and 4 workers-->
```gunicorn -w 4 wsgi:app -D```

<!-- Run using gunicorn.conf.py-->
```   gunicorn -c gunicorn.conf.py app:app```

# Authenitcation
No MFA is used for purposes of demo, however is recommended for customers.  Cognito user pool handles logins via AWS security protocols.  No additional required attribues or custom attributes are used for simplicity of the demo.


# why not curie over davinci considering costs:
Curie	$0.0030 / 1K tokens	$0.0120 / 1K tokens
Davinci	$0.0300 / 1K tokens	$0.1200 / 1K tokens
However, majority of questions are answered as user's data is displayed for this use case.
Thus, the gains in savings per questions are not significant enough to warrant
further trimming down the primed prompt, as most users likely will not have further questions.
The preferred outcome is that the model performs the best possible, linguistically,
so the user does not need to call the rental property.
Cost comparison shows that a user will be less likely to ask more quesitons if their unique data is displayed prior to them asking further questions, but to have an employee answer the phone and respond will far be more costly than to pay the extr dime for a superior model.

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