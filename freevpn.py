import re
import requests
from bs4 import BeautifulSoup



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

def get_vpn_status():
    html = requests.get('https://freevpn.me/').text
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find_all(
        'table', attrs={'class': "table table-striped table-bordered dataTable"})
    # vpns = []
    if table:
        table = table[0]
        tbody = table.tbody
        trows = tbody.find_all('tr')[1:]
        for row in trows:
            name = None
            loc = None
            online = False
            load = None
            tcols = row.find_all('td')
            for i, tcol in enumerate(tcols):
                if i == 1:
                    name = tcol.text.strip().lower()
                elif i == 2:
                    loc = tcol.text.strip()
                elif i == 4:
                    if tcol.text.strip() == TEXT_ONLINE:
                        online = True
                elif i == 8:
                    load = tcol.text.strip()[:-1]
            if name:
                # vpns.append({'name': name, 'loc': loc,
                #              'online': online, 'load': load})
                yield {'name': name, 'loc': loc,
                       'online': online, 'load': load}




