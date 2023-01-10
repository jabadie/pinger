import time
import threading
import schedule
import os
import sys
from flask import Flask, abort
from pinger import Pinger
from pathlib import Path

# This is a simple service that runs regular requests to different URLS and reports results

app = Flask(__name__)

# TODO pull this data from a DB if not running locally
pingMonitors = {
    "airtable" :  Pinger("http://airtable.com/", 60, 2, 1, [], []),
    "dataDotWorld": Pinger("http://data.world/", 300, 2, 1, [], []),
    "foobar": Pinger("http://foo.bar", 300, 2, 1, [],[] )
}

# TODO: move this to a template
def generateIndexOfTriggers():
    output = ['<body><ul>']
    for monitor in pingMonitors.keys():
        output.append(f"<li><a href='/trigger/{monitor}'>{monitor}</a></li>")
    output.append('</ul></body>')
    return '\n'.join(output)

@app.route('/')
def index():
    return generateIndexOfTriggers()

# Trigger individual tests for debugging or for external triggering
@app.route('/trigger/<monitor>')
def runSingleTest(monitor: str):
    if monitor not in pingMonitors.keys():
        abort(404)
    resp, errorMsg = pingMonitors[monitor].pingUrlAndHandleErrors()
    if resp:
        return f"It worked!  {monitor} returned!: {resp}"
    else:
        return f"Request to {monitor} failed.  Error Reason: {errorMsg}"

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
    # Schedule the background jobs to actually run
    for monitor in pingMonitors.values():
       monitor.scheduleBackgroundJob() 
    # Trigger the background jobs to run continously.
    cease_continous_run = runBackgroundTasksContinuously()
    # Start the actual Flask Server
    app.run(host='0.0.0.0', port=8080)
    # Cancel all continous runs and exit
    cease_continous_run.set()