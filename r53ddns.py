from datetime import datetime
import boto3, requests
#default options
#RRSET -- DNS record
#R53HOSTEDZONE -- Route 53 hosted zone ID where dns record exists
#R53TTL -- set TTL when updating rrset
#CLIPROFILE -- AWS CLI profile to use for authentication
RRSET = 'www.example.com'
R53HOSTEDZONE = 'XXXXXXXXXX'
R53TTL = 300
CLIPROFILE = 'xxxx'
def main():
    """http request to figure out source ip"""
    host_ip = requests.get('http://checkip.amazonaws.com').text
	#setup boto3 session using aws cli profile
    session = boto3.Session(profile_name=CLIPROFILE)
    client = session.client('route53')
    #route 53 API call to check value of RRSET
    responce = client.list_resource_record_sets(
        HostedZoneId=R53HOSTEDZONE,
        StartRecordName=RRSET,
        StartRecordType='A',
        MaxItems='1'
    )
    #compare current rrset value returned by route 53
    rvalue = responce['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']
    if rvalue in host_ip:
        print('no change. r53:', rvalue, 'checkip:', host_ip)
    else:
        print('change detected. r53:', rvalue, 'checkip:', host_ip)
        r53up(host_ip)
def r53up(host_ip):
    """update DNS record with new IP"""
    session = boto3.Session(profile_name=CLIPROFILE)
    client = session.client('route53')
    client.change_resource_record_sets(
        HostedZoneId=R53HOSTEDZONE,
        ChangeBatch={
            'Comment': str(datetime.now()),
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': RRSET,
                        'Type': 'A',
                        'TTL': R53TTL,
                        'ResourceRecords': [
                            {
                                'Value': host_ip
                            },
                        ],
                    }
                },
            ]
        }
    )
    print('rrset updated successfully. new ip:', host_ip)
#go to main function when run standalone
if __name__ == '__main__':
    main()
