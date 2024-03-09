import yaml, time, tests, subprocess, signal
from threading import Event

CONF_PATH       =   "/etc/net-monitor/conf.yaml"

current_conf    =   {}
current_states  =   {}
timers          =   {}

stop_event      =   Event()


def load_conf():
    global current_conf
    try:
        with open(CONF_PATH) as f:
            current_conf = yaml.safe_load(f)
        return True
    except Exception as e:
        return False


def get_host_data(host : str):
    for h in current_conf['monitor']['hosts']:
        if h['name'] == host: return h
    else: raise Exception(f"No such host {host}")


def check_host_availability(host : dict):
    match host['type']:
        case 'icmp': return tests.ping(host['addr'])
        case 'command': return tests.command(host['exec'])
        case _: raise Exception(f"Wrong host type {host['type']}")


def check_group_availability(group : dict):
    availability = []
    for host in group['hosts']:
        if check_host_availability(get_host_data(host)) == True:
            availability.append(host)
    if len(group['hosts']) == len(availability): return 'ALL'
    elif len(availability) == 0: return 'NONE'
    else: return '-'.join(availability)


def notify_ha_script(path : str, args : list):
    return subprocess.call(["bash", path, *args])


def convert_args(availability : str, group : dict):
    args = availability.split('-')
    if 'args' in list(group.keys()):
        for redef in group['args']:
            args = list(map(lambda x: x.replace(redef['default'], redef['redefine']), args))
    return args


def init_groups():
    global timers
    for group in current_conf['monitor']['groups']:
        availib = check_group_availability(group)
        current_states[group['name']] = availib
        timers[group['name']] = time.time()
        args = convert_args(availib)
        notify_ha_script(group['exec'], args)


def sigterm_handler(signal, frame):
        print("Received SIGTERM. Exiting gracefully...")
        stop_event.set()




def main():
    global timers
    if load_conf() != True:
        raise Exception("failed to load configuration")
    signal.signal(signal.SIGTERM, sigterm_handler)   # handle SIGTERM signal
    init_groups()
    while not stop_event.is_set():
        for group in current_conf['monitor']['groups']:
            if time.time() - timers[group['name']] >= group['interval']:
                availib = check_group_availability(group)
                if availib != current_states[group['name']]:
                    current_states[group['name']] = availib
                    notify_ha_script(group['exec'], availib.split('-'))
                timers[group['name']] = time.time()
    print("done")





if __name__ == "__main__":
    main()
