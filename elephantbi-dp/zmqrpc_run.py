import zerorpc
import os

from ebidp.rpc_server import RPCServer

app_env = os.getenv('APP_ENV', 'develop')

rpc_server = zerorpc.Server(RPCServer())
rpc_server.bind("tcp://0.0.0.0:4242")
rpc_server.run()
