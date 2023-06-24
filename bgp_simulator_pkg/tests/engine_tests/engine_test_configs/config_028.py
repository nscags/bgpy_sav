from bgp_simulator_pkg.tests.engine_tests.graphs import graph_040
from bgp_simulator_pkg.tests.engine_tests.utils import EngineTestConfig

from bgp_simulator_pkg.simulation_engine import BGPSimpleAS
from bgp_simulator_pkg.simulation_framework import ScenarioConfig, ValidPrefix


config_028 = EngineTestConfig(
    name="028",
    desc="Test of peer preference",
    scenario_config=ScenarioConfig(
        ScenarioCls=ValidPrefix,
        BaseASCls=BGPSimpleAS,
        num_victims=2,
        override_victim_asns={2, 3},
        override_non_default_asn_cls_dict=dict(),
    ),
    graph=graph_040,
)
