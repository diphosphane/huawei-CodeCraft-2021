from cloud_foundation import *
from console_IO import *
import numpy as np

def get_usage_list(vm_type: List[VM_Type], request_list: List[DailyRequest]):
    usage_list = []
    # threshold_list = []
    core=0
    memory=0
    node_core=0
    node_mem=0
    # single_core_max=0
    # single_memory_max=0
    for day in range(len(request_list)):
        core_max_today = core
        memory_max_today = memory
        node_core_max_today = node_core
        node_mem_max_today = node_mem
        for event in range(len(request_list[day].operation)):
            if request_list[day].operation[event]:
                core += request_list[day].vm[event].core
                memory += request_list[day].vm[event].memory
                node_core += request_list[day].vm[event].node_core
                node_mem += request_list[day].vm[event].node_mem
            else:
                core -= request_list[day].vm[event].core
                memory -= request_list[day].vm[event].memory
                node_core -= request_list[day].vm[event].node_core
                node_mem -= request_list[day].vm[event].node_mem
            core_max_today = max(core_max_today, core)
            memory_max_today = max(memory_max_today, memory)
            node_core_max_today = max(node_core_max_today, node_core)
            node_mem_max_today = max(node_mem_max_today, node_mem)

        usage_list.append([core_max_today, memory_max_today, node_core_max_today, node_mem_max_today])
    
    return usage_list

def get_best_servers(server_types: List[ServerType], w_mem=1, w_elec=0, core_threshold=0, mem_threshold=0) -> List[ServerType]:
    score_list = []
    # def func()
    for server_type in server_types:
        if server_type.core > core_threshold and server_type.memory > mem_threshold:
            score_list.append((server_type.price+w_elec*server_type.cost_each_day)/(server_type.core+server_type.memory*w_mem))
    idx = np.argsort(score_list)
    best_servers = np.array(server_types)[idx]
    return best_servers
    
def get_server_list(server_types: List[ServerType], vm_type: List[VM_Type], request_list: List[DailyRequest], w_mem=1, w_elec=0, core_threshold=0, mem_threshold=0, magicn_number=1.618) -> List[Server]:
    usage_list = get_usage_list(vm_type, request_list)
    best_servers =  get_best_servers(server_types, w_mem=w_mem, w_elec=w_elec, core_threshold=core_threshold, mem_threshold=mem_threshold)
    core_max = max(usage_list[0])
    memory_max = max(usage_list[1])

    server_list = []
    print(core_max,memory_max)
    server_number = int(max(core_max//best_servers[0].core, memory_max//best_servers[0].memory)*magicn_number)
    for _ in range(server_number):
        server_list.append(Server(best_servers[0]))
    
    return server_list