#!/usr/bin/python3
"""
GoDaddy DDNS Tools
Connor Berry, 2018
This module performs a check-and-modify: check a record, if it differs from
the user's specifications, change it.
"""
import sys
import argparse
import getpass
import requests, json
from urllib.request import urlopen
IP_FETCH = "https://api.ipify.org"
API_URL = "https://api.godaddy.com/v1/domains/"
TTL_LOW_BOUND = 600
parser = argparse.ArgumentParser(description="A script to check a specified"
                                 +" DNS record matches the IP for this host;"
                                 +" and if it does not, update that IP with"
                                 +" the ip of this host.")
parser.add_argument("site", help="The fully qualified domain name of the"
                    +" particular site.", type=str)
parser.add_argument("type", help="The type of the record that is being"
                    +" updated, caps-sensitive. A, AAAA, MX, SRV, etc.",
                    type=str)
parser.add_argument("record", help="Actual record name, i.e. for gmail.go"
                    +"ogle.com the record would be gmail.", type=str)
parser.add_argument("-ip", help="An IP to use in lieu of the one that is"
                    +" fetched by this script. Useful if this machine is"
                    +" not the desired host for your DNS records. (More"
                    +" secure option, can implement your own \"IP getting\""
                    +" methods instead of the one used in this script.)",
                    type=str)
parser.add_argument("-t", "--ttl", help="Time to live, in seconds. Cannot"
                    +" be lower than 600. GoDaddy default is 1 hour (3600"
                    +" seconds)", type=int)
parser.add_argument("-a", "--auth", help="Your API key:secret pair.", type=str)
parser.add_argument("-nr", help='"Not really" (will fetch but will not make'
                    +' changes to DNS records)', action="store_true")
args = parser.parse_args()
#if not provided with a key & secret from the command line, prompt for
#one unix-style
if not args.auth:
    auth = getpass.getpass()
#assume the one they provided via CLI
else:
    auth = args.auth
if not args.ip:
    #get client ip (insecure)
    client_ip = str(urlopen(IP_FETCH).read())
    client_ip = client_ip.replace("b", "")
    client_ip = client_ip.replace("'", "")
else:
    #use the one provided
    client_ip = args.ip
#provided TTL and within acceptable bounds
if args.ttl and args.ttl >= TTL_LOW_BOUND:
    data = [
        {"data":client_ip, "ttl":args.ttl}
    ]
#not provided or unacceptable uses default
else:
    data = [
        {"data":client_ip}
    ]
#form the headers
headers = {
    'content-type': 'application/json',
    'Authorization': 'sso-key '+auth
    }
#form the composite URL to use with GoDaddy API
url = API_URL+args.site+"/records/"
#send a GET for the record data
req = requests.get(url, headers=headers)
if req.status_code != 200:
    sys.stderr.write("There was a problem accessing your domain records:")
    sys.stderr.write(req.text)
    exit(1)
records = req.json()
for item in records:
    if item['name'] == args.record and item['type'] == args.type:
        print(item)
        if item['data'] == client_ip:
            #no action
            print("Client IP matches record IP (no action taken)")
            exit(0)
        else:
            #have to change the records
            print("Client IP ("+client_ip+") does not match record IP ("
                  +item['data']+")")
            #if we aren't doing a dry-run
            if not args.nr:
                #account for @ symbol
                args.record = args.record.replace("@", "%40")
                #form new composite url
                url = (API_URL+args.site+"/records/"+args.type
                       +"/"+args.record+"/")
                #ship a new request (put this time)
                req = requests.put(url, headers=headers, data=json.dumps(data))
                #gain result
                result = req.text
                #error checking goes here
                if result == "{}" and req.status_code == 200:
                    print("Successfully changed DNS record data to "+client_ip)
                    exit(0)
                #print error and status if not
                sys.stderr.write(result)
                req.raise_for_status()
                exit(1)
            else:
                print("Not changing record (-nr mode)")
                exit(0)
sys.stderr.write("Record not found")
exit(1)


