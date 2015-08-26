# Introduction
Project is in Proof-of-Concept state! If the concept is proven, the requirements and roadmap will be specified.

`hoops` is a tool which automatically (with minimal number of manual steps) creates the basic setup (based on minimal number
of required components) of Zalando Stups on an Amazon AWS account. It is targeted for users who want to benefit from
docker-based PaaS, but without enterprise security requirements (auditing, saml). It should deliver as many features
of STUPS as possible (like private docker registry, OAuth service) while staying super easy to configure, setup and
manage.

## Targets
 - use Sevenseconds to setup AWS account
 - setup minimal number of services in order to be able to run an ASG with docker "hello world" application

## PoC assumptions
 - no SAML
 - no OAuth or mocked OAuth if required
 - use official docker registry instead of pier one
 - setup "stups" services (like even) on the same account as applications (no sub-accounts)
 - use easiest possible implementations (for example, instead of even: nginx with static files for SSH keys)
 - use configuration management tool (like ansible) to perform actions on EC2 instances

## Stups services:
 - seven seconds: YES
 - even: yes, but without OAuth
 - piu: yes
 - odd: yes
 - senza: yes
 - taupage: yes
 - pier one: maybe later. would be great to have own docker registry with s3 backend, but let's try to avoid OAuth first
 - fullstop.: nice to have (in the future)
 - mint, berry: prefferably NO (only if required)
 - mai: NOT PRESENT
 - kio: NOT PRESENT
 - zign: NOT PRESENT
 - yourturn: NOT PRESENT
 - twintip: ???
 - essentials: ???


## Ideas for later stage:
 - setup easy OAuth service (automatical setup required, with easy modular backend, like text files)
 - setup SAML service (see above)
 - pier one registry (independent from docker.com registry)
 - incident reporting with Fullstop.
 - modular extensions (like newrelic, scalyr, logentries, appdynamics, papertrail, loggly, etc.)
