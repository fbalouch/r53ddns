# r53ddns
Route 53 DDNS client written in python using boto3 and requests.

# function
This script determines the public ip of a host using http://checkip.amazonaws.com. The public ip returned by the checkip endpoint is used as the client's public ip. The returned ip is compared against an existing A record in Route 53 and updated if there is a change.

# authentication
The script builds a boto3 session using a predefined aws cli profile.
