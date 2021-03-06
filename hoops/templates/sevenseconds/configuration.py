'''
Sevenseconds configuration for the account
'''

import pystache


TEMPLATE = '''
# Minimal Configuration YAML file for AWS Account Configurator
# see https://github.com/zalando-stups/sevenseconds
global:
  alias: "{account_name}"
  # regions to configure
  regions:
    - eu-central-1
    - eu-west-1
  # hosted zone for each AWS account
  domain: "{account_name}.example.org"
  # base Taupage AMI to search for
  base_ami:
    name: "Taupage-AMI-*"
    is_public: false
    # account_id of the AMI creator
    onwer_id: 123456789123
  # SSH bastion/jump host
  bastion:
    # uncomment the following line to terminate and redeploy "odd"
    # re_deploy: true

    # this "ami_config" section contains the Taupage user data YAML
    # see http://docs.stups.io/en/latest/components/taupage.html
    ami_config:
      application_id: odd
      application_version: "0.1"
      runtime: Docker
      source: stups/odd:latest
      logentries_account_key: 123-123-123-123
      ports:
        # use default SSH port for Docker container
        22: 22
      environment:
        ALLOWED_REMOTE_NETWORKS: "172.31.0.0/16"
        # configure your even URL here
        GRANTING_SERVICE_URL: "https://even.stups.example.org"
        # configure your public even SSH key here
        GRANTING_SERVICE_SSH_KEY: "ssh-rsa AAAAB3Nza123123mysshpublickey123456789"
      root: true
      # use non-default SSH port for OpenSSH on host
      ssh_ports: [2222]
      hostname: "odd-{account_name}"

accounts:
  default:
'''


def gather_user_variables(variables, region):
    # maximal 32 characters because of the loadbalancer-name
    prompt(variables, 'application_id', 'Application ID', default='hello-world',
           value_proc=check_value(18, '^[a-zA-Z][-a-zA-Z0-9]*$'))
    prompt(variables, 'instance_type', 'EC2 instance type', default='cache.t2.small')

    sg_name = 'redis-{}'.format(variables['application_id'])

    rules_missing = check_security_group(sg_name, [('tcp', 6379)], region, allow_from_self=True)
    if ('tcp', 6379) in rules_missing:
        warning('Security group {} does not allow tcp/6379 access, you will not be able to access your redis'.format(
            sg_name))

    return variables


def generate_definition(variables):
    definition_yaml = pystache.render(TEMPLATE, variables)
    return definition_yaml
