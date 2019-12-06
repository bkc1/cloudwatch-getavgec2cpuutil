from datetime import datetime, timedelta
import sys
import boto3 
import argparse
import statistics
sys.tracebacklimit = 0

parser = argparse.ArgumentParser()
parser.add_argument('-r','--region', help='AWS region', required=True)
parser.add_argument('-i','--instance', help='EC2 instance ID', required=True)
parser.add_argument('-s','--start', help='Starting date - format YYYY-MM-DD', required=True, type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),)
parser.add_argument('-e','--end', help='Starting date - format YYYY-MM-DD', required=True, type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),)

args = parser.parse_args()

region = (args.region)
instance = (args.instance)
start = (args.start)
end = (args.end)

cloudwatch = boto3.client('cloudwatch', region_name= f"{region}" )

response = cloudwatch.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'm1',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/EC2',
                    'MetricName': 'CPUUtilization',
                    'Dimensions': [
                        {
                            "Name": "InstanceId",
                            "Value": f"{instance}"
                        },
                    ]
                },
                'Period': 3600,
                'Stat': 'Average',
            },
        },
    ],
    StartTime=f"{start}",
    EndTime=f"{end}",
)

# Parse CPUutil metric values in array, unless empty 
values_array = response['MetricDataResults'][0]['Values']

if not values_array:
  print(f"No metric data found for {instance}:")

# Calculated average from array of 1hr datapoints
cpu_util = (statistics.mean(values_array))
rounded =  str(round(cpu_util, 3))

print(f"{instance} average CPU utilization: {rounded}%")

