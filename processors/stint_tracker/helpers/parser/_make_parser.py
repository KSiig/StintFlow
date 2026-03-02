import argparse

# help-text constants -------------------------------------------------------
PRACTICE_HELP = "Practice mode - requires player to return to garage before tracking"
DRYRUN_HELP = (
    "Run the tracker loop without reading LMU memory. "
    "Heartbeats and cleanup still occur."
)


def _make_parser() -> argparse.ArgumentParser:
    """Build and return an ArgumentParser configured for the stint tracker."""
    parser = argparse.ArgumentParser(
        description="Track stints by monitoring LMU shared memory"
    )

    parser.add_argument(
        "--session-id",
        required=True,
        help="ID of session to create stints in"
    )

    parser.add_argument(
        "--drivers",
        nargs="+",
        required=True,
        help="List of driver names for this session"
    )

    parser.add_argument(
        "--practice",
        action="store_true",
        help=PRACTICE_HELP
    )

    parser.add_argument(
        "--agent-name",
        help=(
            "Optional unique name for this tracker instance. "
            "If omitted a default based on host name will be used."
        )
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=DRYRUN_HELP
    )

    return parser

