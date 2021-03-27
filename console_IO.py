#!/usr/bin/env python3

import sys
from typing import List, Tuple, Dict, Set, DefaultDict
from cloud_foundation import Server, ServerType, VM, VM_Type
from collections import defaultdict

class DailyRequest():
    add_cmd = True
    del_cmd = False
    def __init__(self) -> None:
        self.operation_list: List[bool] = []
        self.id_list: List[int] = []
        self.vm_list: List[VM] = []
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
                self.operation_list.append(self.add_cmd)
                self.id_list.append(id)
                self.vm_list.append(vm)
            else:
                id = int(command_args[1])
                self.operation_list.append(False)
                self.id_list.append(id)
                self.vm_list.append(VM.get_vm_by_id(id))


class OutputCommand():
    # (purchase, 2)                -> purchase type
    # (NV603, 1)                   -> purchase number
    # (NV604, 1)                   
    # (migration, 1)               -> migration number
    # (vm_id, server_id[, node])   -> migration instance
    # (server_id[, node])          -> deployment instance (corresponds to input)
    # (0, B)
    purchase_server_type_num = '(purchase, %d)\n'
    purchase_server_model_num = '(%s, %d)\n'
    migration_num = '(migration, %d)\n'
    migration_vm_server_node = '(%d, %d, %s)\n'
    migration_vm_server = '(%d, %d)\n'
    deploy_server_node = '(%d, %s)\n'
    deploy_server = '(%d)\n'
    command_list: List['OutputCommand'] = []

    def __init__(self) -> None:
        self.server_dict: DefaultDict[str, int] =  defaultdict(int)        # [(server_model, number), ...]
        # self.server_purchase_list: List[str] = []        # [(server_model, number), ...]
        # self.migration_list: List[Tuple[int, int, str]] = [] # [(vm_id, server_id, node), ...]   node=A/B/null
        # self.deploy_list: List[Tuple[int, int]] = []         # [(server_id, node)]      mode=A/B/null
        self.migration_str = ''
        self.migration_count = 0
        self.deploy_str = ''
        self.server_to_be_activate: List[Server] = []
        self.deploy_history: List[Tuple[Server, str]] = []
        self.idx_of_deploy: List[int] = []
        self.deploy_unorder_str_list: List[str] = []
    
    @classmethod
    def new_instance(cls):
        cls.command_list.append(OutputCommand())
    
    def add_server(self, server_type: ServerType, num: int=1):
        # for _ in range(num):
        #     self.server_purchase_list.append(server_type.model)
        self.server_dict[server_type.model] += num
    
    def add_migration(self, vm: VM, server: Server, node: str):
        if node:
            self.migration_str += self.migration_vm_server_node % (vm.id, server.id, node)
            # self.migration_list.append((vm.id, server.id, node))
        else:
            self.migration_str += self.migration_vm_server % (vm.id, server.id)
            # self.migration_list.append((vm.id, server.id, ''))
        self.migration_count += 1
    
    def add_new_vm_dispatch(self, server: 'Server', node: str, new_svr: bool=False):
        if new_svr:
            self.add_server(server._type)
            self.server_to_be_activate.append(server)
        # if node:
        #     self.deploy_str += self.deploy_server_node % (server_id, node)
        # else:
        #     self.deploy_str += self.deploy_server % (server_id)
        self.deploy_history.append((server, node))
    
    def add_unorder_vm_dispatch(self, server: 'Server', node: str, idx: int, new_svr: bool=False):
        if new_svr:
            self.add_server(server._type)
            self.server_to_be_activate.append(server)
        # if node:
        #     tmp = self.deploy_server_node % (server_id, node)
        # else:
        #     tmp = self.deploy_server % (server_id)
        # self.deploy_unorder_str_list.append(tmp)
        self.idx_of_deploy.append(idx)
        self.deploy_history.append((server, node))
    
    def get_vm_dispatch_str(self) -> List[str]:
        # activate server
        for model in self.server_dict.keys():
            for svr in self.server_to_be_activate:
                if svr.model == model:
                    svr.activate_server()
        return_list: List[str] = []
        for svr, node in self.deploy_history:
            if node:
                tmp = self.deploy_server_node % (svr.id, node)
            else:
                tmp = self.deploy_server % svr.id
            return_list.append(tmp)
        return return_list
    
    def print(self):
        print(self.purchase_server_type_num % len(self.server_dict), end='')
        # print(self.purchase_server_type_num % len(self.server_purchase_list), end='')
        for model, num in self.server_dict.items():
            print(self.purchase_server_model_num % (model, num), end='')
        # for model in self.server_purchase_list:
        #     print(self.purchase_server_model_num % (model, 1), end='')
        print(self.migration_num % self.migration_count, end='')
        print(self.migration_str, end='')
        if self.idx_of_deploy:
            for line in (x[1] for x in sorted(zip(self.idx_of_deploy, self.get_vm_dispatch_str()), key=lambda x: x[0])):
                print(line, end='')
        else:
            for line in self.get_vm_dispatch_str():
                print(line, end='')
        # if self.idx_of_deploy:
        #     for deploy_txt in (x[1] for x in sorted(zip(self.idx_of_deploy, self.deploy_unorder_str_list), key=lambda x: x[0])):
        #         print(deploy_txt, end='')
        # else:
        #     print(self.deploy_str, end='')
        sys.stdout.flush()

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

