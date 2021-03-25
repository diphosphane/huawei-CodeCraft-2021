#!/usr/bin/env python3

from dataclasses import dataclass
import numpy as np
from typing import List, Tuple, Any, Union, Dict

##### type define #####
class ServerType():
    type_dict: Dict[str, 'ServerType'] = {}
    def __init__(self, model: str, core: int, memory: int, price: int, cost_each_day: int) -> None:
        # init
        self.model = model
        self.core = core
        self.memory = memory
        self.price = price
        self.cost_each_day = cost_each_day
        # resource limitation
        self.core_lmt = self.core // 2
        self.mem_lmt = self.memory // 2


class VM_Type():
    type_dict: Dict[str, 'VM_Type'] = {}
    def __init__(self, model: str, core: int, memory: int, double: bool) -> None:
        self.model = model
        self.core = core
        self.memory = memory
        self.double = double
        # node requirement
        if self.double:
            self.node_core = self.core // 2
            self.node_mem = self.memory // 2
        else:
            self.node_core = self.core
            self.node_mem = self.memory


class VM():
    vm_dict: Dict[int, 'VM'] = {}
    vm_dispach_dict: Dict[int, 'Server'] = {}           # id -> Server instance
    def __init__(self, model: Union[str, VM_Type], id: int) -> None:
        self.id = id
        if type(model) is str:
            self._type = VM_Type.type_dict[model]
        else:
            self._type: VM_Type = model
        self.__class__.vm_dict[id] = self
    
    @property
    def node_core(self) -> int:
        return self._type.node_core
    
    @property
    def node_mem(self) -> int:
        return self._type.node_mem


class Server():
    server_dict: Dict[int, 'Server'] = {}
    def __init__(self, server_type: ServerType) -> None:
        # type init
        self._type = server_type
        self.core_lmt = self._type.core_lmt
        self.mem_lmt = self._type.mem_lmt
        # core & mem init
        self.left_core = self.right_core = 0
        self.left_mem = self.right_mem = 0
        # vm list       only store vm.id 
        self.left_vm: List[int] = []
        self.right_vm: List[int] = []
        self.double_vm: List[int] = []
        # core & mem remain
        self.left_remain_core = self.right_remain_core = self.core_lmt
        self.left_remain_mem = self.right_remain_mem = self.mem_lmt
    
    def add_vm_type(self, id: int, vm_type: 'VM_Type', side: int):  # -1: left  0: double  1: right
        vm = VM(vm_type.model, id)
        self.add_vm(vm, side)
    
    def add_vm(self, vm: 'VM', side: int):  # -1: left  0: double  1: right
        VM.vm_dispach_dict[vm.id] = self
        if side == -1:          # check core and memory >=0
            self.left_core += vm.node_core          # resource usage
            self.left_mem += vm.node_mem
            self.left_remain_core -= vm.node_core   # resource remain
            self.left_remain_mem -= vm.node_mem
            self.left_vm.append(vm.id)
        elif side == 0:
            self.left_core += vm.node_core          # resource usage
            self.right_core += vm.node_core
            self.left_mem += vm.node_mem
            self.right_mem += vm.node_mem
            self.left_remain_core -= vm.node_core   # resource remain
            self.right_remain_core -= vm.node_core
            self.left_remain_mem -= vm.node_mem
            self.right_remain_mem -= vm.node_mem
            self.double_vm.append(vm.id)
        elif side == 1:
            self.right_core += vm.node_core         # resource usage
            self.right_mem += vm.node_mem
            self.right_remain_core -= vm.node_core  # resource remain
            self.right_remain_mem -= vm.node_mem
            self.right_vm.append(vm.id)
        else:
            raise ValueError


##### input class #####
@dataclass
class UserOperation():
    add: bool  # True: add, False: del
    model: str
    id: int


##### output class #####
@dataclass
class DispatchOperation():
    # (purchase, 2)                -> purchase type
    # (NV603, 1)                   -> purchase number
    # (NV604, 1)                   
    # (migration, 1)               -> migration number
    # (vm_id, server_id[, node])   -> migration instance
    # (server_id[, node])          -> deployment instance
    # (0, B)
    pass

# read input
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
day_num = int(input())
for _ in range(day_num):
    task_num = int(input())
    for _ in range(task_num):
        line = input().strip()[1: -1]
        command_args = line.split(',')
        if command_args[0].strip() == 'add':
            vm_model, id = command_args[1].strip(), int(command_args[2])
            # todo: add vm
        else:
            id = int(command_args[1])
            # todo: delete vm

##### main algorithm #####

# todo: check the price-performance ratio in server
# todo: pin the server
# 