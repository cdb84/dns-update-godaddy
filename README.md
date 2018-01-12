# dns-update-godaddy
A dynamic DNS updater and creator for the GoDaddy API

## update-godaddy.sh
You will need to incorporate your API key into this script in order for it to work properly. This spot is denoted by <API_KEY>. Insert your key and secret like so: key:secret

Usage:

`update-godaddy.sh [site] [DNS record type] [DNS record] [TTL]`

Will throw a kiniption if you are lacking any argument. 
On successful completion, will echo "{}".

## update-godaddy.py

You can provide your API key either on the command line or the program will prompt you for it.

Usage:

`update-godaddy.py [site] [type] [record] [ttl] -auth`

On successful completion, will exit with status 0. On unsuccessful completion, will return the error reported by the request made to api.godaddy.com.