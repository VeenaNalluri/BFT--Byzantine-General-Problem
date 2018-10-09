# assignment-4-BFT

Due Date 17th October 11:59 PM

Implement the BFT algorithm (class slides) (python)  using the client server synchronous communication pattern from zeromq http://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/client_server.html

Assume there are 7 nodes. All nodes need to be connected to all other nodes. The port numbers are statically decided. Submit your code and a readme showing the results of upto 2 failure of nodes. During the setup assume that the nodes are deciding between attacking and retreating. Assume that the primary general is already known. You will also have to make the faulty nodes. To mark the node as faulty use a command line parameter. During test we will only mark upto two nodes as faulty.
