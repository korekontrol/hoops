# Introduction
Project is in Proof-of-Concept state! If the concept is proven, the requirements and roadmap will be specified.

hoops is a tool which automatically (with minimal number of manual steps) creates the basic setup of Zalando Stups
on one Amazon AWS account.

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
 - yourturn: NOT PRESENT
 - kio: NOT PRESENT
 - essentials: ???
 - twintip: ???
 - fullstop.: nice to have (in the future)
 - even: yes, but without OAuth
 - odd: yes
 - mai: NOT PRESENT
 - senza: yes
 - zign: NOT PRESENT
 - seven seconds: YES
 - pier one: maybe later. would be great to have own docker registry with s3 backend, but let's try to avoid OAuth
 - mint, berry: prefferably NO (only if required)



## Ideas for later stage:
 - setup easy OAuth service (automatical setup required, with easy modular backend, like text files)
 - setup SAML service (see above)
 - pier one registry (independent from docker.com registry)
 - incident reporting with Fullstop.
