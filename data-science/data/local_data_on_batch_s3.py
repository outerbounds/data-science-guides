from metaflow import (FlowSpec, step, IncludeFile, 
                      batch, S3)
import json

class S3FileFlow(FlowSpec):
        
    data = IncludeFile('data', 
                       default='./local_data.csv')

    @step
    def start(self):
        with S3(run=self) as s3:
            res = json.dumps({'data': self.data})
            url = s3.put('data', res)
        self.next(self.read_from_batch)
        
    @batch(cpu=1)
    @step
    def read_from_batch(self):
        # change `run=self` to any run
        with S3(run=self) as s3: 
            data = s3.get('data').text
            print(f"File contents: {json.loads(data)}")
        self.next(self.end)

    @step
    def end(self):
        print('Finished reading the data!')

if __name__ == '__main__':
    S3FileFlow()
