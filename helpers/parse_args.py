import argparse

def parse_args():
  parser = argparse.ArgumentParser(
      description="Start stint tracker"
  )

  parser.add_argument(
      "--session-id",
      required=True,
      help="ID of session to create pit stops in"
  )

  parser.add_argument(
      "--drivers",
      nargs="+",
      required=True,
      help="List of driver names"
  )
  
  parser.add_argument(
    "--practice",
    action="store_true",
    help="Mark session as practice"
)

  return parser.parse_args()