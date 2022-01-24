# ----- I M P O R T S ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
import sys, getpass, traceback
import warnings 

import pandas as pd
import numpy as np
# from sklearn.linear_model import LinearRegression

from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from dotenv import dotenv_values
from Client import Client # can be found in same dir as this file in repositorie

# ----- M E T A D A T A ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

__version__ = "v1.0.0"
__description__ = "Script to fetch Pepper data and create .pdf containing weekly report"
__author__ = "Benjamin Thomas Schwertfeger"
__copyright__   = "Benjamin Thomas Schwertfeger"
__email__ = "development@b-schwertfeger.de"
__status__ = "Production"
__repo__ = "https://github.com/ProjectPepperHSB/Backend-Services.git"

# ----- S E T T I N G S ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

if sys.platform == "linux" or sys.platform == "linux2":
    out_dir = f"/home/docker-hbv-kms/weekly-reports"
elif sys.platform == "darwin":
    out_dir = f"/Users/{getpass.getuser()}/repositories/Backend-Services/analysis/out"
elif sys.platform == "win32":
    exit() # enter your windows path path

warnings.filterwarnings("ignore")

plt.rcParams["figure.figsize"] = [10, 6]
plt.rcParams["savefig.bbox"] = "tight"
plt.style.use("fivethirtyeight")

_red, _orange, _gray, _green, _blue = "#fc4f30", "#e5ae38", "#8b8b8b", "#6d904f", "#30a2da"
_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
# ----- ----- -----
LOOKBACK = 7 #days

now = datetime.now()
start_date = (now - timedelta(days=LOOKBACK)).strftime("%Y-%m-%d")
out_fname = f"weekly_report_{start_date}_-_{now.strftime('%Y-%m-%d')}.pdf"

# ----- S E T U P ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

not_understand_df, emotion_states_df, use_case_df = None, None, None

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

def init():
    global not_understand_df, emotion_states_df, use_case_df

    try:
        config = dotenv_values(".env") 
        API_KEY = config["API_KEY"]
    except KeyError:
        print("No .env file with API_KEY found!")
        exit()

    try:
        client = Client(API_KEY, sandbox=False, verbose=1) # create client to connect with web-app 

        query_str = f"WHERE ts > NOW() - INTERVAL {LOOKBACK} day"
        
        not_understand_df = pd.DataFrame(data=client.sql_query(f"SELECT * FROM pepper_did_not_understand_table {query_str}"))
        emotion_states_df = pd.DataFrame(data=client.sql_query(f"SELECT * FROM pepper_emotion_table {query_str}"))
        use_case_df = pd.DataFrame(data=client.sql_query(f"SELECT * FROM pepper_use_case_table {query_str}"))

        # preprocessing
        emotion_states_df["dialog_time"] = np.array([x for x in emotion_states_df["dialog_time"]]).astype("float32")
    except:
        print(f"Could not fetch data from backend!\n{traceback.format_exc()}")
        print("Check your internet connection and check if the backend service is running!")
        exit()

