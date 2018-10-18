import sys
import time
from anytree import Node as AnyTreeNode, RenderTree
from anytree.exporter import DotExporter

import zmq_connections


ports = [5000, 5001, 5002, 5003, 5004, 5005, 5006]

class Lieutenant(object):
    def __init__(self, node_id, istraitor, num_of_lieutenants=5):
        self.node_id = node_id
        self.istraitor = istraitor
        self.num_of_lieutenants = num_of_lieutenants
        self.peers = []
        temp = []
        for i in range(0, len(ports)):
            if i != 0 and i != self.node_id:
                temp.append(ports[i])
                self.peers.append(i)
        
        # setup two sockets, REP & REQ
        self.req_socket, self.req_context = zmq_connections.req_connection(temp)
        self.rep_socket, self.rep_context = zmq_connections.rep_connection(ports[node_id])

        if not istraitor:
            print('In Lieutenant %s' % node_id)
        else:
            print('In a traiter Lieutenant %s' % node_id)

# construct a node inorder to build a decision tree
    class Node(object):
        def __init__(self, value):
            self.value = value
            self.child = []
            self.decision = self.value.split(',')[0]
        
        def add_child(self, node):
            self.child.append(node)


    # Build decision tree using received messages from general and all other lieytenants
    def build_tree(self, root, orders):
        if root == None:
            return
        filtered_orders = list(filter(lambda x: root.value.split(',')[1] in x.split(',')[1] and len(root.value)+1 == len(x), orders))
        print("filtered orders",filtered_orders)
        print("orders",orders)
        for order in filtered_orders:
            child = self.Node(order)
            root.child.append(child)
            self.build_tree(child, orders)
        return root


    # Add decision part for each node
    def init_node_decision(self, root):
        if len(root.child) == 0:
            return root.value.split(',')[0]
        orders = []
        for child in root.child:
            orders.append(self.init_node_decision(child))

        attack = len(list(filter(lambda x: x.split(',')[0] == '1', orders)))
        retreat = len(list(filter(lambda x: x.split(',')[0] == '0', orders)))
        no_decision = len(list(filter(lambda x: x.split(',')[0] == 'X', orders)))

        root_decision = root.value.split(',')[0]

        # final decision is made based on own received order and orders from other lieutenants
        if root_decision == '1':
            attack += 1
        elif root_decision == '0':
            retreat += 1
        else:
            no_decision += 1
        
        # get the majority order
        majority = max(max(attack, retreat), no_decision)
        
        # make decision
        if attack == majority:
            root.decision = '1'
            return '1'
        elif retreat == majority:
            root.decision = '0'
            return '0'
        else:
            root.decision = 'X'
            return 'X'


    # Show the result tree using anytree library
    def display_tree(self, root):

        def visit_tree(root_node, root):
            if len(root.child) == 0:
                return

            # add children for current node and recursively visit the tree
            for node in root.child:
                val = '%s,%s' % (node.value, node.decision)
                child = AnyTreeNode(val, parent=root_node)
                visit_tree(child, node)
            
            return root_node
        
        root_node = visit_tree(AnyTreeNode('%s,%s' % (root.value, root.decision)), root)
       # DotExporter(root_node).to_picture("tree.png")
        for pre, fill, node in RenderTree(root_node):
            print("%s%s" % (pre, node.name))


    def orders_collection(self):
        orders = []

        # array used to record all received orders
        all_orders = []

        # receive general order
        order = self.rep_socket.recv_string()
        # Add self node_id to the end of received order
        order += str(self.node_id)
        ack = 'Acknowledgement from lieutenant %d' % self.node_id
        self.rep_socket.send_string(ack)

        orders.append(order)
        all_orders.append(orders[0][:-1])
        
        # start from round 1
        round = 1

        time.sleep(1)

        # program needs to run m+1 rounds if there are maximum m traitors
        while round <= (self.num_of_lieutenants+1)/3:
            round += 1
            new_orders = []

            # send all received order to all lieutenants
            for order in orders:
                for i in range(0, self.num_of_lieutenants):
                    if self.istraitor:
                        #send X to all
                        order = 'X,%s' % order.split(',')[1]

                    if str(self.peers[i]) in order.split(',')[1]:
                        # send an empty string if cycle exists
                        self.req_socket.send_string('')
                    else:
                        # send received order to other lieutenants
                        self.req_socket.send_string(order)

                    # listen orders from other lieutenants
                    recv_order = self.rep_socket.recv_string()
                    if len(recv_order) != 0:
                        all_orders.append(recv_order)
                        # Add self node_id to the end of received order
                        recv_order += str(self.node_id)
                        new_orders.append(recv_order)

                    # send acknowledge message back
                    ack = 'Acknowledgement from lieutenant %d' % self.node_id
                    self.rep_socket.send_string(ack)

                    # send acknowledge message back
                    self.req_socket.recv_string()
                
            orders = new_orders
            print("orders",orders)
        # build a tree using recieved messages
        root = self.Node(all_orders[0])
        result_tree = self.build_tree(root, all_orders)
        
        # Add decision part for each node and show final result
        final_decision= self.init_node_decision(result_tree)
        print("final_decision",final_decision)
        if(final_decision=='1'):
            print("All nodes will come to a final decision to attack")
        if(final_decision=='0'):
            print("All nodes will come to a final decision to retreat")
        else:
            print("No decision made")
        self.display_tree(result_tree)

        # close sockets and terminate contexts
        self.req_socket.close()
        self.req_context.term()
        self.rep_socket.close()
        self.rep_context.term()


if __name__ == '__main__':
    node_id = int(sys.argv[1])
    istraitor = sys.argv[2]
    if istraitor == 'True' or istraitor == 'true':
        istraitor = True
    else:
        istraitor = False
    lieutenant = Lieutenant(node_id=node_id, istraitor=istraitor)
    lieutenant.orders_collection()