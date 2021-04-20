"""Console script"""
import sys
from wiki_challenge.Engine import Engine


def main(args=None):
    pipeline = Engine()
    pipeline.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
