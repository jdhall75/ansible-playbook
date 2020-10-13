from pybatfish.client.commands import (
    bf_session,
    bf_set_network,
    bf_init_snapshot,
    bf_list_snapshots,
    bf_set_snapshot,
)
from pybatfish.question import bfq, load_questions
from pprint import pprint
from pathlib import Path
import pytest

bf_host = "localhost"
working_dir = str(Path(__file__).parent.parent.absolute())
SNAPSHOT_DIR = f"{working_dir}/candidate/"
SNAPSHOT_NAME = "candidate-1"


@pytest.fixture(scope="module")
def init_bf():
    bf_session.host = bf_host

    bf_set_network("nova_candidate")
    snapshots = bf_list_snapshots()
    pprint(snapshots)
    bf_init_snapshot(SNAPSHOT_DIR, name=SNAPSHOT_NAME, overwrite=True)

    bf_set_snapshot(SNAPSHOT_NAME)

    load_questions()

    print(bfq.initIssues().answer())
    print(bfq.nodeProperties(properties="Configuration_Format").answer().frame())


def test_loaded_hosts(init_bf):
    """ MAKE SURE ALL THE CONFIGS WERE LOADED """
    # gather the number of files that have the -confg suffix
    num_configs = len(list(Path(SNAPSHOT_DIR).glob("**/*-confg")))
    loaded_configs_df = bfq.fileParseStatus().answer().frame()
    # pytest will output this when the test is failed
    print(loaded_configs_df)
    # filter the frame for only configs marked as passed
    passed_df = loaded_configs_df[loaded_configs_df.Status == "PASSED"]
    assert passed_df.shape[0] == num_configs