"""
temp solution
"""
from .bgp import BGP
from bgpy.simulation_engine.policies.sav import StrictuRPF

class BGPWithStrictuRPF(BGP):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, source_address_validation_policy=StrictuRPF, **kwargs)
