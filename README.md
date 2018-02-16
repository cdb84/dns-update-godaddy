# dns-update-godaddy
A dynamic DNS updater and creator for the GoDaddy API.

## Usage
Please note that when using either of these scripts, the safest option is to provide an IP address in the arguments and provide authorization tokens in the actual execution of the program, when prompted. Not providing an IP forces the script to contact another server to requisition an IP for the client, which in some cases can be risky if the server the script contacts gets comprimised. 

### update-godaddy.py

`update-godaddy.py site type record [--ttl T] [--auth A] [-ip IP] [-nr]`

On successful completion, will exit with status 0 and print a succesful message. On unsuccessful completion, will return the error reported by the request made to api.godaddy.com. If the specified DNS record does not exist, one will be created in the execution of this script.

examples: 

`python3 update-godaddy.py google.com A @ --ttl 3600 --auth A98utwhuow49cpjcasjdd:21hf19348f2jhhiasd9f`

`python3 update-godaddy.py cnn.com A mail --ttl 600`

### check-and-modify.py

`check-and-modify.py site type record [--ttl T] [--auth A] [-ip IP] [-nr]`

check-and-modify will contact the GoDaddy API servers and see if the host computer's IP or IP indicated by `-ip` matches the record stored with GoDaddy. If it does, it will do nothing and exit. If it does not, it will update the record accordingly.

## Known Issues
When using either script on Windows Powershell, @ must be replaced as "@" in the command arguments.

## Dependencies

1. Python "requests" library: `pip install requests`
