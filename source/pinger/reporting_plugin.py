from pinger_request_result import PingerRequestResult

# Base class for any reporting plugins we may want to use.
class ReportingPlugin:
    def __init__():
        pass
    # Get the response time and result from the response object and report results
    def reportStats(url: str, resp: PingerRequestResult) -> None:
        pass

