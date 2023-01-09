#Utility class to pass request results back and forth 
class PingerRequestResult(object):
    def __init__(self, isSuccess: bool, responseTimeSeconds: float, failureReason: str, responseCode: int):
        self.isSuccess = isSuccess,
        self.responseTimeSeconds = responseTimeSeconds
        self.failureReason = failureReason
        self.responseCode = responseCode