import os
import sys
from invoke import task


__all__ = [
    'deploy',
    'setup',
    'build',
]


@task
def deploy(ctx):
    """
    Deploys djenga to pypi

    Performs the following steps:
        * bumps the version using `bumpversion`
        * builds the djenga tarball and bdist_wheel
        * pushes the build to pypi
    """
    ctx.run('bumpversion patch')
    build(ctx)
    ctx.run('twine upload dist/*')


@task
def build(ctx):
    ctx.run('rm -rf build dist')
    ctx.run('python setup.py bdist_wheel')
    ctx.run('python setup.py sdist')


def detect_ec2(ctx):
    if os.path.exists('/sys/hypervisor/uuid'):
        result = ctx.run('head -c 3 /sys/hypervisor/uuid')
        return result.stdout.startswith('ec2')
    return False


@task
def setup(ctx):
    """
    Creates a virtual environment to begin working on djenga
    """
    python = None
    codebuild = os.environ.get('CODEBUILD_BUILD_ARN')
    ec2 = detect_ec2(ctx)
    if sys.platform in ('linux', 'darwin'):
        result = ctx.run('which python3.6')
        if result.ok:
            x = '/env' if codebuild else '.'
            python = os.path.join(x, 'bin/python')
            ctx.run(f'python3.6 -m venv {x}')
    elif sys.platform == 'win32':
        if os.path.exists(r'c:\python36\python.exe'):
            name = os.path.basename(os.getcwd())
            home = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
            python = os.path.join(home, 'Envs', name, 'Scripts', 'python.exe')
            if not os.path.exists(python):
                ctx.run(
                    f'powershell.exe mkvirtualenv {name} '
                    f'-python c:/python36/python.exe'
                )

    if python:
        pip = f'{python} -m pip install'
        if codebuild or ec2:
            pip = f'{pip} --cache-dir ./.pip -q'
        ctx.run(f'{pip} -U pip setuptools wheel invoke')
        ctx.run(f'{pip} -r requirements.txt')
    else:
        print('no suitable python version found')
