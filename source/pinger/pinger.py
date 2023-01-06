import requests
import schedule
from datetime import datetime

class Pinger(object):
    def __init__(self, url: str, intervalSeconds: int, retryCount: int, failureThreshold: int, alertWebhooks: list[str], alertEmails: list[str]) -> None:
        self.url = url
        self.reportingPlugin = None
        self.intervalSeconds = intervalSeconds
        self.retryCount = retryCount
        self.failureThreshold = failureThreshold
        self.alertWebhooks = alertWebhooks
        self.alertEmails = alertEmails
    
    # Perform a single GET request to the url
    # returns: True if the service returns a non-error and false otherwise
    def singleGet(self) -> bool:
        print(f"Running ping on {self.url}")
        resp = requests.get(self.url)
        attempt = 1
        while attempt < self.retryCount and not resp.ok:
            resp = requests.get(self.url)
            attempt += 1
        self.reportMetricsIfNecessary(resp)
        if not resp.ok:
            print(f"Error encountered while pinging {self.url}")
            self.handleError(resp)
        else:
            print(f"Successful ping of {self.url}")
        print(f"Finished running ping on {self.url}")
        return resp.ok
    
    def reportMetricsIfNecessary(self, resp: requests.Response) -> None:
        if self.reportingPlugin:
            self.reportingPlugin.reportStats(self.url)
    
    def scheduleBackgroundJob(self):
        schedule.every(self.intervalSeconds).seconds.do(self.singleGet)
    
    def handleError(self, resp: requests.Response):
        # TODO implement error handling
        pass