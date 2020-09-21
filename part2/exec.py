import argparse

from dump import Dump


parser = argparse.ArgumentParser()
parser.add_argument('dump', help='Dump file path')
args = parser.parse_args()

dump = Dump(args.dump)
dump.make_database()
dump.export_database()
