from flask import Flask, request
import flask
from openai import OpenAI
from markupsafe import escape
import re
import json

OPENAI_API_KEY = "PASTE_YOUR_API_KEY_HERE"

client = OpenAI(api_key = OPENAI_API_KEY)

def get_review_info(review: str):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": '''Score the sentiment of the following review from 0 to 10, where 0 is "this product/place is absolutely awful" and 10 is "this product/place is perfect".  Do not include extra commentary. Output a json object with the following keys:
- "score" - a string that contains the score mentioned earlier
- "positive" - a list of quotes from the review about what the person liked.
- "negative" - a list of quotes from the review about what the person did not like. Quote things about the service that were disliked - that way, the operator of the service can see what to improve on.
The positive and negative lists may be empty if nothing is mentioned in the review. Try to have at least 2-3 entries in each list. Limit the number of quotes to 5 per list.
The review is as follows:''',
            },
            {
                "role": "user",
                "content": review,
            },
        ],
        max_tokens=256,
        stop="REVIEW_FINISHED",
    )

    content = completion.choices[0].message.content
    
    return content

def get_review_info_debug(review: str):
    return """{
  "score": "3",
  "positive": [
    "The world of Pandora was cool.",
    "The Tree of Life, cool."
  ],
  "negative": [
    "Be prepared to walk an ungodly distance",
    "experience less magic than you should for the cost and amount of time you put in",
    "not that spectacular",
    "seems like such a money-making pit",
    "need a day for each park",
    "stay at one of the Disney hotels- which cost an arm and a leg",
    "more walking and wasting time"
  ]
}"""



def process_review(review: str):
    review = escape(review)

    raw = get_review_info(review)
    
    data = json.loads(raw)
    
    score = data.get("score", "??")
    
    hdisp = review
    
    for goodquote in data.get("positive", []):
        hdisp = re.sub(re.escape(goodquote), "$sg$\g<0>$sc$", hdisp, re.I)
    
    for badquote in data.get("negative", []):
        hdisp = re.sub(re.escape(badquote), "$sb$\g<0>$sc$", hdisp, re.I)
    
    return score, hdisp
    

app = Flask(__name__)

def create_static_route(route: str):
    app.route("/" + route, endpoint="gened_" + route)(lambda: flask.send_file("static/" + route))

static_routes = [
    "mainpage.html",
    "style.css",
    "background.png",
]

for route in static_routes:
    create_static_route(route)

@app.route("/")
def root():
    return flask.redirect("/mainpage.html")

@app.route("/results", methods=["GET", "POST"])
def api():
    if request.method == "GET" or request.form.get('review', None) is None:
        return flask.redirect("/mainpage.html")

    with open("static/results.html", "r") as f:
        tpl = f.read()
    
    try:
        score, hformat = process_review(request.form['review'])
    except json.JSONDecodeError:
        # json decode failed
        
        return "<h1>Failed to process this review. Please try another review.</h1><a href=\"/\">Back to home</a>"
        
    
    tpl = tpl.replace("{{results.score}}", escape(score))
    tpl = tpl.replace("{{results.highlightedtext}}", hformat)
    tpl = tpl.replace("$sg$", '<span class="liked">')
    tpl = tpl.replace("$sb$", '<span class="disliked">')
    tpl = tpl.replace("$sc$", '</span>')

    return tpl

@app.route("/joinus.html")
def joinus():
    return "<h1>Site under construction</h1>"
