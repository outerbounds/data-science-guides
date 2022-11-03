from metaflow import FlowSpec, step, kubernetes

class PackageSuffixesFlow(FlowSpec):
    
    query1_file = 'query1.sql'
    query2_file = 'query2.sql'
    
    def read_query(self, file):
        file_obj = open(file, 'r')
        result = file_obj.read()
        file_obj.close()
        return result
    
    @kubernetes
    @step
    def start(self):
        self.query1 = self.read_query(self.query1_file)
        self.query2 = self.read_query(self.query2_file)
        self.next(self.end)
        
    @step
    def end(self):
        print("Query 1:", self.query1)
        print("Query 2:", self.query2)

if __name__ == "__main__":
    PackageSuffixesFlow()
