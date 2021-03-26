from greedy import Greedy
from getServer import get_server_list
from cloud_foundation import ServerType, VM_Type, VM, Server
from console_IO import DailyRequest, read_server_vm_inp, read_daily_inp

def main():
    # to read standard input
    # process
    # to write standard output
    # sys.stdout.flush()
    pass


if __name__ == "__main__":
    main()
    # read file
    server_type, vm_type = read_server_vm_inp()
    day_num, request_list = read_daily_inp()
    # server_list
    server_list = get_server_list(server_type, vm_type, request_list, 1, 256, 128, 128, 1.618)
    # print(len(server_list), [i._type.cost_each_day for i in server_list[:4]])
    greedy = Greedy(server_list, request_list)
    greedy.normal_greedy()
    # purchase server
    # Greedy()