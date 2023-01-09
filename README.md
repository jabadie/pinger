# Pinger!

Simple Python service built with Docker and Kubernetes to Regularly check and report the status of URLs

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. 

### Prerequisites

Requirements for the software and other tools to build, test and push 
- Command Line Tools for XCode(Or an equivalent method of obtaining Make and Git)
- [Docker](https://www.docker.com/)
- [Python 3](https://www.python.org/downloads/)
- [pip-tools](https://pypi.org/project/pip-tools/)(Optional - For updating the requirements.txt)

### Installing

Once the prerequesites are installed, a Docker image can be built by executing

    make build

## Deployment

The service can be deployed locally with by executing

    make start

The service can be stopped locally with by executing 

    make stop

## Improvements
The Following are TODOs to for the project.

### Required
* Define a VPC in Terraform and apply
* Define and create the EKS Cluster to deploy this in via Terraform.
* Write Kubernetes configuration for the pod and service
* Move service configuration to JSON files, read them locally for development, and read configuration from the DB when not.
* Attach a database and set up schema and migration management.
* Add Monitoring plugins for Datadog and OpsGenie and configure them.
* Add tests!  At present, there are no unit tests. 
* Add authentication, preferably via SSO of some kind.
* Add managment UI app to replace the JSON configuration file.
* Audit logging for configuration changes and triggers.
* Add state monitor state with the state saved in the DB or a shared cache.
* Add leader election so backup instances can be deployed for redundancy.

### Improvements and features
* Add sharding to make horizontal scaling possible
* Add a Datadog sidecar for container metrics
* Add out-of-band monitors with webhooks to ensure the tests are actually running.  In other words, monitor the monitor.
* Add a CI tool for Terraform so I'm not applying manually and integrate with Github
* Add continuous deployment.
* Add granular roles for monitor and plugin configuration  
* Reduce the size of the container image.  The base image in use at present is a bit fat.  We sould be able to do better.

## Authors

  - **Josh Abadie** - [email](jabadi2@gmail.com)
