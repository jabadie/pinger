import unittest
from pinger import Pinger
from pinger_request_result import PingerRequestResult


class TestPingerExpectingFailure(unittest.TestCase):
    def setUp(self):
        self.url = "http://foo.bar"
        self.intervalSeconds = 30
        self.retryCount = 1
        self.failureThreshold = 2
        self.successThreshold = 2
        self.alertEmails = []
        self.alertWebhooks = []
        self.pinger = Pinger(self.url, self.intervalSeconds, self.retryCount, self.failureThreshold, self.successThreshold, self.alertEmails, self.alertWebhooks)

    def testParamAssignment(self):
        self.assertEqual(self.pinger.intervalSeconds, self.intervalSeconds)
        self.assertEqual(self.pinger.retryCount, self.retryCount)
        self.assertEqual(self.pinger.failureThreshold, self.failureThreshold)
        self.assertEqual(self.pinger.successThreshold, self.successThreshold)
        self.assertEqual(self.pinger.alertEmails, self.alertEmails)
        self.assertEqual(self.pinger.alertWebhooks, self.alertWebhooks)
    
    def testFailedSinglePingFromFailedEstablishedConnection(self):
        requestResult = self.pinger.doSingleRequest()
        self.assertEqual(requestResult.isSuccess, False)
        self.assertRegex(requestResult.failureReason, ".*Failed to establish a new connection.*")

class TestPingerExpectingSuccess(unittest.TestCase):
    def setUp(self):
        self.url = "http://data.world"
        self.intervalSeconds = 30
        self.retryCount = 1
        self.failureThreshold = 2
        self.successThreshold = 2
        self.alertEmails = []
        self.alertWebhooks = []
        self.pinger = Pinger(self.url, self.intervalSeconds, self.retryCount, self.failureThreshold, self.successThreshold, self.alertEmails, self.alertWebhooks)

    def testParamAssignment(self):
        self.assertEqual(self.pinger.intervalSeconds, self.intervalSeconds)
        self.assertEqual(self.pinger.retryCount, self.retryCount)
        self.assertEqual(self.pinger.failureThreshold, self.failureThreshold)
        self.assertEqual(self.pinger.successThreshold, self.successThreshold)
        self.assertEqual(self.pinger.alertEmails, self.alertEmails)
        self.assertEqual(self.pinger.alertWebhooks, self.alertWebhooks)
    
    def testSuccessfulSinglePing(self):
        requestResult = self.pinger.doSingleRequest()
        self.assertEqual(requestResult.isSuccess, True)
        # We can safely assume this get shouldn't take 60 seconds
        self.assertLessEqual(requestResult.responseTimeSeconds, 60)
        self.assertEqual(requestResult.failureReason, "OK")
        self.assertEqual(requestResult.responseCode, 200)
    

        
    
if __name__ == '__main__':
    unittest.main()