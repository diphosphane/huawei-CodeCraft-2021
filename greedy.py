#!/usr/bin/env pyhon3

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
        
        pass
    
    