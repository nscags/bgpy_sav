"""
temp solution
"""
from bgpy.simulation_engine import BGP, StrictuRPF

class BGPWithStrictuRPF(BGP):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, source_address_validation_policy=StrictuRPF, **kwargs)
