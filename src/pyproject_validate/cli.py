import argparse
import sys

from ._version import version
from .handlers import get_handler
from .validators import get_validators


def main():
    parser = argparse.ArgumentParser(prog="pyproject-validate", allow_abbrev=False)
    parser.add_argument("--fix", action="store_true")
    parser.add_argument("--config")
    if sys.version_info[:2] >= (3, 8):
        parser.add_argument("--version", action="version", version=f"%(prog)s {version}")
    args = parser.parse_args()

    handler = get_handler(args.config)
    try:
        data = handler.load()
    except Exception as e:
        print(e)
        sys.exit(1)

    errors_occurred = False
    unfixable_errors = False
    need_fixing = False
    for name, validator in get_validators().items():
        errors = []
        warnings = []
        validator.validate(data, errors, warnings)

        if (errors or warnings) and not args.fix or not validator.fixable:
            print(f"<<< {name} >>>")
            for error in errors:
                print(f"error: {error}")
            for warning in warnings:
                print(f"warning: {warning}")

        if errors:
            errors_occurred = True
            if args.fix and validator.fixable:
                need_fixing = True
                validator.fix(data)
            else:
                unfixable_errors = True
                if validator.exit_early:
                    break

    if need_fixing and not unfixable_errors:
        handler.save(data)
        errors_occurred = False

    sys.exit(int(errors_occurred))
