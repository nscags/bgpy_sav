from copy import deepcopy

from lib_caida_collector import AS

from .local_rib import LocalRib
from .incoming_anns import IncomingAnns
from ..enums import Relationships
from ..announcement import Announcement as Ann


class BGPPolicy:
    __slots__ = ["local_rib", "incoming_anns"]

    name = "BGP"

    def __init__(self):
        """Add local rib and data structures here

        This way they can be easily cleared later without having to redo
        the graph
        """

        self.local_rib = LocalRib()
        self.incoming_anns = IncomingAnns()

    def propagate_to_providers(policy_self, self):
        """Propogates to providers"""

        send_rels = set([Relationships.ORIGIN, Relationships.CUSTOMERS])
        policy_self._propagate(self, Relationships.PROVIDERS, send_rels)

    def propagate_to_customers(policy_self, self):
        """Propogates to customers"""

        send_rels = set([Relationships.ORIGIN,
                         Relationships.PEERS,
                         Relationships.PROVIDERS])
        policy_self._propagate(self, Relationships.CUSTOMERS, send_rels)

    def propagate_to_peers(policy_self, self):
        """Propogates to peers"""

        send_rels = set([Relationships.ORIGIN,
                         Relationships.CUSTOMERS])
        policy_self._propagate(self, Relationships.PEERS, send_rels)

    def _propagate(policy_self, self, propagate_to: Relationships, send_rels: list):
        """Propogates announcements from local rib to other ASes

        send_rels is the relationships that are acceptable to send

        Later you can change this so it's not the local rib that's
        being sent. But this is just proof of concept.
        """

        for as_obj in getattr(self, propagate_to.name.lower()):
            for prefix, ann in policy_self.local_rib.items():
                if ann.recv_relationship in send_rels:
                    # Add the new ann to the incoming anns for that prefix
                    if as_obj.policy.incoming_anns.get(prefix) is None:
                        as_obj.policy.incoming_anns[prefix] = list()
                    as_obj.policy.incoming_anns[prefix].append(ann)

    def process_incoming_anns(policy_self, self, recv_relationship: Relationships):
        """Process all announcements that were incoming from a specific rel"""

        for prefix, ann_list in policy_self.incoming_anns.items():
            # Get announcement currently in local rib
            best_ann = policy_self.local_rib.get(prefix)

            # Done here to optimize
            if best_ann is not None and best_ann.seed_asn is not None:
                continue
            if best_ann is None:
                best_ann = deepcopy(ann_list[0])
                best_ann.seed_asn = None
                best_ann.as_path = (self.asn, *best_ann.as_path)
                best_ann.recv_relationship = recv_relationship
                # Save to local rib
                policy_self.local_rib[prefix] = best_ann

            # For each announcement that was incoming
            for ann in ann_list:
                # BGP Loop Prevention Check
                if self.asn in ann.as_path:
                    continue
                new_ann_is_better = policy_self._new_ann_is_better(self, best_ann, ann, recv_relationship)
                # If the new priority is higher
                if new_ann_is_better:
                    # Don't bother tiebreaking, if priority is same, keep existing
                    # Just like normal BGP
                    # Tiebreaking with time and such should go into the priority
                    # If we ever decide to do that
                    best_ann = deepcopy(ann)
                    best_ann.seed_asn = None
                    best_ann.as_path = (self.asn, *ann.as_path)
                    best_ann.recv_relationship = recv_relationship
                    # Save to local rib
                    policy_self.local_rib[prefix] = best_ann
            policy_self.incoming_anns = IncomingAnns()

    def _new_ann_is_better(policy_self, self, deep_ann, shallow_ann, recv_relationship: Relationships):
        """Assigns the priority to an announcement according to Gao Rexford"""

        if deep_ann.recv_relationship.value > recv_relationship.value:
            return False
        elif deep_ann.recv_relationship.value < recv_relationship.value:
            return True
        else:
            if len(deep_ann.as_path) < len(shallow_ann.as_path) + 1:
                return False
            elif len(deep_ann.as_path) > len(shallow_ann.as_path) + 1:
                return True
            else:
                if deep_ann.as_path[0] <= self.asn:
                    return False
                else:
                    return True
