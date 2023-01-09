import sys
import requests
import schedule
from datetime import datetime
from reporting_plugin import ReportingPlugin
from pinger_request_result import PingerRequestResult

# Manages the sending of test requests and handling failures. 
class Pinger(object):
    def __init__(self, url: str, intervalSeconds: int, retryCount: int, failureThreshold: int, alertWebhooks: list[str], alertEmails: list[str], requestTimeoutSeconds: int=30, reportingPlugin: ReportingPlugin=None) -> None:
        self.url = url
        self.reportingPlugin: None or ReportingPlugin = None
        self.intervalSeconds = intervalSeconds
        self.retryCount = retryCount
        self.failureThreshold = failureThreshold
        self.alertWebhooks = alertWebhooks
        self.alertEmails = alertEmails
        self.requestTimeoutSeconds = requestTimeoutSeconds
    
    # Do a single get with the requests class and return the results
    def doSingleRequest(self) -> PingerRequestResult:
        # We could in theory use Requests.Response.elapsed for timing, but we dont' have access
        # to that if there's a timeout. Using two methods of timing things is very bad.  so, we do this.
        startTime = datetime.now()
        try: 
            resp = requests.get(self.url)
            endTime = datetime.now()
            elapsedTime = endTime - startTime
            return PingerRequestResult(resp.ok, elapsedTime.total_seconds(), resp.reason, resp.status_code)
        # TODO Capture only request exceptions.  Let others flow threw an crash
        except Exception as e:
            endTime = datetime.now()
            elapsedTime = endTime - startTime
            return PingerRequestResult(False, elapsedTime.total_seconds(), str(e), -1)
    
    # Perform a single GET request to the url and handle any errors
    # returns: True if the service returns a non-error and false otherwise
    def pingUrlAndHandleErrors(self) -> tuple[bool, str]:
        print(f"Running test on {self.url}", file=sys.stderr)
        resp = self.doSingleRequest()
        attempt = 1
        while attempt < self.retryCount and not resp.isSuccess:
            resp = self.doSingleRequest()
            attempt += 1
        self.reportMetricsIfNecessary(resp)
        if not resp.isSuccess:
            print(f"Error encountered while pinging {self.url}: Error: {resp.failureReason}", file=sys.stderr)
            self.handleErrorAndAlertIfNecessary(resp)
        else:
            print(f"Successful response from {self.url}")
        return resp.isSuccess, resp.failureReason

    #  
    def reportMetricsIfNecessary(self, resp: PingerRequestResult) -> None:
        if self.reportingPlugin:
            self.reportingPlugin.reportStats(self.url, resp)
    
    # schedule the job 
    def scheduleBackgroundJob(self):
        self.job =  schedule.every(self.intervalSeconds).seconds.do(self.pingUrlAndHandleErrors)
    
    # Check for previous failures, and if necessary, email alerts and trigger webhooks
    def handleErrorAndAlertIfNecessary(self, resp: PingerRequestResult):
        # TODO implement error handling
        pass