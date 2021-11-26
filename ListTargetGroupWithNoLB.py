#sudo pip3 install PTable

import boto3
import pprint
from prettytable import PrettyTable
from pprint import pprint

getprofilelist = ['default']
session=boto3.session.Session(profile_name="default")
temp_dict = {"default":[]}
data = {"default":[]}

elb = session.client(service_name="elbv2",region_name="us-east-1")

def updatedict(account,TargetGroupName,Protocol,TargetType):
  if account == "default":
    account = "default"
  tgname = TargetGroupName
  protocol = Protocol
  targettype = TargetType
  if tgname not in temp_dict[account]:
    temp_dict[account].append(tgname)
    data[account].append([tgname,protocol,targettype])

for item_profile in getprofilelist:
  marker = None
  get_profile_session = boto3.session.Session(profile_name=item_profile)
  client = get_profile_session.client('elbv2')
  response = client.describe_target_groups()
  for i in response['TargetGroups']:
    if not i['LoadBalancerArns']:
      updatedict(item_profile,i['TargetGroupName'],i['Protocol'],i['TargetType'])
    else:
      continue
  try:
    marker = response['Marker']
    while True:
      response1 = client.describe_target_groups(Marker=marker)
      for j in response1['TargetGroups']:
        if not j['LoadBalancerArns']:
          updatedict(item_profile,j['TargetGroupName'],j['Protocol'],j['TargetType'])
        else:
          continue
      try:
        marker = response1['Marker']
      except KeyError:
        break
  except KeyError:
    print("**************************")

eastaccount_table = PrettyTable(["TargetGroupName","Protocol","TargetType"])

for item_data in data.keys():
  if item_data == "default":
    for k in data[item_data]:
      eastaccount_table.add_row([k[0],k[1],k[2]])
  else:
    print("No Table") 

print(eastaccount_table)
