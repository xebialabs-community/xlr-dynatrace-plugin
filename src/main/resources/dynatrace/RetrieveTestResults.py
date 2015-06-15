#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#
import sys, string, time, urllib
import com.xhaus.jyson.JysonCodec as json

TESTRUN_COMPLETED_STATUS = 200
INSUFFICIENT_LICENSE_STATUS = 403
PROFILE_OR_TESTRUN_NOT_FOUND_STATUS = 404

poll_interval = 20
max_poll_count = 10

if dynatraceServer is None:
    print "No server provided."
    sys.exit(1)

serverUrl = dynatraceServer['url']
if serverUrl.endswith('/'):
    serverUrl = serverUrl[:len(serverUrl)-1]

connection = HttpRequest(dynatraceServer, username, password)

pollCount = 0
while (pollCount < max_poll_count):
    time.sleep(poll_interval)
    response = connection.get("/rest/management/profiles/%s/testruns/%s" % (profile, testRunId), contentType = 'application/json', headers = {'Accept-Encoding': 'gzip'})
    pollCount += 1
    if response.status == TESTRUN_COMPLETED_STATUS:
        data = json.loads(response.response)
        testResults = data.get('testRun')
        numDegradedTests = testResults.get('numDegraded')
        numFailedTests = testResults.get('numFailed')
        numImprovedTests = testResults.get('numImproved')
        numInvalidatedTests = testResults.get('numInvalidated')
        numPassedTests = testResults.get('numPassed')
        numVolatileTests = testResults.get('numVolatile')
        print "Test run %s completed." % testRunId
        print "# degraded tests: #%s" % numDegradedTests
        print "# failed tests: #%s" % numFailedTests
        print "# improved tests: #%s" % numImprovedTests
        print "# invalidated tests: #%s" % numInvalidatedTests
        print "# passed tests: #%s" % numPassedTests
        print "# volatile tests: #%s" % numVolatileTests
        print "Result: %s" % testResults
        # TODO add a deep link to Dynatrace for more details if one exists
        sys.exit(0)
    elif response.status == INSUFFICIENT_LICENSE_STATUS:
        print "The Dynatrace server at %s does not have a Test Center Edition license or the connecting user is not authorized." % serverUrl
        sys.exit(1)
    elif response.status == PROFILE_OR_TESTRUN_NOT_FOUND_STATUS:
        print "No system profile with name %s or test run with id %s found in the Dynatrace server at %s." % (profile, testRunId, serverUrl) 
        sys.exit(1)   
    elif not response.isSuccessful():
        print "Failed to connect to Dynatrace server at %s." % serverUrl
        response.errorDump()
        sys.exit(1)

print "Unable to retrieve test results for test run %s after #%s attempts." % (testRunId, max_poll_count)
sys.exit(1)