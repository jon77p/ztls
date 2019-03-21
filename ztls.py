import requests
from os import getenv
from sys import argv

def ztls(preferred=None):
    API = getenv('ZT_API')

    if not API:
        print('Error!')
        print("'ZT_API' environment variable does not exist!")
        exit()

    base = 'https://my.zerotier.com/api/'
    header = {'Authorization': 'bearer ' + API}

    req = requests.get(base + 'network', headers=header).json()
    networks = {}

    for i in req:
        networks[i['config']['name']] = i['id']

    results = {}

    print()
    for network in networks:
        if preferred is None or preferred.lower() == network.lower():
            results[network] = {}
            print(network + ":")
            print()

            res = requests.get(base + 'network/' + networks[network] + '/member', headers=header).json()

            for member in res:
                if member['config']['authorized']:
                    results[network][member['name']] = {}
                    results[network][member['name']]['name'] = member['name']
                    results[network][member['name']]['ip'] = member['config']['ipAssignments'][0]
                    if member['online']:
                        results[network][member['name']]['status'] = '🌐'
                    else:
                        results[network][member['name']]['status'] = '⛔️'
                    
                    print("{0: <20} | {1:<15} | Status: {2}".format(results[network][member['name']]['name'], results[network][member['name']]['ip'], results[network][member['name']]['status']))
            print()

if __name__ == "__main__":
    if len(argv) == 2:
        ztls(argv[1])
    else:
        ztls()
