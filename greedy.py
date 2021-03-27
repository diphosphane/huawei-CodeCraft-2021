#!/usr/bin/env pyhon3

from itertools import count
import random
import time
from random import choice
from cloud_foundation import *
from console_IO import *
import numpy as np



class Greedy():
    def __init__(self, server_list: List[Server], daily_requests: List[DailyRequest]) -> None:
        self.server_list = server_list
        self.daily_requests = daily_requests
        # self.left_remain_core = np.array([ x.left_remain_core for x in self.server_list ])
        # self.right_remain_core = np.array([ x.right_remain_core for x in self.server_list ])
        # self.left_remain_mem = np.array([ x.left_remain_mem for x in self.server_list ])
        # self.right_remain_mem = np.array([ x.right_remain_mem for x in self.server_list ])
        self.svr_in_use: List[Server] = []
        self.svr_not_use_idx: Set[int] = set(range(len(server_list)))
    
    def run(self):
        for rq in self.daily_requests:
            node_double, node_single, mv_del = self.vm_type_classify(rq)
            for idx in node_double:
                core_rank = self.res_core_rank(node_double, rq)[::-1]
                pass
    
    @staticmethod
    def vm_type_classify(rq: DailyRequest) -> Tuple[List[int], List[int], List[int]]:
        node_double: List[int] = []  # only store idx in rq
        node_single: List[int] = []
        vm_del: List[int] = []
        for idx, ope, vm in zip(count(), rq.operation_list, rq.vm_list):
            if ope:
                if vm.double:
                    node_double.append(idx)
                else:
                    node_single.append(idx)
            else:
                vm_del.append(idx)
        return node_double, node_single, vm_del
    
    def server_classify(self):
        pass
    
    @staticmethod
    def res_core_rank(node_idx: List[int], rq: DailyRequest) -> List[int]:
        core_list = np.array([ rq.vm_list[idx].node_core for idx in node_idx ])
        sorted_idx = node_idx[core_list.argsort()].tolist()
        return sorted_idx

    @staticmethod
    def res_mem_rank(node_idx: List[int], rq: DailyRequest) -> List[int]:
        mem_list = np.array([ rq.vm_list[idx].node_mem for idx in node_idx ])
        sorted_idx = node_idx[mem_list.argsort()].tolist()
        return sorted_idx
    
    @staticmethod
    def satisfy_require(vm_core: int, vm_mem: int, svr_core: int, svr_mem: int) -> bool:
        return svr_core >= vm_core and svr_mem >= vm_mem

    def normal_greedy(self):
        # start_time = time.time()
        for iter, rq in enumerate(self.daily_requests):
            # iter_start_time = time.time()
            output = OutputCommand()
            vm_double_idxs, vm_single_idxs, vm_del_idxs = self.vm_type_classify(rq)
            # double occupy vm
            for vm_idx in vm_double_idxs:
                vm = VM.get_vm_by_id(rq.id_list[vm_idx])
                found = False
                for svr in self.svr_in_use:
                    if svr.can_put_vm_left(vm) and svr.can_put_vm_right(vm):
                        svr.add_vm_by_instance(vm, 0)
                        output.add_unorder_vm_dispatch(svr, '', vm_idx)
                        found = True
                        break
                if not found:
                    found = False
                    for svr_idx in list(self.svr_not_use_idx):
                        svr = self.server_list[svr_idx]
                        if svr.can_put_vm_left(vm):
                            self.svr_not_use_idx.remove(svr_idx)
                            self.svr_in_use.append(svr)
                            # svr.activate_server(output)
                            svr.add_vm_by_instance(vm, 0)
                            output.add_unorder_vm_dispatch(svr, '', vm_idx, new_svr=True)
                            found = True
                            break
                    if not found: raise ValueError
            for vm_idx in vm_single_idxs:
                vm = VM.get_vm_by_id(rq.id_list[vm_idx])
                found = False
                for svr in self.svr_in_use:
                    if svr.can_put_vm_left(vm):
                        svr.add_vm_by_instance(vm, -1)
                        output.add_unorder_vm_dispatch(svr, 'A', vm_idx)
                        found = True
                        break
                    if svr.can_put_vm_right(vm):
                        svr.add_vm_by_instance(vm, 1)
                        output.add_unorder_vm_dispatch(svr, 'B', vm_idx)
                        found = True
                        break
                if not found:
                    found = False
                    for svr_idx in list(self.svr_not_use_idx):
                        svr = self.server_list[svr_idx]
                        if svr.can_put_vm_right(vm):
                            self.svr_not_use_idx.remove(svr_idx)
                            self.svr_in_use.append(svr)
                            # svr.activate_server(output)
                            svr.add_vm_by_instance(vm, 1)  # add vm to right side
                            output.add_unorder_vm_dispatch(svr, 'B', vm_idx, new_svr=True)
                            found = True
                            break
                    if not found: raise ValueError
            for vm_idx in vm_del_idxs:
                vm = VM.get_vm_by_id(rq.id_list[vm_idx])
                vm.del_vm()
            output.print()
            # iter_end_time = time.time()
            # print(f'iter time: {iter_end_time - iter_start_time}')
        # end_time = time.time()
        # print(f'all time: {end_time - start_time}')


    def random_greedy(self):
        # start_time = time.time()
        for iter, rq in enumerate(self.daily_requests):
            # iter_start_time = time.time()
            output = OutputCommand()
            vm_double_idxs, vm_single_idxs, vm_del_idxs = self.vm_type_classify(rq)
            # double occupy vm
            for vm_idx in vm_double_idxs:
                vm = VM.get_vm_by_id(rq.id_list[vm_idx])
                found = False
                for svr in self.svr_in_use:
                    if svr.can_put_vm_left(vm) and svr.can_put_vm_right(vm):
                        svr.add_vm_by_instance(vm, 0)
                        output.add_unorder_vm_dispatch(svr, '', vm_idx)
                        found = True
                        break
                if not found:
                    found = False
                    while True:
                    # for svr_idx in self.svr_not_use_idx:
                        svr_idx = random.choice(list(self.svr_not_use_idx))
                        svr = self.server_list[svr_idx]
                        svr = Server(svr._type)
                        if svr.can_put_vm_left(vm):
                            self.svr_in_use.append(svr)
                            # svr.activate_server(output)
                            svr.add_vm_by_instance(vm, 0)
                            output.add_unorder_vm_dispatch(svr, '', vm_idx, new_svr=True)
                            found = True
                            break
                    if not found: raise ValueError
            for vm_idx in vm_single_idxs:
                vm = VM.get_vm_by_id(rq.id_list[vm_idx])
                found = False
                for svr in self.svr_in_use:
                    if svr.can_put_vm_left(vm):
                        svr.add_vm_by_instance(vm, -1)
                        output.add_unorder_vm_dispatch(svr, 'A', vm_idx)
                        found = True
                        break
                    if svr.can_put_vm_right(vm):
                        svr.add_vm_by_instance(vm, 1)
                        output.add_unorder_vm_dispatch(svr, 'B', vm_idx)
                        found = True
                        break
                if not found:
                    found = False
                    while True:
                    # for svr_idx in self.svr_not_use_idx:
                        svr_idx = random.choice(list(self.svr_not_use_idx))
                        svr = self.server_list[svr_idx]
                        svr = Server(svr._type)
                        if svr.can_put_vm_right(vm):
                            self.svr_in_use.append(svr)
                            # svr.activate_server(output)
                            svr.add_vm_by_instance(vm, 1)  # add vm to right side
                            output.add_unorder_vm_dispatch(svr, 'B', vm_idx, new_svr=True)
                            found = True
                            break
                    if not found: raise ValueError
            for vm_idx in vm_del_idxs:
                vm = VM.get_vm_by_id(rq.id_list[vm_idx])
                vm.del_vm()
            output.print()
            # iter_end_time = time.time()
            # print(f'iter time: {iter_end_time - iter_start_time}')
        # end_time = time.time()
        # print(f'all time: {end_time - start_time}')

    def order_greedy(self):
        start_time = time.time()
        for iter, rq in enumerate(self.daily_requests):
            # iter_start_time = time.time()
            output = OutputCommand()
            vm_double_idxs, vm_single_idxs, vm_del_idxs = self.vm_type_classify(rq)
            for vm_idx, vm in enumerate(rq.vm_list):
                if vm_idx in vm_del_idxs:
                    vm.del_vm()
                    continue
                found = False
                for svr in self.svr_in_use:
                    if vm.double:
                        if svr.can_put_vm_left(vm) and svr.can_put_vm_right(vm):
                            svr.add_vm_by_instance(vm, 0)
                            # output.add_unorder_vm_dispatch(svr.id, '', vm_idx)
                            output.add_new_vm_dispatch(svr.id, '')
                            found = True
                            break
                    else:
                        if svr.can_put_vm_left(vm):
                            svr.add_vm_by_instance(vm, -1)
                            # output.add_unorder_vm_dispatch(svr.id, 'A', vm_idx)
                            output.add_new_vm_dispatch(svr.id, 'A')
                            found = True
                            break
                        if svr.can_put_vm_right(vm):
                            svr.add_vm_by_instance(vm, 1)
                            # output.add_unorder_vm_dispatch(svr.id, 'B', vm_idx)
                            output.add_new_vm_dispatch(svr.id, 'B')
                            found = True
                            break
                        pass
                if not found:
                    for svr_idx in list(self.svr_not_use_idx):
                        svr = self.server_list[svr_idx]
                        if svr.can_put_vm_left(vm):
                            self.svr_not_use_idx.remove(svr_idx)
                            self.svr_in_use.append(svr)
                            svr.activate_server(output)
                            if vm.double:
                                svr.add_vm_by_instance(vm, 0)
                                # output.add_unorder_vm_dispatch(svr.id, '', vm_idx)
                                output.add_new_vm_dispatch(svr.id, '')
                            else:
                                svr.add_vm_by_instance(vm, 1)  # add vm to right side
                                # output.add_unorder_vm_dispatch(svr.id, 'B', vm_idx)
                                output.add_new_vm_dispatch(svr.id, 'B')
                            found = True
                            break
                    if not found: raise ValueError
            output.print()
            # iter_end_time = time.time()
            # print(f'iter time: {iter_end_time - iter_start_time}')
        end_time = time.time()
        # print(f'all time: {end_time - start_time}')