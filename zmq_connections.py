import zmq


# setup req connections for a node which connects with other nodes
def req_connection(ports):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    for port in ports:
        connect_str = 'tcp://localhost:%s' % port
        socket.connect(connect_str)
    return socket, context


# Setup a REP socket for a particular node
def rep_connection(port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.setsockopt(zmq.RCVBUF, 256)
    bind_str = 'tcp://*:%s' % port
    socket.bind(bind_str)
    return socket, context