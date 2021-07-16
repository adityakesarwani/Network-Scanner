import ipaddress
import aioping  # type:ignore
import asyncio
import time
import argparse
import typing


async def do_ping(host: str, timeout: float, sem: asyncio.locks.Semaphore, active_hosts: typing.List) -> str:
    """do_ping() is responsible for pinging the hosts"""
    await sem.acquire()
    try:
        delay = await aioping.ping(host, timeout=timeout) * 1000
        active_hosts.append("Ping response in %.6s ms from " % delay + host)
        return "Ping response in %s ms from " % delay + host

    except TimeoutError:
        return "Timed out for " + host

    finally:
        sem.release()


def get_hosts(net: str) -> typing.List[str]:
    """get_hosts() will return all the hosts within a network"""
    print("Network to scan:",net)
    network = ipaddress.IPv4Network(net)
    hosts_obj = network.hosts()
    print("Prefix to scan:",network.prefixlen)
    hosts = []
    for i in hosts_obj:
        hosts.append(str(i))
    print("Number of hosts to scan:",len(hosts))
    return hosts


async def execute(hosts: typing.List[str], timeout: float, sem: asyncio.locks.Semaphore, active_hosts: typing.List) -> None:
    """execute() takes care of concurrency and asyncio and prints the output in the external file"""
    tasks = []

    # opening a txt file for writing the output of ping
    srcfile = open('output.txt', 'w')

    for host in hosts:
        tasks.append(asyncio.ensure_future(do_ping(host, timeout, sem, active_hosts)))
    print("Scanning the hosts... ")
    delays = await asyncio.gather(*tasks)
    for delay in delays:
        print(delay, file=srcfile)


def set_params(net: str, concurrency: int, timeout: float) -> typing.Tuple[str, int, float]:
    """set_params() is responsible to set all the parameters for pinging"""
    set_net = net
    if concurrency is None:
        set_concurrency = 1
    else:
        set_concurrency = concurrency
    if timeout is None:
        set_timeout = 5.0
    else:
        set_timeout = timeout
    return (set_net, set_concurrency, set_timeout)

def main():
    start_time = time.time()

    # fetching command line inputs and storing them in the variables
    parser = argparse.ArgumentParser(description="Ping-based concurrent network scan")
    parser.add_argument("pingdiscover", help="Subnet + netmask. E.g. <192.168.0.0/24>", type=str)
    parser.add_argument("--concurrent", help="Concurrency level", type=int)
    parser.add_argument("--timeout", help="Timeout", type=float)
    args = parser.parse_args()
    net, concurrency, timeout = set_params(args.pingdiscover, args.concurrent, args.timeout)

    # fetching all the hosts within a network
    hosts = get_hosts(net)

    # setting up the concurrency level of the execution
    sem = asyncio.Semaphore(concurrency)
    active_hosts=[]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute(hosts, timeout, sem, active_hosts))
    if(len(active_hosts)>0):
        for active_host in active_hosts:
            print (active_host)
    else:
        print("No active host found")

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()