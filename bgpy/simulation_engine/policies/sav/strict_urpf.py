from bgpy.as_graphs import AS
from .base_sav_policy import BaseSAVPolicy

class StrictuRPF(BaseSAVPolicy):
    """
    """

    def validate(self, as_obj: AS, prev_hop: AS, source):
        # Strict uRPF is applied to only customer and peer interfaces
        if (prev_hop.asn not in as_obj.customer_asns or
            prev_hop.asn not in as_obj.peer_asns):
            return True
        else:
            # Get announcement to source address
            for ann in as_obj.policy._local_rib.data.values():
                if ann.as_path[-1] == source:
                    source_ann = ann

            # check if interfaces match (symmetric route)
            if source_ann.next_hop.asn == prev_hop.asn:
                return True
            else:
                return False