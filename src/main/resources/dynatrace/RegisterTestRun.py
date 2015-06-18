#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#
import sys, string
import com.xhaus.jyson.JysonCodec as json

TESTRUN_REGISTERED_STATUS = 201
INSUFFICIENT_LICENSE_STATUS = 403
PROFILE_NOT_FOUND_STATUS = 404

def addEntryIfPresent(dict, key, value):
    if value:
        dict[key] = value

contentMap = { 'category': category }
addEntryIfPresent(contentMap, 'versionMajor', versionMajor)
addEntryIfPresent(contentMap, 'versionMinor', versionMinor)
addEntryIfPresent(contentMap, 'versionRevision', versionRevision)
addEntryIfPresent(contentMap, 'versionBuild', versionBuild)
addEntryIfPresent(contentMap, 'versionMilestone', versionMilestone)
addEntryIfPresent(contentMap, 'marker', marker)
addEntryIfPresent(contentMap, 'platform', platform)
addEntryIfPresent(contentMap, 'loadTestName', loadTestName)

if dynatraceServer is None:
    print "No server provided."
    sys.exit(1)

serverUrl = dynatraceServer['url']
if serverUrl.endswith('/'):
    serverUrl = serverUrl[:len(serverUrl)-1]

connection = HttpRequest(dynatraceServer, username, password)
response = connection.post("/rest/management/profiles/%s/testruns" % profile, json.dumps(contentMap), contentType = 'application/json')

if response.status == TESTRUN_REGISTERED_STATUS:
    data = json.loads(response.response)
    testRunId = data.get('testRun').get('id')
    print "Registered test run with ID %s via Dynatrace server at %s.\n" % (testRunId, serverUrl)
elif response.status == INSUFFICIENT_LICENSE_STATUS:
    print "The Dynatrace server at %s does not have a Test Center Edition license or the connecting user is not authorized.\n" % serverUrl
    sys.exit(1)
elif response.status == PROFILE_NOT_FOUND_STATUS:
    print "No system profile with name '%s' found in the Dynatrace server at %s.\n" % (profile, serverUrl)
    sys.exit(1)
else:
    print "Failed to register test run via Dynatrace server at %s.\n" % serverUrl
    response.errorDump()
    sys.exit(1)
