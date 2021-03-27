from console_IO import *
from cloud_foundation import *
import random

def get_server_type(vm: 'VM', server_type_list: List['ServerType'], w_elec=0) -> 'ServerType':
    core = vm.node_core
    memory = vm.node_mem
    ratio = core/memory

    capacity_list = [i for i, server in enumerate(server_type_list) if server.core_lmt > core and server.mem_lmt > memory] 
    # scores = [(server_type_list[i].core/server_type_list[i].memory - ratio)**2 *(server_type_list[i].price+server_type_list[i].cost_each_day*w_elec) for i in capacity_list]
    scores = [((server_type_list[i].core/server_type_list[i].memory - ratio)**2 *(server_type_list[i].price+server_type_list[i].cost_each_day*w_elec)/(server_type_list[i].core+(0.5+random.random())*server_type_list[i].memory)**(w_elec/16))*random.random() for i in capacity_list]
    idx=capacity_list[scores.index(min(scores))]
    return server_type_list[idx]