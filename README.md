# dns-update-godaddy
A dynamic DNS updater and creator for the GoDaddy API.

## update-godaddy.py
Usage:

`update-godaddy.py site type record [--ttl T] [--auth A]`

On successful completion, will exit with status 0. On unsuccessful completion, will return the error reported by the request made to api.godaddy.com. If the specified DNS record does not exist, one will be created in the execution of this script.