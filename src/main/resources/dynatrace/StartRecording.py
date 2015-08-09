#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#
import sys
from com.xebialabs.xlrelease.plugin.webhook import XmlPathResult

def extractXPath(xml, xPath):
    return XmlPathResult(xml, xPath).get()

STATUS_SUCCESS = 200
STATUS_FORBIDDEN = 403

if dynatraceServer is None:
    print "No server provided."
    sys.exit(1)

serverUrl = dynatraceServer['url']
if serverUrl.endswith('/'):
    serverUrl = serverUrl[:len(serverUrl)-1]

connection = HttpRequest(dynatraceServer, username, password)
body = ''
# watch for encoding problems
if presentableName:
    body += 'presentableName=' + presentableName
if description:
    body += '&description=' + description

response = connection.post("/rest/management/profiles/%s/startrecording" % profile, body, contentType = 'text/xml')


if response.status == STATUS_SUCCESS:
    sessionName = extractXPath(response.response, '/result/@value')
    print "Started recording of session %s via Dynatrace server at %s.\n" % (sessionName, serverUrl)
elif response.status == STATUS_FORBIDDEN:
    errorMsg = extractXPath(response.response, '/error/@reason')
    print "Failed to start recording via Dynatrace server at %s: %s\n" % (serverUrl, errorMsg)
    response.errorDump()	
else:
    print "Failed to start recording via Dynatrace server at %s.\n" % serverUrl
    response.errorDump()
    sys.exit(1)
