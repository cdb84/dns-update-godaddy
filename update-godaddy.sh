#!/bin/bash
#you must use %40 for your main (@) record since I have yet to write this script in a better language that allows me to scrub the curl statement for bad HTTP/HTML characters
#this script dynamically updates DNS records based on the public IP of the *machine it is running on*
#usage: update-godaddy.sh [site] [DNS record type] [DNS record] [TTL]
IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"
TTL=$4
RECORD=$3
TYPE=$2
SITE=$1
curl -XPUT -H "Content-type: application/json" -H 'Authorization: sso-key <API_KEY>' -d "[{\"data\": \"$IP\",\"ttl\": $TTL}]" "https://api.godaddy.com/v1/domains/$SITE/records/"$TYPE"/$RECORD"
