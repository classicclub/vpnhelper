import re
import requests
import argparse


RE_PASS = re.compile(r'(<li><strong>Password:<\/strong>)(?P<password>[^<]+)(<\/li>)')

TEXT_ONLINE = 'Online'
VPNS = ('me', 'eu', 'se', 'im', 'it', 'be', 'co.uk')

def get_password(username):
    passw = None
    html  = requests.get('https://'+ username + '/accounts').text

    match = RE_PASS.search(html)
    if match:
        passw = match.groups()[1]
    
    return passw.strip() if passw else None



