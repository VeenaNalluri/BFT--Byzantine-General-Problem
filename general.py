
import zmq_connections
import argparse


ports = [5000, 5001, 5002, 5003, 5004, 5005, 5006]


class General(object):
    def __init__(self, istraitor=0):
        self.node_id = 0
        self.istraitor = istraitor
        ports.pop(self.node_id)
        self.socket, self.context = zmq_connections.req_connection(ports)

    def general_order(self):
        try:
            if self.istraitor == 1:
                # if the general is traitor
                attack_num = int(input('Number of attack orders'))
                retreat_num = int(input('Number of retreat orders'))
                for i in range(0, attack_num):
                    #appending the node id to the order
                    order = '1, %s' % self.node_id
                    #sending the order to the lieutenants
                    self.socket.send_string(order)
                    #getting the acknowledge from lieutenants
                    ack = self.socket.recv_string()
                    print(ack)
                
                for i in range(attack_num, attack_num+retreat_num):
                    order = '0, %s' % self.node_id
                    self.socket.send_string(order)
                    ack = self.socket.recv_string()
                    print(ack)
            else:
                # if the general is not traitor, request user input and send the order to all lieutenants 
                order = input('What order does General give?\n Attack 1, Retreat 0')
                if order == '1':
                    print('Attack')
                elif order == '0':
                    print('Retreat')
                else:
                    print('Provide correct input')
                order = '%s,%s' % (order, self.node_id)

                # send round 0 order to each lieutenant
                for i in range(0, 6):
                    self.socket.send_string(order)
                    ack = self.socket.recv_string()
                    print(ack)
        except ValueError:
            print('Invalid order')
        finally:
            self.socket.close()
            self.context.term()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--faulty', type=int, default=0, choices=[0, 1], help='Is general traitor?(0/1) ')
    args = parser.parse_args()
    istraitor = args.faulty

    general = General(istraitor=istraitor)
    general.general_order()