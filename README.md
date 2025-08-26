# AD-Attack-Toolkit

All-in-one, modular toolkit to automate **Active Directory** workflows:
- Enumeration (LDAP/DNS/SMB)
- Exploitation, Privilege Escalation, Persistence, OPSEC

> **Use only in authorized environments.**

## Features
- Menu-driven CLI with safety confirmations
- LDAP enumeration (users, groups, computers) via `ldap3`
- DNS SRV lookups for DC/GC/Kerberos discovery
- SMB share listing (guest/anonymous) using Python `smbprotocol`

## Install
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt