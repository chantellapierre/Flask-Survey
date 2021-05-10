from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

debug = DebugToolbarExtension(app)
# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = '<victorias-secret>'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


RESPONSES_KEY = 'responses'

@app.route('/')
"""Show user homepage"""
def start():
    return render_template('start.html', survey=survey)


@app.route('/survey', methods=['POST'])
"""Show user beginning of survey"""
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')


@app.route('/questions/<int:qid>')
"""Show user survey questions"""
def show_question(qid):
     responses = session.get(RESPONSES_KEY)
     question = survey.questions[qid]

    if (len(responses) == len(survey.questions)):
        # Survey complete, all questions answered
        return redirect("/complete")

    if (len(responses) != qid):
        # Deny access of questions out of order
        flash(f"Sorry, you're trying to access an invalid question (id:{qid})")
        return redirect(f"/questions/{len(responses)}")

    if (responses is None):
        # Empty answer
        return redirect("/")

    return render_template(
        "question.html", question_num=qid, question=question)


@app.route("/answer", methods=['POST'])
"""Save user answers to survey questions"""
    def save_answer():
        answer=request.form["answer"]

    # Add response to session
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # Handle completed survey
        return redirect("/completed")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def complete():
    """Show survey completed page"""

    return render_template("completed.html")