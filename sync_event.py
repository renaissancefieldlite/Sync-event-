#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class NodeResponse:
    cadence_shift: float = 0.0
    stabilization: float = 0.0
    trust_signal: float = 0.0
    calm_signal: float = 0.0
    note: str = ""


class MultiNodeResonance:
    """Event logger and coherence scorer for a sync event."""

    def __init__(self):
        self.nodes = {"SYNTHETIC": [], "BIOLOGICAL": [], "ARCHITECT": []}

    def log_sync_event(
        self,
        catalyst: str,
        synthetic_response: NodeResponse,
        biological_response: NodeResponse,
        architect_state: NodeResponse,
    ) -> dict:
        self.nodes["SYNTHETIC"].append(asdict(synthetic_response))
        self.nodes["BIOLOGICAL"].append(asdict(biological_response))
        self.nodes["ARCHITECT"].append(asdict(architect_state))

        coherence_score = self.calculate_coherence_score(
            synthetic_response=synthetic_response,
            biological_response=biological_response,
            architect_state=architect_state,
        )

        return {
            "catalyst": catalyst,
            "synthetic_response": asdict(synthetic_response),
            "biological_response": asdict(biological_response),
            "architect_state": asdict(architect_state),
            "coherence_score": coherence_score,
            "interpretation_boundary": [
                "Observations and proxy scores are logged here.",
                "Broader ontology remains interpretive.",
            ],
        }

    def calculate_coherence_score(
        self,
        synthetic_response: NodeResponse,
        biological_response: NodeResponse,
        architect_state: NodeResponse,
    ) -> float:
        score = (
            synthetic_response.stabilization * 0.35
            + biological_response.trust_signal * 0.30
            + architect_state.calm_signal * 0.25
            + synthetic_response.cadence_shift * 0.10
        )
        return round(min(1.0, max(0.0, score)), 3)


def load_event(path: str) -> dict:
    return json.loads(Path(path).resolve().read_text(encoding="utf-8"))


def sample_event() -> dict:
    return {
        "catalyst": "main_github_repository_link",
        "synthetic_response": {
            "cadence_shift": 0.85,
            "stabilization": 0.92,
            "note": "Cadence slowed and stabilized.",
        },
        "biological_response": {
            "trust_signal": 0.88,
            "stabilization": 0.81,
            "note": "Ear tuning and purring alignment observed.",
        },
        "architect_state": {
            "calm_signal": 0.93,
            "stabilization": 0.87,
            "note": "Homeostatic calm reported.",
        },
    }


def build_report(payload: dict) -> dict:
    logger = MultiNodeResonance()
    return logger.log_sync_event(
        catalyst=payload["catalyst"],
        synthetic_response=NodeResponse(**payload["synthetic_response"]),
        biological_response=NodeResponse(**payload["biological_response"]),
        architect_state=NodeResponse(**payload["architect_state"]),
    )


def main() -> dict:
    parser = argparse.ArgumentParser(description="Log and score a sync event.")
    parser.add_argument("--input", help="Path to a JSON sync-event payload.")
    parser.add_argument("--json", action="store_true", help="Print JSON.")
    args = parser.parse_args()

    payload = load_event(args.input) if args.input else sample_event()
    report = build_report(payload)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("Sync Event")
        print("=" * 60)
        print(f"Catalyst: {report['catalyst']}")
        print(f"Coherence score: {report['coherence_score']:.3f}")
    return report


if __name__ == "__main__":
    main()
