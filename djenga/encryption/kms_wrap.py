"""
Encrypts secrets using kms key wrapping.

Usage:
  kms_wrap [--region=<region_name>] [--profile=<profile name>] --key <key_alias_or_id>

Options:
  -r --region=<region_name>    AWS Region Name
  -p --profile=<profile_name>  the name of the profile to use to connect to aws
  -k --key=<key_alias_or_id>   the alias or id of the kms key to use
"""
from argparse import ArgumentParser
import os
import sys
from djenga.encryption.kms_wrapped import encrypt


def get_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-r', '--region',
        dest='region',
        metavar='region_name',
        help='aws region name, e.g., us-east-2',
        default=None,
    )
    parser.add_argument(
        '-p', '--profile',
        dest='profile',
        metavar='profile_name',
        help='the name of the profile to use when connecting to aws',
        default=None,
    )
    parser.add_argument(
        '-k', '--key',
        dest='key',
        metavar='<id or alias>',
        help='the name of the key to use for encryption',
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    # do not print prompt if input is being piped
    if sys.stdin.isatty():
        print('Enter plaintext: ', end='', file=sys.stderr),
        sys.stderr.flush()
    stdin = os.fdopen(sys.stdin.fileno(), 'rb', 0)
    plain_text = stdin.readline()
    plain_text = plain_text.decode('utf-8').rstrip()
    value = encrypt(
        plain_text,
        alias=args.key,
        profile=args.profile,
        region=args.region)
    print(f'{value}')


if __name__ == "__main__":
    main()
