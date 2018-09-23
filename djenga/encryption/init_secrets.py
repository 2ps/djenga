"""
Encrypts secrets using kms key wrapping.

Usage:
  init_secrets [--region=<region_name>] [--profile=<profile name>] --key <key_alias_or_id> --env env_name

Options:
  -r --region=<region_name>    AWS Region Name
  -p --profile=<profile_name>  the name of the profile to use to connect to aws
  -k --key=<key_alias_or_id>   the alias or id of the kms key to use
  -e --env=<env name>          the name of the environment (i.e., if you want to use multiple encryption keys)
"""
from argparse import ArgumentParser
from base64 import b64encode
import os
import sys
from djenga.encryption.helpers import _prefix_alias
from djenga.encryption.helpers import _get_client
from djenga.utils.print_utils import notice
from djenga.utils.print_utils import notice_end
from gnupg import GPG
from git import Repo


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
    parser.add_argument(
        '-e', '--env',
        dest='env',
        metavar='<name>',
        help='the name of the environment this key will be used for',
    )
    return parser


def add_local_key(gpg, dir_name, data_key, fingerprint):
    notice('generating local key')
    filename = os.path.join(dir_name, fingerprint)
    gpg.encrypt(data_key, fingerprint, armor=True, output=filename)
    notice_end()
    return filename


def generate_server_key(args, dir_name):
    client = _get_client(args.region, args.profile)
    alias = _prefix_alias(args.key)
    notice('generating data key from kms')
    response = client.generate_data_key(
        KeyId=alias,
        KeySpec='AES_256')
    notice_end()
    notice('generating encrypted server key')
    server_key = b64encode(response['CiphertextBlob']).decode('utf-8')
    filename = os.path.join(dir_name, 'server.txt')
    with open(filename, 'w') as f:
        f.write(server_key)
        f.write('\n')
    notice_end()
    return response, filename


def git_commit(*filenames, message: str):
    notice('commit to git')
    repo = Repo('.')
    repo.index.add(filenames)
    repo.index.commit(message=message)
    notice_end()


def validate_gpg():
    notice('validating gpg setup')
    home = os.environ.get('HOME')
    gpg_home = os.path.join(home, '.gnupg')
    gpg = GPG(homedir=gpg_home)
    secret_keys = gpg.list_keys(secret=True)
    if not secret_keys:
        notice_end('uninitialized')
        print('It looks like you have not created a '
              'gpg private key for yourself.')
        sys.exit(1)
    notice_end()
    return gpg, secret_keys[0]


def initialize_secrets_dir(args):
    notice(f'initializing {args.env}')
    dir_name = f'.secrets/{args.env}'
    if os.path.exists(dir_name):
        notice_end(f'already exists')
        sys.exit(1)
    os.makedirs(dir_name, mode=0o755, exist_ok=True)
    os.chmod(dir_name, mode=0o755)
    notice_end()
    return dir_name


def main():
    parser = get_parser()
    args = parser.parse_args()
    dir_name = initialize_secrets_dir(args)
    gpg, gpg_secret_key = validate_gpg()
    response, filename = generate_server_key(args, dir_name)
    my_filename = add_local_key(
        gpg, dir_name, response['Plaintext'],
        gpg_secret_key['fingerprint'])
    uid = gpg_secret_key['uids'][0]
    message = (f'[secrets]  initialized keys '
               f'for {args.env}\n\ninitialization by {uid}')
    git_commit(filename, my_filename, message=message)


if __name__ == "__main__":
    main()
