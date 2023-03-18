
# auditDownyVibez

auditDownyVibez is a auditing tool designed to validate system configurations against the CIS (Center for Internet Security) Benchmark for Ubuntu 20.04 Server. This tool leverages the power of goss, a YAML-based testing tool, to perform its checks. The main feature of auditDownyVibez is its ability to run through Ansible, allowing a controller server to execute tests on multiple target hosts specified in a playbook. Upon completion, the tool generates an HTML report with a summary of the audit results for each target host.


## Features

- Validate system configurations against the CIS Benchmark for Ubuntu 20.04 LTS.
- Utilizes goss and YAML to perform configuration checks.
- Seamlessly integrates with Ansible to run tests on multiple target hosts.
- Automatically generate an HTML report with a summary of the audit results for each target host.


## Prerequisites

- Ansible installed on the controller server.
- Python 3.x installed on the target systems.
- The [goss](https://github.com/goss-org/goss) binary installed on the target systems.
## Installation

1. Clone the auditDownyVibez repository on the controller server:

```bash
  git clone https://github.com/grenishtri/auditDownyVibez.git
```
2. Change to the auditDownyVibez directory:
```bash
  cd auditDownyVibez
```

## Usage
The complete_commands.sh script, located in the play-books directory, will run the necessary Ansible playbooks in sequence. Before executing the script, ensure that your Ansible inventory is properly configured with the target hosts.

1. Change to the play-books directory:
```bash
  cd play-books
```

2. Execute the complete_commands.sh script:
```bash
  ./complete_commands.sh
```
The script will prompt you to confirm each step before proceeding.

<img width="665" alt="image" src="https://user-images.githubusercontent.com/90232209/226115783-f02ae169-f3f0-472a-a147-c7e056213154.png">


3. After the prerequisites are installed and the tests are executed, an HTML report will be generated for each target host, providing a summary of the audit results.
<img width="731" alt="image" src="https://user-images.githubusercontent.com/90232209/226116146-26ff3e54-5384-4f11-8a5f-5048b7eaaddc.png">

## Ansible

To use the Ansible playbook with this audit tool, you need to update the `/etc/ansible/hosts` file on the Ansible controller machine with the correct IP addresses of the target hosts. Replace the example IP addresses with the public IP addresses of your hosts:

```bash
[ubuntu_hosts]
host1 ansible_ssh_host=1.2.3.4 ##change this to public ip address of hosts
host2 ansible_ssh_host=2.3.4.5 ##change this to public ip address of hosts
```


Alternatively, you can specify the IP addresses in a custom inventory file and provide its path when running the playbook using the `-i` option:
```bash
ansible-playbook -i path/to/your/inventory/file playbook.yml
```
<img width="634" alt="Screenshot 2023-03-17 145105" src="https://user-images.githubusercontent.com/90232209/226117210-95e784f1-7c49-4b2a-ab00-33e60b992365.png">


Make sure that Ansible is installed on the controller machine for the playbook to work properly. You can follow the [official Ansible installation guide](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) for detailed instructions on how to install Ansible.


## License

auditDownyVibez is released under the MIT License.
[MIT](https://choosealicense.com/licenses/mit/)
