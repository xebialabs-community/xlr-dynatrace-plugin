#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#
import sys, datetime

def noneToEmpty(stringValue):
    if stringValue:
        return stringValue
    else:
        return ''

STATUS_SUCCESS = 201
STATUS_FORBIDDEN = 403

if dynatraceServer is None:
    print "No server provided."
    sys.exit(1)

serverUrl = dynatraceServer['url']
if serverUrl.endswith('/'):
    serverUrl = serverUrl[:len(serverUrl)-1]

connection = HttpRequest(dynatraceServer, username, password)

if not start:
    start = datetime.datetime.now().isoformat()
if not end:
    end = start

body = """
<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<incident>
  <message>%s</message>
  <description>%s</description>
  <severity>informational</severity>
  <start>%s</start>
  <end>%s</end>
</incident>
""" % (noneToEmpty(message), noneToEmpty(description), start, end)

response = connection.post("/rest/management/profiles/%s/incidentrules/Deployment/incidents" % profile, body, contentType = 'application/xml')

if response.status == STATUS_SUCCESS:
    print "Registered a deployment with Dynatrace server at %s.\n" % serverUrl
else:
    print "Failed to register a deployment with Dynatrace server at %s.\n" % serverUrl
    response.errorDump()
    sys.exit(1)
