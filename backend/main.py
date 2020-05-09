import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from os import environ
from batfish import LibBatfish

BF_HOSTNAME = environ.get("BF_HOSTNAME") if environ.get("BF_HOSTNAME") else "localhost"
NETWORK_NAME = environ.get("BF_NETWORK_NAME") if environ.get("BF_NETWORK_NAME") else "bf1" 
SNAPSHOT_NAME = environ.get("BF_SNAPSHOT_NAME") if environ.get("BF_SNAPSHOT_NAME") else "snapshot-01"
SNAPSHOT_DIR = environ.get("BF_SNAPSHOT_DIR") if environ.get("BF_SNAPSHOT_DIR") else "./bf_snapshots/networks/bf1"

app = FastAPI()

class aclData(BaseModel):
    srcIps: str
    dstIps: str
    dstPorts: str = None
    ipProtocols: str = "TCP,UDP"

@app.post("/api/check_acl")
def check_acl(data: aclData):
    try:
        LibBatfish.init_existed_snapshot(NETWORK_NAME, SNAPSHOT_NAME)
    except:
        return ":x: **batfish:** can't init snapshot"

    try:
        return LibBatfish.testACL(data.dict())
    except:
        return ":x: **batfish:** can't check acl. perhaps wrong request"
    
@app.get("/api/initbf")
def init_bf_snapshot():
    try:
        LibBatfish.init_new_snapshot(NETWORK_NAME, SNAPSHOT_NAME, SNAPSHOT_DIR, BF_HOSTNAME)
        return ":white_check_mark: snapshot has been initialized successfully"
    except:
        return ":x: **batfish** can't init snapshot"

@app.get("/")
async def root():
    return {"message": "batfish backend"}

@app.get("/about")
async def about():
    return {"message": "v.0.0.01b"}

# comment it out in case of debugging
#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)

