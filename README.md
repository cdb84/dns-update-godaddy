# dns-update-godaddy
A dynamic DNS updater and creator for the GoDaddy API.

## update-godaddy.py
Usage:

`update-godaddy.py site type record [--ttl T] [--auth A]`

On successful completion, will exit with status 0. On unsuccessful completion, will return the error reported by the request made to api.godaddy.com. If the specified DNS record does not exist, one will be created in the execution of this script.

examples: 

`python3 update-godaddy.py google.com A @ --ttl 3600 --auth A98utwhuow49cpjcasjdd:21hf19348f2jhhiasd9f`

`python3 update-godaddy.py cnn.com A mail --ttl 600`
