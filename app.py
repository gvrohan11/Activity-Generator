import requests
from flask import Flask, jsonify, render_template, request, send_file, url_for, redirect

app = Flask(__name__)

activity = {}

status = ""

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

def generate_url(selected_type, selected_access, seletected_participants, min_budget, max_budget):
    url = "http://www.boredapi.com/api/activity/"

    added = False

    if selected_type != "":
        url += f"?type={selected_type}"
        added = True

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
    
    if min_budget != "":
        if added:
            url += f"&minprice={min_budget}"
        else:
            url += f"?minprice={min_budget}"
            added = True
    
    if max_budget != "":
        if added:
            url += f"&maxprice={max_budget}"
        else:
            url += f"?maxprice={max_budget}"
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

    global status

    print("here?")

    # url = "http://www.boredapi.com/api/activity/"

    selected_type = request.form.get("type")
    print(selected_type)

    selected_access = request.form.get("accessibility")
    print(selected_access)

    selected_participants = request.form.get("people")
    print(selected_participants)

    min_budget = request.form.get("min_budget")
    max_budget = request.form.get("max_budget")

    if min_budget != "" or max_budget != "":
        try:

            if min_budget != "":
                min_budget = float(min_budget)
                print(min_budget)

            if max_budget != "":
                max_budget = float(max_budget)
                print(max_budget)

        except:
            print("not a valid budget")
            status = "Not a valid budget"
            return redirect('/bad_results')

    # min_budget = request.form.get("min_budget")
    # print(min_budget)

    # max_budget = request.form.get("max_budget")
    # print(max_budget)

    if max_budget < min_budget and max_budget != "":
        # include a string here
        print("min budget must be less than max budget")
        status = "Min budget must be less than max budget"
        return redirect('/bad_results')
    
    if max_budget != "" and min_budget != "" and (max_budget < 0 or min_budget < 0):
        print("budget cannot be negative")
        status = "Budget cannot be negative"
        return redirect('/bad_results')

    url = generate_url(selected_type, selected_access, selected_participants, min_budget, max_budget)

    print(url)

    response = []

    try:
        response = requests.get(url)
    except:
        return "Error: Could not connect to API", 400
    
    # print(response.status_code)
    
    info = response.json()

    # print(info)

    if "error" in info:
        print(info)
        status = "No activities found in Bored API database with those parameters"
        print(status)
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

    activity["participants"] = f"# of Participants: {info['participants']}"

    activity["price"] = "{:.2f}".format(info['price'])


    return redirect('/good_results')

@app.route("/bad_results", methods=["GET"])
def result_status_get():
    global activity

    global status

    print(f"bad results status: {status}")

    return render_template("bad_results.html", status=status), 200

@app.route("/good_results", methods=["GET"])
def results_get():
    global activity

    return render_template("good_results.html", activity=activity), 200