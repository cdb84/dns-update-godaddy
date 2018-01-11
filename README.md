# dns-update-godaddy
A dynamic DNS updater for the GoDaddy API

You will need to incorporate your production key into this script in order for it to work properly. This spot is denoted by <API_KEY>. Insert your key and secret like so: key:secret

Usage:

`update-godaddy.sh [site] [DNS record type] [DNS record] [TTL]`

Will throw a kiniption if you are lacking any argument. 
On successful completion, will echo "{}".
