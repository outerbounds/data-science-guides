
import os
os.environ['METAFLOW_PROFILE'] = 'test'
from metaflow import Flow
import subprocess

def test_flow():
    cmd = ['python', 'simple_flow.py', 'run', '--run-id-file', 'test_id']
    subprocess.check_call(cmd)
    with open('test_id') as f:
        run = Flow('FlowToTest')[f.read()]
        assert run.data.x == 1
