#Utility class to pass request results back and forth 
class PingerRequestResult(object):
    def __init__(self, isSuccess: bool, responseTimeSeconds: float, failureReason: str, responseCode: int):
        self.isSuccess: bool = isSuccess
        self.responseTimeSeconds: float = responseTimeSeconds
        self.failureReason: str = failureReason
        self.responseCode: int = responseCode