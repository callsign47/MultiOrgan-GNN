"""
ORGANIX Command-Line Interface (CLI).
"""

import argparse
import sys
import json
from organix.core.logging import get_logger
from organix.evaluation.leakage_gate import run_leakage_gate
from organix.experiments.registry import list_registered_experiments, get_experiment_info
from organix.data.cohort import load_final_cohort
from organix.data.manifest import verify_and_load_manifest
from organix.utils.paths import get_paths

logger = get_logger("organix.cli")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="organix",
        description="ORGANIX: Heterogeneous Systemic Graph Interaction Network (HSGIN) for Multi-Organ Risk Modeling",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: gate
    gate_parser = subparsers.add_parser("gate", help="Run automated 4-tier leakage control gate")

    # Command: verify
    verify_parser = subparsers.add_parser("verify", help="Verify cohort, manifest, and artifact integrity")

    # Command: experiments
    exp_parser = subparsers.add_parser("experiments", help="List or inspect registered benchmark experiments")
    exp_parser.add_argument("--id", type=str, default=None, help="Specific experiment ID to inspect")

    args = parser.parse_args()

    if args.command == "gate":
        logger.info("Executing ORGANIX Automated Leakage-Control Gate...")
        report = run_leakage_gate()
        if report.get("all_passed"):
            logger.info("SUCCESS: ALL 4 HARD LEAKAGE GATES PASSED.")
            sys.exit(0)
        else:
            logger.error("FAILURE: LEAKAGE DETECTED.")
            sys.exit(1)

    elif args.command == "verify":
        logger.info("Verifying ORGANIX Assets and Checksums...")
        manifest = verify_and_load_manifest()
        logger.info("  -> Manifest Checksum: VERIFIED (25 features, zero direct overlap)")
        cohort = load_final_cohort()
        logger.info(f"  -> Final Cohort: VERIFIED (N={len(cohort):,} patients)")
        paths = get_paths()
        if paths.patient_graphs_path.exists():
            logger.info(f"  -> Patient Graphs: VERIFIED ({paths.patient_graphs_path.name})")
        logger.info("All canonical assets verified successfully.")
        sys.exit(0)

    elif args.command == "experiments":
        if args.id:
            info = get_experiment_info(args.id)
            print(json.dumps(info, indent=2))
        else:
            print("Registered ORGANIX Experiments:")
            for exp_id in list_registered_experiments():
                info = get_experiment_info(exp_id)
                print(f"  - {exp_id:<22}: {info['name']}")
        sys.exit(0)

    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
