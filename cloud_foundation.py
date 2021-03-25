#!/usr/bin/env python3

from typing import List, Tuple, Dict, Set

class ServerType():
    type_dict: Dict[str, 'ServerType'] = {}   # model -> ServerType
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
        # add type to class member variable
        self.__class__.type_dict[model] = self
    
    @classmethod
    def get_type_by_model(cls, model: str) -> 'ServerType':
        return cls.type_dict[model]


class VM_Type():
    type_dict: Dict[str, 'VM_Type'] = {}  # model -> VM_Type
    def __init__(self, model: str, core: int, memory: int, double: bool) -> None:
        # init
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
        # add type to class member variable
        self.__class__.type_dict[model] = self
    
    @classmethod
    def get_type_by_model(cls, model: str) -> 'VM_Type':
        return cls.type_dict[model]


class VM():
    vm_dict: Dict[int, 'VM'] = {}
    vm_dispach_dict: Dict[int, 'Server'] = {}           # id -> Server instance
    def __init__(self, model_type: VM_Type, id: int) -> None:
        self.id = id
        self.__class__.vm_dict[id] = self
        self._type = model_type
    
    @property
    def node_core(self) -> int:
        return self._type.node_core
    
    @property
    def node_mem(self) -> int:
        return self._type.node_mem
    
    @classmethod
    def get_vm_by_id(cls, id: int) -> 'VM':
        return cls.vm_dict[id]


class Server():
    server_dict: Dict[int, 'Server'] = {}
    server_num = 0
    def __init__(self, server_type: ServerType) -> None:
        # type init
        self._type = server_type
        self.core_lmt = self._type.core_lmt
        self.mem_lmt = self._type.mem_lmt
        # core & mem init
        self.left_core = self.right_core = 0
        self.left_mem = self.right_mem = 0
        # vm list       only store vm.id 
        self.left_vm_id_set: Set[int] = set()
        self.right_vm_id_set: Set[int] = set()
        self.double_vm_id_set: Set[int] = set()
        # core & mem remain
        self.left_remain_core = self.right_remain_core = self.core_lmt
        self.left_remain_mem = self.right_remain_mem = self.mem_lmt
        # add instance into cls.server_dict
        id = self.__class__.server_num
        self.__class__.server_dict[id] = self
        self.__class__.server_num += 1
    
    def add_vm__by_type(self, id: int, vm_type: 'VM_Type', side: int):  # -1: left  0: double  1: right
        vm = VM(vm_type, id)
        self.add_vm_by_instance(vm, side)
    
    def add_vm_by_instance(self, vm: 'VM', side: int):  # -1: left  0: double  1: right
        VM.vm_dispach_dict[vm.id] = self
        id = vm.id
        if side == -1:          # check core and memory >=0
            self.occupy_left_resource(vm)
            self.left_vm_id_set.add(id)
        elif side == 0:
            self.occupy_left_resource(vm)
            self.occupy_right_resource(vm)
            self.double_vm_id_set.add(id)
        elif side == 1:
            self.occupy_right_resource(vm)
            self.right_vm_id_set.add(id)
        else:
            raise ValueError
    
    def del_vm_by_instance(self, vm: 'VM'):
        self.del_vm_by_id(vm.id)
    
    def del_vm_by_id(self, id: int):
        del VM.vm_dispach_dict[id]
        vm = VM.get_vm_by_id(id)
        if id in self.left_vm_id_set:
            self.release_left_resource(vm)
            self.left_vm_id_set.remove(id)
        elif id in self.double_vm_id_set:
            self.release_left_resource(vm)
            self.release_right_resource(vm)
            self.double_vm_id_set.remove(id)
        elif id in self.right_vm_id_set:
            self.release_right_resource(vm)
            self.right_vm_id_set.remove(id)
        else:
            raise ValueError
    
    def occupy_left_resource(self, vm: 'VM'):
        self.left_core += vm.node_core          # resource usage
        self.left_mem += vm.node_mem
        self.left_remain_core -= vm.node_core   # resource remain
        self.left_remain_mem -= vm.node_mem
    
    def release_left_resource(self, vm: 'VM'):
        self.left_core -= vm.node_core          # resource usage
        self.left_mem -= vm.node_mem
        self.left_remain_core += vm.node_core   # resource remain
        self.left_remain_mem += vm.node_mem
    
    def occupy_right_resource(self, vm: 'VM'):
        self.right_core += vm.node_core         # resource usage
        self.right_mem += vm.node_mem
        self.right_remain_core -= vm.node_core  # resource remain
        self.right_remain_mem -= vm.node_mem
    
    def release_right_resource(self, vm: 'VM'):
        self.right_core -= vm.node_core         # resource usage
        self.right_mem -= vm.node_mem
        self.right_remain_core += vm.node_core  # resource remain
        self.right_remain_mem += vm.node_mem

    @classmethod
    def get_server_by_id(cls, id: int) -> 'Server':
        return cls.server_dict[id]
    
    @property
    def model(self) -> str:
        return self._type.model


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

