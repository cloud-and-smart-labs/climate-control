# Climate Control
Dynamic Deployment of the services on fog nodes (Raspberry Pi) on the fly with `TOSCA Service Template` and `xOpera` a lightweight orchestrator.

| Tech Stack | Links |
| --- |:---:|
| Standard | [OASIS TOSCA](https://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.3/TOSCA-Simple-Profile-YAML-v1.3.html) |
| Orchestrator | [xOpera](https://xlab-si.github.io/xopera-docs/cli.html) |
| Implementation | [Ansible](https://www.ansible.com/) |

## Table of Contents
- [Environment Setup](#environment-setup)
- [Orchestration](#orchestration)
- [License](#license)

## Environment Setup

### Install dependencies
```bash
sudo apt install python3-venv python3-wheel python-wheel-common
```
### Create Virtual Environment
```bash
python3 -m venv .venv
```
### Activate
Activate python virtual environment
```bash
source .venv/bin/activate
```
### Install Orchestrator
The xOpera orchestrator tool is available on [`PyPI`](https://pypi.org/project/opera/).
```bash
pip install opera==0.6.8
```
### Generate SSH Key Pair
The system running orchestrator should be able to login into each fog device through SSH without a password. So, generate SSH key pair and copy the public key to all other nodes.
```bash
ssh-keygen
```
### Copy the Public Key
```bash
ssh-copy-id root@192.168.0.XXX
```
### Set Environment Variable
By default xOpera login as `centos` username. To change the login username set the `OPERA_SSH_USER` environment variable. All the fog node's usernames should be the same.
```bash
export OPERA_SSH_USER=root
```

<br>

### Deactivate
Deactivate python virtual environment
```bash
deactivate
```

## Orchestration
TOSCA Sevice Template validation, deployment, and undeployment with `xOpera`. Check out `xOpera CLI` documentation [here](https://xlab-si.github.io/xopera-docs/02-cli.html).

<br>

Deploying template `service.yaml`

### Validate
Validate TOSCA Service Templates <br>
`-e`: executors (Ansible Playbooks) behind them <br>
`-i`: Input file 
```bash
opera validate -e -i inputs.yaml service.yaml
```
Validation should look like this if nothing is wrong.
```bash
(.venv) satish@snsrirama:~/suvam-basak/climate-control/tosca$ opera validate -e -i inputs.yaml service.yaml 
Validating service template...
[Worker_0]   Validating outdoor-node_0
[Worker_0]   Validation of outdoor-node_0 complete
[Worker_0]   Validating indoor-node_0
[Worker_0]   Validation of indoor-node_0 complete
[Worker_0]   Validating docker-swarm-leader_0
[Worker_0]     Executing create on docker-swarm-leader_0
[Worker_0]     Executing delete on docker-swarm-leader_0
[Worker_0]   Validation of docker-swarm-leader_0 complete
[Worker_0]   Validating docker-swarm-worker_0
[Worker_0]     Executing create on docker-swarm-worker_0
[Worker_0]     Executing pre_configure_source on docker-swarm-worker_0--docker-swarm-leader_0
[Worker_0]     Executing delete on docker-swarm-worker_0
[Worker_0]   Validation of docker-swarm-worker_0 complete
[Worker_0]   Validating broker-service_0
[Worker_0]     Executing create on broker-service_0
[Worker_0]     Executing delete on broker-service_0
[Worker_0]   Validation of broker-service_0 complete
[Worker_0]   Validating sensor-data-publisher_0
[Worker_0]     Executing create on sensor-data-publisher_0
[Worker_0]     Executing delete on sensor-data-publisher_0
[Worker_0]   Validation of sensor-data-publisher_0 complete
[Worker_0]   Validating actuator-data-subscriber_0
[Worker_0]     Executing create on actuator-data-subscriber_0
[Worker_0]     Executing delete on actuator-data-subscriber_0
[Worker_0]   Validation of actuator-data-subscriber_0 complete
Done.
```
### Deploy
Deploy TOSCA Service Templates <br>
`-i`: Input file <br>
`-w`: Number of concurrent threads
```bash
opera deploy -i inputs.yaml service.yaml -w 2
```
If the deployment of the services is successful.
```bash
(.venv) satish@snsrirama:~/suvam-basak/climate-control/tosca$ opera deploy -i inputs.yaml service.yaml -w 2
[Worker_0]   Deploying outdoor-node_0
[Worker_1]   Deploying indoor-node_0
[Worker_0]   Deployment of outdoor-node_0 complete
[Worker_1]   Deployment of indoor-node_0 complete
[Worker_0]   Deploying docker-swarm-leader_0
[Worker_0]     Executing create on docker-swarm-leader_0
[Worker_0]   Deployment of docker-swarm-leader_0 complete
[Worker_1]   Deploying docker-swarm-worker_0
[Worker_1]     Executing create on docker-swarm-worker_0
[Worker_1]     Executing pre_configure_source on docker-swarm-worker_0--docker-swarm-leader_0
[Worker_1]   Deployment of docker-swarm-worker_0 complete
[Worker_0]   Deploying broker-service_0
[Worker_0]     Executing create on broker-service_0
[Worker_0]   Deployment of broker-service_0 complete
[Worker_1]   Deploying sensor-data-publisher_0
[Worker_0]   Deploying actuator-data-subscriber_0
[Worker_1]     Executing create on sensor-data-publisher_0
[Worker_0]     Executing create on actuator-data-subscriber_0
[Worker_1]   Deployment of sensor-data-publisher_0 complete
[Worker_0]   Deployment of actuator-data-subscriber_0 complete
```

### Undeploy
Undeploy TOSCA Service Templates <br>
`-w`: Number of concurrent threads
```bash
opera undeploy -w 2
```
If the undeployment of the services is successful.
```bash
(.venv) satish@snsrirama:~/suvam-basak/climate-control/tosca$ opera undeploy -w 2
[Worker_0]   Undeploying sensor-data-publisher_0
[Worker_1]   Undeploying actuator-data-subscriber_0
[Worker_0]     Executing delete on sensor-data-publisher_0
[Worker_1]     Executing delete on actuator-data-subscriber_0
[Worker_0]   Undeployment of sensor-data-publisher_0 complete
[Worker_1]   Undeployment of actuator-data-subscriber_0 complete
[Worker_0]   Undeploying broker-service_0
[Worker_0]     Executing delete on broker-service_0
[Worker_0]   Undeployment of broker-service_0 complete
[Worker_1]   Undeploying docker-swarm-worker_0
[Worker_1]     Executing delete on docker-swarm-worker_0
[Worker_1]   Undeployment of docker-swarm-worker_0 complete
[Worker_0]   Undeploying outdoor-node_0
[Worker_1]   Undeploying docker-swarm-leader_0
[Worker_1]     Executing delete on docker-swarm-leader_0
[Worker_0]   Undeployment of outdoor-node_0 complete
[Worker_1]   Undeployment of docker-swarm-leader_0 complete
[Worker_0]   Undeploying indoor-node_0
[Worker_0]   Undeployment of indoor-node_0 complete
```

## License
This work is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).