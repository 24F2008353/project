from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import json
import math
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestBody(BaseModel):
    regions: list[str]
    threshold_ms: float

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/api/latency")
def analyze_latency(req: RequestBody):
    return analyze(req)

@app.get("/api/latency")
def latency_get():
    return {"status": "ok"}
    
@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str):
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
    )

DATA_FILE = Path(__file__).parent.parent / "q-vercel-latency.json"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    DATA = json.load(f)

def percentile_95(values):
    values = sorted(values)
    k = math.ceil(0.95 * len(values)) - 1
    return values[max(0, min(k, len(values)-1))]
    
@app.post("/")
def analyze(req: RequestBody):
    result = []

for region in req.regions:
    ...
    result.append({
        "region": region,
        "avg_latency": round(sum(latencies) / len(latencies), 2),
        "p95_latency": round(percentile_95(latencies), 2),
        "avg_uptime": round(sum(uptimes) / len(uptimes), 3),
        "breaches": sum(
            1 for r in rows
            if r["latency_ms"] > req.threshold_ms
        )
    })

return result
