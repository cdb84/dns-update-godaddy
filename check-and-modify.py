#!/usr/bin/python3
import requests, json
import argparse
import getpass
from urllib.request import urlopen
import sys
ip_fetch = "https://api.ipify.org"
parser = argparse.ArgumentParser(description="A script to check a specified DNS record matches the IP for this host; and if it does not, update that IP with the ip of this host.")
parser.add_argument("site", help="The fully qualified domain name of the particular site.", type=str)
parser.add_argument("typ", help="The type of the record that is being updated, caps-sensitive. A, AAAA, MX, SRV, etc.", type=str)
parser.add_argument("record", help="Actual record name, i.e. for gmail.google.com the record would be gmail.", type=str)
parser.add_argument("-ip", help="An IP to use in lieu of the one that is fetched by this script. Useful if this machine is not the desired host for your DNS records. (More secure option, can implement your own \"IP getting\" methods instead of the one used in this script.)", type=str)
parser.add_argument("-t", "--ttl", help="Time to live, in seconds. Cannot be lower than 600.", type=int)
parser.add_argument("-a", "--auth", help="Your API key:secret pair.", type=str)
parser.add_argument("-nr", help='"Not really" (will fetch but will not make changes to DNS records)', action="store_true")
args = parser.parse_args()
#if not provided with a key & secret from the command line, prompt for one unix-style
if not args.auth:
    auth=getpass.getpass()
#assume the one they provided via CLI
else:
    auth=args.auth
if not args.ip:
    #get client ip (insecure)
    client_ip = str(urlopen(ip_fetch).read())
    client_ip = client_ip.replace("b", "")
    client_ip = client_ip.replace("'", "")
else:
    #use the one provided
    client_ip = args.ip
#provided TTL and within acceptable bounds
if args.ttl and args.ttl >= 600:
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
url = "https://api.godaddy.com/v1/domains/"+args.site+"/records/"
#send a GET for the record data
r = requests.get(url, headers=headers)
if r.status_code != 200:
    sys.stderr.write("There was a problem accessing your domain records:")
    sys.stderr.write(r.text)
    exit(1)
res = r.json()
for item in res:
    if item['name'] == args.record and item['type'] == args.typ:
        print(item)
        if item['data'] == client_ip:
            #no action
            print("Client IP matches record IP (no action taken)")
            exit(0)
        else:
            #have to change the records
            print("Client IP ("+client_ip+") does not match record IP ("+item['data']+")")
            #if we aren't doing a dry-run
            if not args.nr:
                #account for @ symbol
                args.record = args.record.replace("@", "%40")
                #form new composite url
                url = "https://api.godaddy.com/v1/domains/"+args.site+"/records/"+args.typ+"/"+args.record+"/"
                #ship a new request (put this time)
                r = requests.put(url, headers=headers, data=json.dumps(data))
                #gain result
                res = r.text
                #error checking goes here
                if res == "{}" and r.status_code == 200:
                    print("Successfully changed DNS record data to "+client_ip)
                    exit(0)
                #print error and status if not
                sys.stderr.write(res)
                r.raise_for_status()
                exit(1)
            else:
                print("Not changing record (nr mode)")
                exit(0)
sys.stderr.write("Record not found")
exit(1)


