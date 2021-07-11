# Network Scanner

Hi! I'm **Network Scanner**. I am a python-based tool which helps to scan the network and check for active hosts within a network by pinging them. I am very fast as I implement concepts of **asyncio** for concurrent processing.


## Files in Repository 

There are two main files in the repository which can help you to start using the tool. The files are mentioned below:

 1. net_scan.py  `This file contains all the python code`

 2. requirements.txt `This file contains all the required dependencies needed to be installed for running the tool`

## Installation Instructions

For installing the tool we need to go through two steps which are mentioned below:

**1.** **Cloning the git repository**

 - For cloning the git repository open a terminal and go to the directory where you want to clone the files.
 - Run the following command. Git automatically creates a folder with the repository name and downloads the files there.
 
	> git clone https://github.com/adityakesarwani/Network-Scanner
 - To view the files, go to the new directory
 
	 > cd Network-Scanner

**2.**  **Installing all the required dependencies**

 - For installing the required dependencies we can use requirements.txt file.
 - Run the following command, pip will automatically install all the mentioned python packages within the requirements.txt file. 
 
	 >pip install -r requirements.txt

Once we are done with both the steps we are good to use the tool.

## Getting Started

This tool accepts command line arguments to perform a "ping-based" concurrent scan.

The tool accepts three command line argument:

 1. **Network ID:** the network which needs to be scanned. 
 Syntax: X.X.X.X/subnet_prefix 
 Example: 192.168.100.0/24
 2. **Concurrency level:** number of concurrent hosts that are pinged at the same time (accepts int value) (default level 1). **The recommeded concurrency level is from 1 to 500**. The tool can crash with the concurrency level of the more than 500. 
 3. **Timeout:** number of seconds after giving up on pinging a host (accepts int/ float)(default 5s).

Let’s start with a simple example:

In this example we would be scanning the **network 8.8.8.0/24** with the **concurrency level of 500** at the **timeout of 1s.**

Run the following command in the terminal to test above example:

    $ python net_scan.py 8.8.8.0/24 --concurrent 500 --timeout 1

An **output.txt** file will be created in the same directory after running the python script, which would contain the output of network scan.

## How it works?

Lets summarize the working of tool in steps: 

 1. The journey of the tool starts with taking the command line inputs for **Network_ID**, **Concurrency_Level** and **Timeout**.
 2. Once the inputs are taken, we fetch the IP addresses of all the hosts within the mentioned Network using `ipaddress` python package.
 3. Then we have used **Semaphores** to maintain the concurrency in the tool. We have assigned the input of Concurrency_Level to semaphores. 
 4. After setting up the concurrency level we have created tasks to ping the ip addresses. We have individual tasks for all the ip addresses in the network.
 5. Once the tasks are created we have kept those tasks on the **event_loop** to execute then concurrently. 
 6. After the execution of pings to all the hosts, the ping-reply is printed in a text file named "output.txt". 
