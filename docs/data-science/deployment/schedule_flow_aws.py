from metaflow import FlowSpec, schedule, step
from datetime import datetime

@schedule(daily=True)
class DailyFlowAWS(FlowSpec):

    @step
    def start(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('time is %s' % now)
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == '__main__':
    DailyFlowAWS()
