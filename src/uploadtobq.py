#!/usr/bin/env python
# import argparse
import time
import uuid

from google.cloud import bigquery
from google.cloud import storage


class Bq(object):
    def __init__(self, prj, ds, tb, col):
        # 'gomi-dev' 'cindy_test'
        self.bqc = bigquery.Client(prj)
        self.ds = self.bqc.dataset(ds)
        self.tb = self.ds.table(tb)
        self.tb_tmp = None
        self.col = col
        self.start()

    def start(self):
        self.add_dataset()
        self.add_table()

    def get_projects(self):
        for project in self.bqc.list_projects():
            print(project.project_id)

    def get_datasets(self, project=None):
        # list all ds
        for dataset in self.bqc.list_datasets():
            print(dataset.name)

    def add_dataset(self):
        if not self.ds.exists():
            self.ds.create()

    def get_tables(self):
        for table in self.dc.list_tables():
            print(table.name)

    def add_table(self):
        if not self.tb.exists():
            self.tb.schema = [ bigquery.SchemaField('{}'.format(i), 'STRING', description=i) for i in self.col]
            self.tb.create()

    def get_schema(self):
        # Reload the table so that the schema is available.
        self.tb.reload()
        schema = [(i.name) for i in self.tb.schema]
        print([(i.name, i.field_type) for i in self.tb.schema])
        return schema

    def get_data(self, num):
        rows = list(self.tb.fetch_data(max_results=num))
        columns = self.get_schema()

        format_string = '{!s:<16} ' * len(columns)
        print(format_string.format(*columns))

        for row in rows:
            print(format_string.format(*row))

    def copy_table(self, src_tb, dest_tb):
        self.tb = self.ds.table(src_tb)
        self.tb_tmp = self.ds.table(dest_tb)

        job_id = str(uuid.uuid4())
        job = self.bqc.copy_table(job_id, self.tb_tmp, self.tb)
        job.create_disposition = (bigquery.job.CreateDisposition.CREATE_IF_NEEDED)
        job.begin()
        print('Waiting for job to finish...')
        wait_for_job(job)
        print('Table {} copied to {}.'.format(table_name, self.tb_tmp))

    def delete_tb(self, table_name):
        self.tb = self.ds.table(table_name)
        self.tb.delete()
        print('Table {}:{} deleted.'.format(self.ds, self.tb))

    def up(self, source_file_name, filetype='text/csv', skip_leading=0, quote="'"):
        # if not self.tb.exists():
        #     self.tb.schema = (
        #         # bigquery.SchemaField('date', 'STRING'),
        #         # bigquery.SchemaField('aqi', 'STRING'),
        #         # bigquery.SchemaField('status', 'STRING'),
        #         # bigquery.SchemaField('aqi_rank', 'STRING'),
        #         # bigquery.SchemaField('pm25', 'STRING'),
        #         # bigquery.SchemaField('pm10', 'STRING'),
        #         # bigquery.SchemaField('so2', 'STRING'),
        #         # bigquery.SchemaField('no2', 'STRING'),
        #         # bigquery.SchemaField('co', 'STRING'),
        #         # bigquery.SchemaField('o3', 'STRING'),
        #         # bigquery.SchemaField('city', 'STRING')
        #     )
        #
        #     self.tb.create()

        self.tb.reload()
        # lines = [line.rstrip('\n') for line in open(source_file_name)]
        with open(source_file_name, 'rb') as source_file:
            job = self.tb.upload_from_file(source_file, source_format=filetype, skip_leading_rows=skip_leading, quote_character=quote)

        wait_for_job(job)
        print('Loaded {} rows into {}:{}.'.format(job.output_rows, self.ds, self.tb))
        # load_data_from_file(dataset_name, table_name, source_file_name)

class St(object):
    def __init__(self, prj, bkt):
        self.stc = storage.Client(prj)
        self.bkt = self.stc.get_bucket(bkt)

        # if self.stc.lookup_bucket(self.bkt) is None:
        #     self.stc.create_bucket(self.bkt)
        #     print('Bucket {} created'.format(self.bkt))
        #     self.bkt = self.stc.get_bucket(self.bkt)

    def delete_bucket(self, bkt):
        bucket = self.stc.get_bucket(bkt)
        bucket.delete()
        print('Bucket {} deleted'.format(bucket.name))

    def all_buckets(self):
        bkts = [i.name for i in self.stc.list_buckets()]
        return bkts

    def all_blobs(self):
        all = self.bkt.list_blobs()
        blobs = [blob.name for blob in all if len(all) > 0]
        return blobs


def wait_for_job(job):
    while True:
        job.reload()
        if job.state == 'DONE':
            if job.error_result:
                raise RuntimeError(job.errors)
            return
        time.sleep(1)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    # parser.add_argument('dataset_name')
    # parser.add_argument('table_name')
    # parser.add_argument('source_file_name', help='Path to a .csv file to upload.')
    # args = parser.parse_args()
    # load_data_from_file(args.dataset_name, args.table_name, args.source_file_name)

    prj_name = 'gomi-dev'
    dataset_name = 'cindy_test'
    table_name = 'history_20170113'
    weather_schema = ['date','htemp','ltemp','status','winddir','windpower','city','updatetime']
    air_schema = ['date','aqi','status','aqi_rank','pm25', 'pm10','so2', 'no2','co', 'o3','city']
    source_file_name = "/Users/data/Desktop/cindy/weather/up/history/history_20170215.csv"

    schema = weather_schema
    
    #check schema
    with open(source_file_name) as f:
        head = [next(f).strip().split(',') for x in range(1)]
    if len(head) != len(schema):
        schema = ['col{}'.format(i) for i in range(1, len(head)+1)]

    # bqc = bigquery.Client(prj_name)
    # ds = bqc.dataset(dataset_name)
    # tb = ds.table(table_name)
    # tb.reload()
    # schema = [(i.name) for i in tb.schema]
    # print([(i.name, i.field_type) for i in tb.schema])

    # b = Bq(prj_name, dataset_name, table_name, schema)
    # b.up(source_file_name)


    # bucket_name = 'iot_weather'
    # st = St(prj_name, bucket_name)
    #
    # print(st.all_buckets())
    # print(st.all_blobs())
    # bucket_name = 'my-new-bucket'
    # bucket = stc.create_bucket(bucket_name)
    # print('Bucket {} created.'.format(bucket.name))
    # job = bigquery_client.load_table_from_storage(job_name, table, source)
    # job.begin()
    # wait_for_job(job)
    # print('Loaded {} rows into {}:{}.'.format(job.output_rows, dataset_name, table_name))
