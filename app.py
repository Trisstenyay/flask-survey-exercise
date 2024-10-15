from flask import Flask, request, render_template, redirect, url_for, flash, session

from surveys import satisfaction_survey

app = Flask(__name__)
app.secret_key = 'flash_messages'  # You can use any string





@app.route('/')
def start_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("instructions.html", title=title, instructions=instructions)



@app.route('/middleware', methods=["POST"])
def middleware():
    if request.method == 'POST':
        if 'responses' not in session:
            session['responses'] = []
    return redirect(url_for('question', question_number=len(session['responses'])))
    



@app.route('/questions/<int:question_number>', methods= ["GET", "POST"])
def question(question_number):
    print('question', len(session['responses']))
    print('question2', question_number)
    # Check if the user has answered all questions
    if len(session['responses']) == len(satisfaction_survey.questions):
        return redirect(url_for('thank_you'))
    
    # # Check if the question number in the URL is out of range
    if question_number >= len(satisfaction_survey.questions):
    #     # Redirect to the correct question if it doesn't exist
        flash("Invalid question number!")
        return redirect(url_for('question', question_number=len(session['responses'])))
    
    #  # Check if the user is trying to access a question they haven't reached yet
    if question_number != len(session['responses']):
        return redirect(url_for('question', question_number=len(session['responses'])))
    
    question = satisfaction_survey.questions[question_number]
    return render_template('questions.html', question=question, question_number=question_number)
    


@app.route('/answer', methods= ["POST"])
def answer():
    if request.method == "POST":
        value = request.form.get('answer')
        
        if 'responses' in session:
            responses = session['responses']
            responses.append(value)
            session['responses'] = responses
    return redirect(f'/questions/{len(session["responses"])}')


    

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')



