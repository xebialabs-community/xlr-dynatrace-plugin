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

if dynatraceServer is None:
    print "No server provided."
    sys.exit(1)

serverUrl = dynatraceServer['url']
if serverUrl.endswith('/'):
    serverUrl = serverUrl[:len(serverUrl)-1]

connection = HttpRequest(dynatraceServer, username, password)

# Even once all tests have been completed, the Dynatrace server can take a bit
# of time to process all the data.
time.sleep(delay)

response = connection.get("/rest/management/profiles/%s/testruns/%s" % (profile, testRunId), contentType = 'application/json', headers = {'Accept-Encoding': 'gzip'})
if response.status == TESTRUN_COMPLETED_STATUS:
    data = json.loads(response.response)
    testResults = data.get('testRun')
    numDegradedTests = testResults.get('numDegraded')
    numFailedTests = testResults.get('numFailed')
    numImprovedTests = testResults.get('numImproved')
    numInvalidatedTests = testResults.get('numInvalidated')
    numPassedTests = testResults.get('numPassed')
    numVolatileTests = testResults.get('numVolatile')
    print "Test run %s completed.\n" % testRunId
    # the log output is Markdown
    print "\# degraded tests: #%s\n" % numDegradedTests
    print "\# failed tests: #%s\n" % numFailedTests
    print "\# improved tests: #%s\n" % numImprovedTests
    print "\# invalidated tests: #%s\n" % numInvalidatedTests
    print "\# passed tests: #%s\n" % numPassedTests
    print "\# volatile tests: #%s\n" % numVolatileTests
    print "Result: %s\n" % testResults
    # TODO add a deep link to Dynatrace for more details if one exists
    sys.exit(0)
elif response.status == INSUFFICIENT_LICENSE_STATUS:
    print "The Dynatrace server at %s does not have a Test Center Edition license or the connecting user is not authorized.\n" % serverUrl
    sys.exit(1)
elif response.status == PROFILE_OR_TESTRUN_NOT_FOUND_STATUS:
    print "No system profile with name %s or test run with id %s found in the Dynatrace server at %s.\n" % (profile, testRunId, serverUrl) 
    sys.exit(1)
elif not response.isSuccessful():
    print "Unable to retrieve test results for test run %s from Dynatrace server at %s.\n" % (testRunId, serverUrl)
    response.errorDump()
    sys.exit(1)