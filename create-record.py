#!/usr/bin/python3
import requests, json
import argparse
import getpass
from urllib.request import urlopen
import sys
''' 
    Connor Berry 2018
    MIT License 
'''
#modeled from the following curl statement:
#curl -XPUT -H "Content-type: application/json" -H 'Authorization: sso-key <API_KEY>' -d "[{\"data\": \"$IP\",\"ttl\": $TTL}]" "https://api.godaddy.com/v1/domains/$SITE/records/"$TYPE"/$RECORD"

_ip_fetch_ = "https://api.ipify.org"
_ttl_low_bound_ = 600

parser = argparse.ArgumentParser(description="A script to dynamically update and/or create your site's GoDaddy DNS records.")
parser.add_argument("site", help="The fully qualified domain name of the particular site.", type=str)
parser.add_argument("type", help="The type of the record that is being updated, caps-sensitive. A, AAAA, MX, SRV, etc.", type=str)
parser.add_argument("record", help="Actual record name, i.e. for gmail.google.com the record would be gmail. If the specified record does not exist, one will be created.", type=str)
parser.add_argument("-t", "--ttl", help="Time to live, in seconds. Cannot be lower than 600.", type=int)
parser.add_argument("-ip", help="An IP to use in lieu of the one that is fetched by this script. Useful if this machine is not the desired host for your DNS records. (More secure option, can implement your own \"IP getting\" methods instead of the one used in this script.)", type=str)
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
    client_ip = str(urlopen(_ip_fetch_).read())
    client_ip = client_ip.replace("b", "")
    client_ip = client_ip.replace("'", "")
else:
    #use the one provided
    client_ip = args.ip    
#need to account for the @ symbol being a pain in HTML
args.record = args.record.replace("@", "%40") 
#form the compostite URL to be used with GoDaddy's API (v1)
url = "https://api.godaddy.com/v1/domains/"+args.site+"/records/"+args.type+"/"+args.record+"/"
#form the headers
headers = {
    'content-type': 'application/json',
    'Authorization': 'sso-key '+auth
    }
if args.ttl and args.ttl >= _ttl_low_bound_:
    data = [
        {"data":client_ip, "ttl":args.ttl}
    ]
#save making a connection just for it to bounce back at us
elif args.ttl and args.ttl < 600: 
    sys.stderr.write("Error: TTL lower than acceptable threshold.") 
    #should really have that print to stderr though
    exit(1)
#assuming they did not provide a TTL (GoDaddy can still handle without one)
else:
    data = [
        {"data":client_ip}
    ]
if not args.nr:
    #ship the request
    r = requests.put(url, headers=headers, data=json.dumps(data))
    res = r.text #gather the result
    #perform some insurance that it executed sucessfully
    if res == "{}" and r.status_code == 200: 
        exit(0)
    #print the error and status if not
    sys.stderr.write(res) 
    r.raise_for_status()
    exit(1)
else:
    print("(nr mode)", url, headers, data)
