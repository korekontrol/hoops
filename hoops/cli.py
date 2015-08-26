#!/usr/bin/env python3
import functools
import sys
import importlib
import tempfile
import yaml

from boto.exception import BotoServerError
import click
from clickclick import AliasedGroup, Action
from clickclick.console import print_table
import requests
import boto.vpc
import boto.ec2
import boto.iam
import boto.route53

import hoops
import sevenseconds.cli

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Hoops {}'.format(hoops.__version__))
    sevenseconds.cli.print_version
    ctx.exit()


def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper():
        try:
            func()
        except boto.exception.NoAuthHandlerFound:
            sys.stderr.write('No AWS credentials found.\n')
            sys.stderr.write('or manually configure either ~/.aws/credentials ' +
                             'or AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY.\n')
            sys.exit(1)
    return wrapper


@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.option('-V', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True,
              help='Print the current version number and exit.')
def cli():
    pass


@cli.command()
@click.argument('configuration_file', type=click.File('rb'))
# @region_option
# @click.option('-t', '--template', help='Use a custom template', metavar='TEMPLATE_ID')
# @click.option('-v', '--user-variable', help='Provide user variables for the template',
#              metavar='KEY=VAL', multiple=True, type=KEY_VAL)
@click.pass_context
def init(ctx, configuration_file):
    '''Initialize a new AWS account with Sevenseconds'''

    config = yaml.safe_load(configuration_file)
    region = config.get('region')
    check_credentials(region)

    module = importlib.import_module('hoops.templates.sevenseconds.configuration')
    variables = {}

#    variables = module.gather_user_variables(variables, region)
    with Action('Generating Sevenseconds configuration...'):
        definition_file = tempfile.NamedTemporaryFile()
        try:
            definition = module.generate_definition(variables)
            definition_file.write(definition.encode('utf-8'))
            definition_file.seek(0, 0)
        finally:
            ctx.invoke(sevenseconds.cli.configure, file=definition_file, account_name_pattern='*', saml_user=None, saml_password=None, dry_run=True)
            definition_file.close()



# def parse_args(input, region, version, parameter):
#     paras = {}
#     defaults = {}

#     # process positional parameters first
#     seen_keyword = False
#     for i, param in enumerate(input['SenzaInfo'].get('Parameters', [])):
#         for key, config in param.items():
#             # collect all allowed keys and default values regardless
#             paras[key] = None
#             defaults[key] = config.get('Default', None)
#             if i < len(parameter):
#                 if '=' in parameter[i]:
#                     seen_keyword = True
#                 else:
#                     if seen_keyword:
#                         raise click.UsageError("Positional parameters must not follow keywords.")
#                     paras[key] = parameter[i]

#     if len(paras) < len(parameter):
#         raise click.UsageError('Too many parameters given.')

#     # process keyword parameters separately, if any
#     if seen_keyword:
#         for i in range(len(parameter)):
#             param = parameter[i]
#             if '=' in param:
#                 key, value = param.split('=', 1)  # split only on first =
#                 if key not in paras:
#                     raise click.UsageError('Unrecognized keyword parameter: "{}"'.format(key))
#                 if paras[key] is not None:
#                     raise click.UsageError('Parameter specified multiple times: "{}"'.format(key))
#                 paras[key] = value

#     # finally, make sure every parameter got a value assigned, using defaults if given
#     for key, defval in defaults.items():
#         paras[key] = paras[key] or defval
#         if paras[key] is None:
#             raise click.UsageError('Missing parameter "{}"'.format(key))

#     args = TemplateArguments(region=region, version=version, **paras)
#     return args


# def get_region(region):
#     if not region:
#         config = configparser.ConfigParser()
#         try:
#             config.read(os.path.expanduser('~/.aws/config'))
#             if 'default' in config:
#                 region = config['default']['region']
#         except:
#             pass

#     if not region:
#         raise click.UsageError('Please specify the AWS region on the command line (--region) or in ~/.aws/config')

#     cf = boto.cloudformation.connect_to_region(region)
#     if not cf:
#         raise click.UsageError('Invalid region "{}"'.format(region))
#     return region


def check_credentials(region):
    iam = boto.iam.connect_to_region(region)
    return iam.get_account_alias()


def main():
    handle_exceptions(cli)()


if __name__ == "__main__":
    main()
