import sys
import requests
import schedule
import re
from datetime import datetime
from reporting_plugin import ReportingPlugin
from pinger_request_result import PingerRequestResult

# src: https://www.makeuseof.com/regular-expressions-validate-url/#:~:text=The%20regex%20will%20consider%20a,characters%20and%2For%20special%20characters.
# Using a global variable with compile to make this more performant
URL_VALIDATION_RE = re.compile('^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$')

# TODO move this to tunable application settings in a UI
# -1 means no limit, first value of the tuple is the inclusive lower limit, the second 
PINGER_LIMITS = {
    "intervalSeconds" : [10,-1],
    "retryCount" : [-1, 5],
    "failureThreshold" : [-1, -1],
    "successThreshold" : [-1, -1],
    "requestTimeoutSeconds": [-1, 30]
}


# Manages the sending of test requests and handling failures. 
class Pinger(object):
    def __init__(self, url: str, intervalSeconds: int, retryCount: int, failureThreshold: int, successThreshold: int, alertWebhooks: list[str], alertEmails: list[str], requestTimeoutSeconds: int=30, reportingPlugin: ReportingPlugin=None) -> None:
        self.url = url
        self.reportingPlugin: None or ReportingPlugin = None
        self.intervalSeconds = intervalSeconds
        self.retryCount = retryCount
        self.failureThreshold = failureThreshold
        self.successThreshold = successThreshold
        self.alertWebhooks = alertWebhooks
        self.alertEmails = alertEmails
        self.requestTimeoutSeconds = requestTimeoutSeconds
        self.validateParameters()
    
    def validateParameters(self):
        global URL_VALIDATION_RE
        global PINGER_LIMITS
        # We can assume the value 
        if URL_VALIDATION_RE.match(self.url) == None:
            tb = sys.exc_info()[2]
            raise ValueError(f"Invalid Value given for URL to Pinger. '{self.url}' is not an URL  ").with_traceback(tb)

        if self.__isValueOutOfLimits(self.retryCount, PINGER_LIMITS['retryCount']) == False:
            tb = sys.exc_info()[2]
            raise ValueError(f"Interval for Ping is too small.  Must be greater than  seconds. '{self.url}' monitor has an interval value of {self.intervalSeconds} seconds").with_traceback(tb)

        if self.__isValueOutOfLimits(self.failureThreshold, PINGER_LIMITS['failureThreshold']) == False:
            tb = sys.exc_info()[2]
            raise ValueError(f"The provided Failure threshold for '{self.url}' is out of range. ").with_traceback(tb)

        if self.__isValueOutOfLimits(self.requestTimeoutSeconds, PINGER_LIMITS['requestTimeoutSeconds']) == False:
            tb = sys.exc_info()[2]
            raise ValueError(f"Request Timeout provided for '{self.url}' is out of range.  Must be less than 30 seconds").with_traceback(tb)

    def __isValueOutOfLimits(self, val: int, limits: list[int])  -> bool:
        if limits[0] != -1 and limits[0] > val:
            return False
        if limits[1] != -1 and limits[1] < val:
            return False
        return True
    
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
        return (resp.isSuccess, resp.failureReason)

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