def plots(pdf):
    # PIE ----- USE-CASE-USAGE -----
    plt.figure()
    fig = use_case_df["use_case"].value_counts().plot(kind="pie", autopct="%1.1f%%").get_figure()
    plt.title("Use-Case usage"); plt.axis("off"); pdf.savefig(fig)

    # PIE ----- GENDER-DISTRIBUTION -----
    plt.figure()
    fig = emotion_states_df.gender.value_counts().plot(kind="pie", autopct="%1.1f%%",colors = [ _red, _blue ]).get_figure()
    plt.title("Gender distribution"); plt.axis("off"); pdf.savefig(fig)      

    # PIE ----- BASIC-EMOTION -----
    plt.figure()
    fig = emotion_states_df["basic_emotion"].value_counts().plot(kind="pie", autopct="%1.1f%%",colors = [ _gray, _red, _orange, _green]).get_figure()
    plt.title("Distribution of basic emotion occurrence"); plt.axis("off"); pdf.savefig()

    # BARH ----- DISTRIBUTION OF EMOTION BY GENDER -----
    plt.figure()
    fig = pd.concat(
        [emotion_states_df[["gender", "basic_emotion"]].pivot_table(index=["gender"], columns=col, aggfunc=len) for col in ["basic_emotion"]], axis = 1
    ).fillna(0).plot(kind = "barh", color = { "bad": _red, "bored": _gray, "excited": _orange, "good": _green }).get_figure()
    plt.title("Distributions of basic emotions grouped by gender"); plt.xlabel("count"); pdf.savefig()

    # BARH ----- DISTRIBUTION OF PLEASURE STATES ------
    plt.figure()
    fig = pd.concat(
        [emotion_states_df[["gender", "pleasure_state"]].pivot_table(index=["gender"], columns=col, aggfunc=len) for col in ["pleasure_state"]], axis=1
    ).fillna(0).plot(kind="barh", color={ "bad": _red, "medium": _gray, "good": _orange, "perfect": _green })
    plt.title("Distribution of pleasure states grouped by gender"); pdf.savefig()

    # ----- STATISTICS BY DAY OF WEEK ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ------ ----- ----- ----- ----- 
    d = emotion_states_df[["distance", "gender", "age", "basic_emotion", "pleasure_state", "excitement_state", "smile_state", "dialog_time", "ts"]]
    d_use_case = use_case_df[["use_case", "ts"]]

    for i, ts in enumerate(d["ts"]):
        date_obj = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.000Z")
        d["ts"][i] = f"{date_obj.day}.{date_obj.month}.{date_obj.year} {date_obj.hour}:{date_obj.minute}"
    for i, ts in enumerate(d_use_case["ts"]):
        date_obj = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.000Z")
        d_use_case["ts"][i] = f"{date_obj.day}.{date_obj.month}.{date_obj.year} {date_obj.hour}:{date_obj.minute}"
        
    d["weekday"] = [datetime.strptime(ts, "%d.%m.%Y %H:%M").weekday() for ts in d["ts"]]
    d_use_case["weekday"] = [datetime.strptime(ts, "%d.%m.%Y %H:%M").weekday() for ts in d_use_case["ts"]]
    
    # BAR ----- EMOTIONS BY WEEKDAY
    plt.figure()
    fig = pd.concat(
        [d[["weekday", "basic_emotion"]].pivot_table(index=["weekday"], columns=col, aggfunc=len) for col in ["basic_emotion"]], axis = 1
    ).fillna(0).plot(kind = "bar", color = { "bad": _red, "bored": _gray, "excited": _orange, "good": _green }, rot = 35)

    plt.title("Distribution of basic emotions grouped by weekday")
    plt.xticks(np.arange(len(plt.gca().get_xticklabels())), [_weekdays[int(i.get_text())] for i in plt.gca().get_xticklabels()])
    plt.xlabel("weekday"); plt.ylabel("count"); pdf.savefig()

    # BAR ----- GENDER BY WEEKDAY
    plt.figure()    
    fig = pd.concat(
        [d[["weekday", "gender"]].pivot_table(index=["weekday"], columns=col, aggfunc=len) for col in ["gender"]], axis = 1
    ).fillna(0).plot(kind = "bar", rot = 35)

    plt.title("Usage by gender and weekday")
    plt.xticks(np.arange(len(plt.gca().get_xticklabels())), [_weekdays[int(i.get_text())] for i in plt.gca().get_xticklabels()])
    plt.xlabel("weekday"); plt.ylabel("count"); pdf.savefig()

    # BAR ----- Dialog time by weekday
    plt.figure()
    fig = d[["weekday", "dialog_time"]].groupby("weekday").mean().plot(kind="bar", rot=35)
    plt.title("Mean dialog time by weekday")
    plt.xticks(np.arange(len(plt.gca().get_xticklabels())), [_weekdays[int(i.get_text())] for i in plt.gca().get_xticklabels()])
    plt.xlabel("weekday"); plt.ylabel("dialog time in minutes"); pdf.savefig()

    plt.figure()
    fig = pd.concat(
        [d_use_case[["weekday", "use_case"]].pivot_table(index=["weekday"], columns=col, aggfunc=len) for col in ["use_case"]],axis = 1
    ).fillna(0).plot(kind = "bar", rot = 35)

    plt.title("Use case by weekday")
    plt.xticks(np.arange(len(plt.gca().get_xticklabels())), [_weekdays[int(i.get_text())] for i in plt.gca().get_xticklabels()])
    plt.xlabel("weekday")
    plt.ylabel("count")
    pdf.savefig()

    # ----- ----- ------ ----- ----- ----- ----- ----- ----- ------ ----- ----- ----- ----- ----- ----- ------ ----- ----- ----- ----- 

    # SCATTER ----- LINEAR REGRESSION -----
    # maybe not representative enough for 7 day period
    
    # data = emotion_states_df[["distance", "age", "gender", "basic_emotion", "pleasure_state", "excitement_state", "smile_state", "dialog_time"]]
    # X = data.iloc[:, 1].values.reshape(-1, 1).astype("int") # age
    # Y = data.iloc[:, -1].values.reshape(-1, 1).astype("float32") # dialog_time
    # linear_regressor = LinearRegression(); linear_regressor.fit(X, Y) 
    # Y_pred = linear_regressor.predict(X)  

    # plt.figure()
    # fig = plt.scatter(X, Y)
    # plt.plot(X, Y_pred, color="red")
    # plt.xlabel("age"); plt.ylabel("dialog time")
    # plt.title("Linear regression on dialog time and age")
    # pdf.savefig()


def main():
    init()

    with PdfPages(f"{out_dir}/{out_fname}") as pdf:
        plots(pdf)
        
        # metadata
        d = pdf.infodict()
        d["Title"] = f"Weekly report {start_date} - {now}"
        d["Author"] = "Team Pepper"
        # d["Subject"] = "...."
        d["Keywords"] = "pepper robot matplotlib plots report"
        d["CreationDate"] = now.strftime('%Y-%m-%d')


if __name__ == "__main__":
    main()
