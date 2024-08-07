from .base_sav_policy import BaseSAVPolicy

class FeasiblePathuRPF(BaseSAVPolicy):
    name: str = "Feasible-Path uRPF"

    def validate(self, as_obj, prev_hop, source):  
        # Feasible-Path uRPF is applied to only customer and peer interfaces
        if (prev_hop.asn in as_obj.provider_asns):
            return True
        else:
            for neighbor_asn, prefix_dict in as_obj.policy._ribs_in.data.items():
                for prefix, ann in prefix_dict.items():
                    if ann.as_path[-1] == source and ann.next_hop == prev_hop:
                        return True
            
            return False