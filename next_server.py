from console_IO import *
from cloud_foundation import *

def get_server_type(vm: 'VM', server_type_list: List['ServerType'], w_elec=0) -> 'ServerType':
    core = vm.core
    memory = vm.memory
    ratio = core/memory

    capacity_list = [i for i, server in enumerate(server_type_list) if server.core > core and server.memory > memory] 
    scores = [(server_type_list[i].core/server_type_list[i].memory - ratio)**2 *(server_type_list[i].price+server_type_list[i].cost_each_day*w_elec) for i in capacity_list]
    idx=capacity_list[scores.index(min(scores))]
    return server_type_list[idx]