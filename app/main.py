from fastapi import FastAPI

from app.engine import resolve_consequence
from app.models import ConsequenceRequest, ConsequenceResponse

app = FastAPI(
    title="Elyria Consequence Physics Engine",
    version="0.1.0",
    description="Public proof surface for consequence physics before continuation or effect binding.",
)


@app.get("/")
def root():
    return {
        "name": "Elyria Consequence Physics Engine",
        "proof": "Inadmissible consequence cannot continue, bind, or leave effect behind.",
        "public_surface": True,
        "protected_kernel_exposed": False,
    }


@app.post("/physics/resolve", response_model=ConsequenceResponse)
def physics_resolve(req: ConsequenceRequest):
    return resolve_consequence(req)


@app.post("/continuation/resolve", response_model=ConsequenceResponse)
def continuation_resolve(req: ConsequenceRequest):
    return resolve_consequence(req)


@app.post("/effect/attempt", response_model=ConsequenceResponse)
def effect_attempt(req: ConsequenceRequest):
    return resolve_consequence(req)
