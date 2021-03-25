#!/usr/bin/env python3

from typing import List, Tuple, Dict, Set
from cloud_foundation import Server, ServerType, VM, VM_Type

class DailyRequest():
    add_cmd = True
    del_cmd = False
    def __init__(self) -> None:
        self.operation: List[bool] = []
        self.id: List[int] = []
        self.vm: List[VM] = []
        self.read_one_day()
    
    def read_one_day(self):
        task_num = int(input())
        for _ in range(task_num):
            line = input().strip()[1: -1]
            command_args = line.split(',')
            if command_args[0].strip() == 'add':
                vm_model, id = command_args[1].strip(), int(command_args[2])
                vm_type = VM_Type.type_dict[vm_model]
                vm = VM(vm_type, id)
                self.operation.append(self.add_cmd)
                self.id.append(id)
                self.vm.append(vm)
            else:
                id = int(command_args[1])
                self.operation.append(False)
                self.id.append(id)
                self.vm.append(VM.get_vm_by_id(id))


class OutputCommand():
    # (purchase, 2)                -> purchase type
    # (NV603, 1)                   -> purchase number
    # (NV604, 1)                   
    # (migration, 1)               -> migration number
    # (vm_id, server_id[, node])   -> migration instance
    # (server_id[, node])          -> deployment instance (corresponds to input)
    # (0, B)
    purchase_server_type_num = '(purchase, %d)'
    purchase_server_model_num = '(%s, %d)'
    migration_num = '(migration, %d)'
    migration_vm_server_node = '()'
    def __init__(self) -> None:
        
        pass
    pass

def read_server_vm_inp() -> Tuple[List[ServerType], List[VM_Type]]:
    server_type_num = int(input())
    server_type_list: List[ServerType] = []
    for _ in range(server_type_num):
        line = input().strip()[1: -1]
        model, core, memory, price, cost_each_day = line.split(',')
        server_type_list.append(ServerType( model.strip(),
                                            int(core), 
                                            int(memory), 
                                            int(price), 
                                            int(cost_each_day)))
    vm_type_num = int(input())
    vm_type_list: List[VM_Type] = []
    for _ in range(vm_type_num):
        line = input().strip()[1: -1]
        model, core, memory, double = line.split(',')
        vm_type_list.append(VM_Type(model.strip(), 
                                    int(core),
                                    int(memory),
                                    bool(int(double))))
    return server_type_list, vm_type_list

def read_daily_inp() -> Tuple[int, List[DailyRequest]]:
    day_num = int(input())
    requests: List[DailyRequest] = []
    for _ in range(day_num):
        requests.append(DailyRequest())
    return day_num, requests

