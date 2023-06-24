from bgp_simulator_pkg.tests.engine_tests.graphs import graph_019
from bgp_simulator_pkg.tests.engine_tests.utils import EngineTestConfig

from bgp_simulator_pkg.simulation_engine import BGPSimpleAS
from bgp_simulator_pkg.enums import ASNs
from bgp_simulator_pkg.simulation_framework import ScenarioConfig, ValidPrefix


config_023 = EngineTestConfig(
    name="023",
    desc="Test of tiebreak preference",
    scenario_config=ScenarioConfig(
        ScenarioCls=ValidPrefix,
        BaseASCls=BGPSimpleAS,
        override_attacker_asns={ASNs.ATTACKER.value},
        override_victim_asns={ASNs.VICTIM.value},
        override_non_default_asn_cls_dict=dict(),
    ),
    graph=graph_019,
)
