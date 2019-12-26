import os
from aws_xray_sdk.core import xray_recorder

DAEMON_ADDRESS = os.getenv('DAEMON_ADDRESS', '127.0.0.1:2000')
xray_recorder.configure(
    sampling=False,
    context_missing='LOG_ERROR',
#    plugins=('EC2Plugin', ),
    daemon_address=DAEMON_ADDRESS,
    dynamic_naming='*mysite.com*'
)

recorder = xray_recorder
