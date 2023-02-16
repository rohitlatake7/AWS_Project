import json
import boto3
import io
from datetime import *
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

#Config detail
db_table_name="cleanData"
table = dynamodb.Table(db_table_name)
config_file_bucket = "config-data-clean-mumbai"
config_file_key = "config.txt"
destination_bucket = "output-data-bucket-mumbai"
deli =","
	

# Reading config file
column_header_iter = s3.Object(config_file_bucket, config_file_key).get()['Body'].iter_lines()
for row in column_header_iter:
        header_list = row.decode("utf-8", errors="ignore").split(',')


def lambda_handler(event, context):
    
    string_out = io.StringIO()
    # TODO implement
    print("dropped_column_header_list" , header_list) 
    
    # Reading input from event
    input = event.get("Records")[0]['s3']
    bucket_name = event.get("Records")[0]['s3']['bucket']['name']
    key = event.get("Records")[0]['s3']['object']['key']
    print(json.dumps(bucket_name))
    print(json.dumps(key))
    try:    
        # fetch_column_indexes returns column_indexes from CSV file which needs to dropped.
        obj = s3.Object(bucket_name, key).get()['Body'].iter_lines()
        file_header_list = next(obj).decode("utf-8", errors="ignore").split(deli)
        print(file_header_list)
        column_indexes = []
        header_list_upper = [x.upper() for x in header_list]
        for index, data in enumerate(file_header_list):
            if data.upper() in header_list_upper:
                column_indexes.append(int(index))
        column_indexes.sort(reverse=True)
        # column_indexes=column_indexes[::-1]
        print("dropped_column_header_index",column_indexes)
        
        # dropping cloumns from file header
        for index in column_indexes:
            del file_header_list[int(index)]
        string_out.write(deli.join([str(x) for x in file_header_list]) + '\n')
    
        #process the file 
        
        for line in obj:
    
            row_list = line.decode("utf-8", errors="ignore").split(deli)
            row_list_len = len(row_list)
            # print(row_list)
            # dropping required columns
            for index in column_indexes:
                if row_list_len > index:
                    del row_list[int(index)]
            # print(deli.join([str(x) for x in row_list]) + '\n')
            string_out.write(deli.join([str(x) for x in row_list]) + '\n')
        
        s3.Object(destination_bucket, key).put(Body=string_out.getvalue(), ServerSideEncryption='AES256')
        
        entry_item = {
            'destination_bucket': destination_bucket,
            'file_name': key,
            'processed_date': str(datetime.now()),
            'status': 'Successful'
            #   ,'activity_name':pii_source_file_key.split('/')[3]
        }
    
        table.put_item(
            Item=entry_item
        )
    except Exception as e:
        entry_item = {
            'destination_bucket': destination_bucket,
            'file_name': key,
            'processed_date': str(datetime.now()),
            'status': 'fail'
            #   ,'activity_name':pii_source_file_key.split('/')[3]
        }
        table.put_item(
            Item=entry_item
            )
            
    return 
