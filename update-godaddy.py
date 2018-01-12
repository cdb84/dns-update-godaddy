#!/usr/bin/python3
import requests, json
import argparse
import getpass
from urllib.request import urlopen
#curl -XPUT -H "Content-type: application/json" -H 'Authorization: sso-key <API_KEY>' -d "[{\"data\": \"$IP\",\"ttl\": $TTL}]" "https://api.godaddy.com/v1/domains/$SITE/records/"$TYPE"/$RECORD"

client_ip = str(urlopen("https://api.ipify.org").read())
client_ip = client_ip.replace("b", "")
client_ip = client_ip.replace("'", "")

parser = argparse.ArgumentParser(description="A script to dynamically update and/or create your site's GoDaddy DNS records.")
parser.add_argument("site", help="The fully qualified domain name of the particular site.", type=str)
parser.add_argument("typ", help="The type of the record that is being updated. A, AAAA, MX, SRV, etc.", type=str)
parser.add_argument("record", help="Actual record name, i.e. for gmail.google.com the record would be gmail. If the specified record does not exist, one will be created.", type=str)
parser.add_argument("-t", "--ttl", help="Time to live, in seconds. Cannot be lower than 600.", type=int)
parser.add_argument("-a", "--auth", help="Your API key:secret pair.", type=str)

args = parser.parse_args()
if not args.auth:
    auth=getpass.getpass()
else:
    auth=args.auth
    

url = "https://api.godaddy.com/v1/domains/"+args.site+"/records/"+args.typ+"/"+args.record+"/"

headers = {
    'content-type': 'application/json',
    'Authorization': 'sso-key '+auth
    }
if args.ttl and args.ttl >= 600:
    data = [
        {"data":client_ip, "ttl":args.ttl}
    ]
elif args.ttl and args.ttl <= 600:
    print("Error: TTL lower than acceptable threshold.")
    exit(1)
else:
    data = [
        {"data":client_ip}
    ]
r = requests.put(url, headers=headers, data=json.dumps(data))
res = r.text
if res == "{}" and r.status_code == 200:
    exit(0)
print(res)
r.raise_for_status()
exit(1)