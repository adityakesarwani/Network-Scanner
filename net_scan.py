import ipaddress
import aioping  # type:ignore
import asyncio
import time
import argparse
import typing


async def do_ping(host: str, timeout: float) -> str:
    """do_ping() is responsible for pinging the hosts"""
    await sem.acquire()
    try:
        delay = await aioping.ping(host, timeout=timeout) * 1000
        return "Ping response in %s ms from " % delay + host

    except TimeoutError:
        return "Timed out for " + host

    finally:
        sem.release()


def get_hosts(net: str) -> typing.List[str]:
    """get_hosts() will return all the hosts within a network"""
    network = ipaddress.IPv4Network(net)
    hosts_obj = network.hosts()
    hosts = []
    for i in hosts_obj:
        hosts.append(str(i))
    return hosts


async def execute(hosts: typing.List[str], timeout: float) -> None:
    """execute() takes care of concurrency and asyncio """
    tasks = []
    for host in hosts:
        tasks.append(asyncio.ensure_future(do_ping(host, timeout)))

    delays = await asyncio.gather(*tasks)
    for delay in delays:
        print(delay, file=srcfile)
    srcfile.close()


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


if __name__ == "__main__":
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

    # opening a txt file for writing the output of ping
    srcfile = open('output.txt', 'w')

    # setting up the concurrency level of the execution
    sem = asyncio.Semaphore(concurrency)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute(hosts, timeout))

    print("--- %s seconds ---" % (time.time() - start_time))