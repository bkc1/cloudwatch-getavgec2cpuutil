## Average EC2 CPU utilization

This Python3 tool uses the Boto3 AWS SDK to get CPUutilization metrics for an EC2 instance and calculates the average across a period of time .

### Usage

```
$ python3 ec2_cpu_avg.py -r <region> -i <instance_id> -s <start_date> -e <end_date>
$ python3 ec2_cpu_avg.py -r us-east-1 -i i-0ecc7ed056e8XXXXX -s 2019-11-29 -e 2019-11-30
```

#### Get utilization across a list of instances
Must have AWScli installed

```
$ for list in `aws ec2 describe-instances --query 'Reservations[*].Instances[*].InstanceId' --output text`
do python3 ec2_cpu_avg.py -r us-west-2 -i ${list} -s 2019-11-29 -e 2019-11-30
