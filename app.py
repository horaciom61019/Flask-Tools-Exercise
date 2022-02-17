from flask import Flask, flash, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret" 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route("/")
def start_page():
    """ Survey start page """

    return render_template("start_page.html", survey=survey)


# On "start" click, redirect to first question
@app.route("/begin", methods=["POST"])
def start_survey():
    """ Clear the session """
    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """ Show current question """

    responses = session.get(RESPONSES_KEY)

    # Get question data from Survery 
    question = survey.questions[qid]

    if responses is None:
        # Attempt to access future questions
        return redirect("/")

    elif len(responses) == len(survey.questions):
        # Completed questions
        return redirect("/complete")

    elif len(responses) != qid:
        # Attempt to answer question out of order
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    return render_template("question.html", question_num=qid, question=question)


@app.route("/answer", methods=["POST"])
def handle_question():
    """ Save response and redirect to next question"""

    # Get response 
    choice = request.form['answer']

    # Add response to session's responses
    response = session[RESPONSES_KEY]
    response.append(choice)
    session[RESPONSES_KEY] = response

    if len(response) == len(survey.questions):
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(response)}") 


@app.route("/complete")
def complete():
    """ Show survey completion page """

    return render_template("complete.html")