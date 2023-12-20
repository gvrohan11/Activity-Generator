import requests
from flask import Flask, jsonify, render_template, request, send_file, url_for, redirect

app = Flask(__name__)

activity = {}


'''
activity
accessibility (text)
type
participants (text)
cost
'''

# activity (no label), accessibility (), type, participants, price

'''
"activity": "Learn Express.js",
"accessibility": 0.25,
"type": "education",
"participants": 1,
"price": 0.1,
"link": "https://expressjs.com/",
"key": "3943506"
'''

def generate_url(selected_type, selected_access, seletected_participants, selected_price):
    url = "http://www.boredapi.com/api/activity/"

    added = False

    if selected_type != "":
        url += f"?type={selected_type}"

    if selected_access != "":
        to_add = ""
        if selected_access == "0":
            to_add = "maxaccessibility=0.1"
        elif selected_access == "1":
            to_add = "minaccessibility=0.1&maxaccessibility=0.3"
        elif selected_access == "2":
            to_add = "minaccessibility=0.3&maxaccessibility=0.6"
        elif selected_access == "3":
            to_add = "minaccessibility=0.6&maxaccessibility=0.85"
        else:
            to_add = "minaccessibility=0.85"
        
        if added:
            url += f"&{to_add}"
        else:
            url += f"?{to_add}"
            added = True

    if seletected_participants != "":
        if added:
            url += f"&participants={seletected_participants}"
        else:
            url += f"?participants={seletected_participants}"
            added = True

    if selected_price != "":
        if added:
            url += f"&maxprice={selected_price}"
        else:
            url += f"?maxprice={selected_price}"
            added = True

    return url

@app.route("/")
def init():
    return render_template("index.html")

@app.route("/generate", methods=["GET"])
def generate_get():
    
    return render_template("generate.html"), 200

@app.route("/generate", methods=["POST"])
def generate_post():
    global activity

    url = "http://www.boredapi.com/api/activity/"

    selected_type = request.form.get("type")
    # if selected_type != "":
    #     url += f"?type={selected_type}"

    selected_access = request.form.get("accessibility")

    url = generate_url(selected_type, selected_access, "", "")


    response = []

    try:
        response = requests.get(url)
    except:
        return "Error: Could not connect to API", 400
    
    # print(response.status_code)
    
    info = response.json()

    # print(info)

    if info["error"]:
        print(info)
        return redirect('/bad_results')

    activity["activity"] = info["activity"]

    description = ""

    acc = info["accessibility"]
    if acc <= 0.1:
        description = "fully accessible"
    elif acc <= 0.3:
        description = "very accessible"
    elif acc <= 0.6:
        description = "moderately accessible"
    elif acc <= 0.85:
        description = "slightly accessible"
    else:
        description = "almost not accessible, unfortunately"

    activity["accessibility"] = f"This activity is {description}"

    activity["type"] = info["type"].capitalize()

    activity["participants"] = f"This activity requires {info['participants']} participants"

    activity["price"] = "{:.2f}".format(info['price'])


    return redirect('/good_results')

@app.route("/bad_results", methods=["GET"])
def result_status_get():
    global activity

    return render_template("bad_results.html"), 200

@app.route("/good_results", methods=["GET"])
def results_get():
    global activity

    return render_template("good_results.html", activity=activity), 200