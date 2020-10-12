# ejabberd-pleroma-auth

This is a modified version of Ejabberd external auth script for [Pleroma](https://pleroma.social/). Original script is [here](https://github.com/processone/ejabberd/blob/master/test/ejabberd_SUITE_data/extauth.py).

This script implements readonly operations: auth and issuer. You can only verify users' credentials and their presence.  

Script assumes your Pleroma instance is working on port `4000` and responds requests to `127.0.0.1`. If you have different setup, please change related constants on very top of file.


## How to use it?

```bash
cp pleroma_ejabberd_auth.py /etc/ejabberd/pleroma_ejabberd_auth.py
chown ejabberd /etc/ejabberd/pleroma_ejabberd_auth.py
chmod 700 /etc/ejabberd/pleroma_ejabberd_auth.py
```

Set external auth params in ejabberd.yaml file:

```
auth_method: [external]
extauth_program: "python3 /etc/ejabberd/pleroma_ejabberd_auth.py"
extauth_instances: 3
auth_use_cache: false
```

Restart / reload your ejabberd service.

## Problem?
Check ejabberd logs.

Script sends its own logs to file `/var/log/ejabberd/pleroma_auth.log` which is supposed to be owned by user `ejabberd`.
