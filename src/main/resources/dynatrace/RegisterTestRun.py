import sys, string
import com.xhaus.jyson.JysonCodec as json

TESTRUN_REGISTERED_STATUS = 201
INSUFFICIENT_LICENSE_STATUS = 403
PROFILE_NOT_FOUND_STATUS = 404

# TODO: build full input object based on parameters
content = """
{
    "category": "%s"
}
""" % category

if dynatraceServer is None:
    print "No server provided."
    sys.exit(1)

serverUrl = dynatraceServer['url']
if serverUrl.endswith('/'):
    serverUrl = serverUrl[:len(serverUrl)-1]

connection = HttpRequest(dynatraceServer, username, password)
response = connection.post("/rest/management/profiles/%s/testruns" % profile, content, contentType = 'application/json')

if response.status == TESTRUN_REGISTERED_STATUS:
    data = json.loads(response.response)
    testRunId = data.get('testRun').get('id')
    print "Registered test run with ID %s via Dynatrace server at %s." % (testRunId, serverUrl)
elif response.status == INSUFFICIENT_LICENSE_STATUS:
    print "The Dynatrace server at %s does not have a Test Center Edition license or the connecting user is not authorized." % serverUrl
elif response.status == PROFILE_NOT_FOUND_STATUS:
    print "No system profile with name %s found in the Dynatrace server at %s." % (profile, serverUrl)
else:
    print "Failed to register test run via Dynatrace server at %s." % serverUrl
    response.errorDump()
    sys.exit(1)
