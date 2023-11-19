# Telegram Bot for Deploying Code-Server Containers

This repository hosts a Telegram bot designed to deploy Code-Server containers using Ansible. It also includes a Python script to detect new open ports and a sample Ansible inventory and configuration file.

## File Structure

├── README.md # This file   
├── ansible.cfg # Ansible configuration file    
├── code-server.yaml # Ansible playbook for deploying Code-Server   
├── inventory # Ansible inventory file  
├── main.py # Python script to detect new open ports    
└── telebot2easy.py # Telegram bot code

## Contents

- **`ansible.cfg`**: Ansible configuration file.
- **`code-server.yaml`**: Ansible playbook for deploying the Code-Server container.
- **`inventory`**: Ansible inventory file containing hosts information.
- **`main.py`**: Python script to monitor and detect new open ports.
- **`telebot2easy.py`**: Telegram bot script for deploying containers via commands.

## Getting Started

### Prerequisites
- Python 3.x installed.
- Required Python packages: `psutil` and `python-telegram-bot`.

### Setting Up Ansible
- Update `ansible.cfg` and `inventory` files with your environment details.

### Running the Code
- Execute `main.py` to monitor new open ports.
- Start the Telegram bot using `telebot2easy.py`.

### Using the Telegram Bot
- Initiate a conversation with the bot and send commands to deploy containers.

## Notes
- Configure the bot's API token in `telebot2easy.py` before use.
- Adapt the configurations according to your project's needs.
