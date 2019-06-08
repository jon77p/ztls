import requests
from os import getenv, uname
from sys import argv

def ztls(preferred=None, only_online=False):
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
        if preferred is None or preferred.lower() in network.lower():
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
                        if uname().sysname == 'Darwin':
                            results[network][member['name']]['status'] = '\x1b[1;32;40m' + '􀁣' + '\x1b[0m'
                        else:
                            results[network][member['name']]['status'] = '🌐'
                    else:
                        if only_online is False:
                            if uname().sysname == 'Darwin':
                                results[network][member['name']]['status'] = '\x1b[1;31;40m' + '􀁠' + '\x1b[0m'
                            else:
                                results[network][member['name']]['status'] = '⛔️'
                        else:
                            continue                   
                    print("{0: <20} | {1:<15} | Status: {2}".format(results[network][member['name']]['name'], results[network][member['name']]['ip'], results[network][member['name']]['status']))
            print()

if __name__ == "__main__":
    if '-online'.lower() in argv:
        only_online = True
        argv.pop() # remove online cmd arg from argv size
    else:
        only_online = False

    if len(argv) == 2:
        ztls(argv[1], only_online=only_online)
    else:
        ztls(only_online=only_online)
