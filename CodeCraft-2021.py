from greedy import Greedy
from getServer import get_server_list
from cloud_foundation import ServerType, VM_Type, VM, Server
from console_IO import DailyRequest, read_server_vm_inp, read_daily_inp
from typing import List
import time

def main():
    # to read standard input
    # process
    # to write standard output
    # sys.stdout.flush()
    pass


if __name__ == "__main__":
    start = time.time()
    # read file
    server_type, vm_type = read_server_vm_inp()
    day_num, request_list = read_daily_inp()
    # server_list = get_server_list(server_type, vm_type, request_list, 1, 256, 128, 128, 1.618)
    # print(len(server_list), [i._type.cost_each_day for i in server_list[:4]])
    # server_list = [ Server(x) for x in server_type ]
    server_list: List[Server] = []
    # server_pre = Server(ServerType.get_type_by_model('hostV871Y'))
    # server_list = [server_pre] + server_list
    for svr_type in server_type:
        model = svr_type.model
        server_list.append(Server(ServerType.get_type_by_model(model)))
    # server_list = [server_pre] +  server_list
    greedy = Greedy(server_list, request_list)
    # greedy.normal_greedy()
    # greedy.order_greedy()
    greedy.random_greedy()
    # purchase server
    # Greedy()
    end = time.time()
    # print(f'total time: {end - start}')
