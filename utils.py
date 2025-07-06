from __future__ import annotations
import random
import json
from typing import Dict, Union
from collections import defaultdict
import os

def parse_probing_result(result: Union[Dict, str], cmd: str):
    lg_info = LGInfo()
    parsed_result: Dict = defaultdict(dict)

    if isinstance(result, str):
        parsed_result = "Server error"
        return parsed_result

    for vp_id, item in result.items():
        country = lg_info.vp2country[vp_id] if vp_id in vp_id else "Unknown"
        if 'error' in item[cmd].lower() or 'exception' in item[cmd].lower():
            probe_result = "LG error"
        else:
            probe_result = item[f"{cmd}_raw"]
        parsed_result[vp_id] = {
            "country": country,
            "probe_result": probe_result
        }
    return parsed_result

class LGInfo:
    def __init__(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        eyes_path = os.path.join(current_dir, 'base_data', 'eyes.json')
        lg_info_path = os.path.join(current_dir, 'base_data', 'lg_vp_info.json')

        self.eyes = json.load(open(eyes_path, 'r'))
        self.lg_info = json.load(open(lg_info_path, 'r'))

        self.as2lg, self.lg2vp, self.vp2lg, self.vp2as, self.as2vp, self.cmd2lg, self.vp2cmd, self.vp2country = self._init_data()

    
    def _init_data(self):
        as2lg = defaultdict(list)
        lg2vp = defaultdict(list)
        vp2lg: Dict[str, str] = defaultdict()
        vp2as: Dict[str, str] = defaultdict()
        as2vp = defaultdict(list)
        cmd2lg = defaultdict(list)
        vp2cmd = defaultdict(dict) # vp_id: {'ping':}
        vp2country = defaultdict()
        
        for lg in self.eyes:
            # 当前LG的配置
            cmd2lg['ping'].append(lg)
            cmd2lg['bgp'].append(lg)
            cmd2lg['traceroute'].append(lg)
            l = self.eyes[lg]
            for item in l:
                asn, vp_id = str(item['asn']), str(item['id'])

                if 'ping_cmd' in item:
                    vp2cmd[vp_id]['ping'] = item['ping_cmd']
                if 'bgp_cmd' in item:
                    vp2cmd[vp_id]['bgp'] = item['bgp_cmd']
                if 'trace_cmd' in item:
                    vp2cmd[vp_id]['traceroute'] = item['trace_cmd']
                #1. ASN -> LG
                if lg not in as2lg[asn]:
                    as2lg[asn].append(lg)
                
                #2. LG -> VP: vp_id: reply_time
                lg2vp[lg].append(vp_id)
                
                #3. vp_id -> LG 
                vp2lg[vp_id] = lg
                vp2as[vp_id] = asn
                as2vp[asn].append(vp_id)
                if vp_id in self.lg_info:
                    vp2country[vp_id] = self.lg_info[vp_id][-2]
        return as2lg, lg2vp, vp2lg, vp2as, as2vp, cmd2lg, vp2cmd, vp2country