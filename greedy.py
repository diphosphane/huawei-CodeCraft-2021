#!/usr/bin/env pyhon3

from itertools import count
from cloud_foundation import *
from console_IO import *
import numpy as np


class Greedy():
    def __init__(self, server_list: List[Server], daily_requests: List[DailyRequest]) -> None:
        self.server_list = server_list
        self.daily_requests = daily_requests
        self.left_remain_core = np.array([ x.left_remain_core for x in self.server_list ])
        self.right_remain_core = np.array([ x.right_remain_core for x in self.server_list ])
        self.left_remain_mem = np.array([ x.left_remain_mem for x in self.server_list ])
        self.right_remain_mem = np.array([ x.right_remain_mem for x in self.server_list ])
        self.in_use = [False for _ in range(len(server_list))]
    
    def run(self):
        for rq in self.daily_requests:
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
    
    @staticmethod
    def res_big_core_idx(node_idx: List[int], rq: DailyRequest) -> List[int]:
        vm_list = [ rq.vm_list[idx] for idx in node_idx ]
        core_list = np.array([ vm.node_core for vm in vm_list]) 
        
        