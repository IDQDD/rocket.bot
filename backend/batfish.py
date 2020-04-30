import pandas as pd
from pybatfish.client.commands import *
from pybatfish.datamodel import *
from pybatfish.datamodel.answer import *
from pybatfish.datamodel.flow import *
from pybatfish.question import *
from pybatfish.question import bfq

from ipaddress import ip_address

class LibBatfish(object):
    net2acl = {
        "10.1.10": {"in": "VL10_IN", "out": "VL10_OUT"},
        "10.1.20": {"out": "VL20_OUT"},
        "10.1.30": {"in": "VL10_IN", "out": "VL30_OUT"}
    }

    def init_new_snapshot(network, snapshot, snapshot_dir, host="localhost"):
        bf_session.host = host
        bf_set_network(network)
        bf_init_snapshot(snapshot_dir, snapshot, overwrite=True)
        load_questions()

    def init_existed_snapshot(network, snapshot):
        bf_set_network(network)
        bf_set_snapshot(snapshot)
        load_questions()

    def testACL(data):
        hc = HeaderConstraints(**data)
        filters = LibBatfish.getAclNames(data["srcIps"], data["dstIps"])
        if (filters):
            filters = ",".join(filters)
            res = bfq.testFilters(headers=hc,filters=filters,nodes="/n7k/").answer().frame()
            return res.to_markdown()
        else:
            return ":white_check_mark: There is no acl filters applied to the flow"

    def getAclNames(src, dst):
        filters = []

        src = ".".join(src.split(".")[:3])
        dst = ".".join(dst.split(".")[:3])

        if (x := LibBatfish.net2acl.get(src)): 
            if (y := x.get("in")): filters.append(y)
        if (x := LibBatfish.net2acl.get(dst)): 
            if (y := x.get("out")): filters.append(y)

        return filters
