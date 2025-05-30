import boto3
import sys

ec2 = boto3.client('ec2')

INSTANCE_ID =[]

#インスタンス起動
def start_instance():
	ec2.start_instances(InstanceIds = INSTANCE_ID)
	print(f"Started EC2: {INSTANCE_ID}")

#インスタンス停止
def stop_instance():
	ec2.stop_instances(InstanceIds = INSTANCE_ID)
	print(f"Stopped EC2: {INSTANCE_ID}")

#インスタンス削除
def terminate_instance():
	ec2.terminate_instances(InstanceIds = INSTANCE_ID)
	print(f"Terminated EC2: {INSTANCE_ID}")

#インスタンス作成
def create_instance(image_id, instance_type, min_count, max_count, keyname, security_group_ids, name = None):
	response = ec2.run_instances(
		ImageId = image_id,
		InstanceType = instance_type,
		MinCount = int(min_count),
		MaxCount = int(max_count),
		KeyName = keyname,
		SecurityGroupIds = security_group_ids,
	)
	instance_id = response['Instances'][0]['InstanceId']
	INSTANCE_ID.append(instance_id)

	#名前指定がないとき一意にする
	if not name:
		name = f"NoName -{instance_id[-6:]}"

	ec2.create_tags(
		Resources = [instance_id],
		Tags=[
			{'key': 'Name', 'Value': name}
		]
	)

	print(f"Created EC2: {instance_id}")

#IAM内のインスタンス一覧表示
def list_instances():
	response = ec2.describe_instances()
	for reservation in response['Reservations']:
		for instance in reservation['Instances']:
			name = None
			if 'Tags' in instance:
				for tag in instance['Tags']:
					if tag['Key'] == 'Name':
						name = tag['Value']
						break
			print(f"Instance Name : {name} Instance ID: {instance['InstanceId']}  State: {instance['State']['Name']}")

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("usage : python Filename.py [start|stop|terminate|create|list] [instance_id1 instance_id2 ...]")
		sys.exit(1)

	command = sys.argv[1]

	if command == 'create':
		image_id = input("ImageId (default ami-0c1638aa346a43fe8): ") or 'ami-0c1638aa346a43fe8'
		instance_type = input("InstanceType (default t2.micro): ") or 't2.micro'
		min_count = input("MinCount (default 1): ") or '1'
		max_count = input("MaxCount (default 1): ") or '1'
		keyname = input("KeyName: ")
		security_group_ids = input("SecurityGroupIds (スペース区切り): ").split()
		name = input("Name: ")
		if not keyname:
			print("KetName is required")
			sys.exit(1)
		create_instance(image_id, instance_type, min_count, max_count, keyname, security_group_ids, name)
		sys.exit(0)

	if len(sys.argv) > 2:
		INSTANCE_ID.extend(sys.argv[2:])

	if command == 'start':
		start_instance()
	elif command == 'stop':
		stop_instance()
	elif command == 'terminate':
		print(f"Are you sure to delete instance {INSTANCE_ID}? yes/no")
		confirm = input()
		if confirm == 'yes':
			terminate_instance()
		else:
			sys.exit(1)
	elif command == 'list':
		list_instances()
	else:
		print(f"unknown command >> {command}")
