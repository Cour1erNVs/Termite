import argparse
from termite.generator import generate_variants
from termite.analyzer import analyze

def banner():
    print(r"""
████████╗███████╗██████╗ ███╗   ███╗██╗████████╗███████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║╚══██╔══╝██╔════╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║   █████╗  
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║   ██╔══╝  
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║   ██║   ███████╗
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝   ╚═╝   ╚══════╝
""")


def run():
    parser = argparse.ArgumentParser(prog="Termite")

    subparsers = parser.add_subparsers(dest="command")

    # generate
    gen = subparsers.add_parser("generate")
    gen.add_argument("-i", "--input", required=True)
    gen.add_argument("-n", "--num", type=int, default=3)
    gen.add_argument("--level", type=int, default=1)

    # analyze
    ana = subparsers.add_parser("analyze")
    ana.add_argument("-f", "--file", required=True)
    ana.add_argument("-m", "--meta", required=True)

    args = parser.parse_args()

    if args.command == "generate":
        with open(args.input, "rb") as f:
            data = f.read()

        results = generate_variants(data, args.num, args.level)

        for r in results:
            print(f"[+] Created: {r[0]} | Meta: {r[1]}")

    elif args.command == "analyze":
        analyze(args.file, args.meta)

    else:
        parser.print_help()