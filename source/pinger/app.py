import time
import threading
import schedule
import os
import sys
from flask import Flask
from pinger import Pinger
from pathlib import Path

app = Flask(__name__)

airtablePinger = Pinger("http://airtable.com/", 5, 2, 1, [], [])
airtablePinger.scheduleBackgroundJob()

dataDotWorldPinger = Pinger("http://data.world/", 10, 2, 1, [], [])
dataDotWorldPinger.scheduleBackgroundJob()

@app.route('/')
def index():
    return 'hello world'

@app.route('/airtable')
def doAirtable():
    if airtablePinger.singleGet():
        return "It worked!  Airtable returned!"

def runBackgroundTasksContinuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                print("Let's run scheduled jobs")
                Path('/tmp/foo').touch()
                schedule.run_pending()
                time.sleep(interval)
    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

if __name__ == "__main__":
    cease_continous_run = runBackgroundTasksContinuously()
    app.run(host='0.0.0.0', port=8080)
    cease_continous_run.set()