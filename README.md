[@kozRandBot](https://t.me/kozRandBot)
======================================

[![CI Build](https://github.com/kozalosev/kozRandBot/actions/workflows/ci-build.yml/badge.svg)](https://github.com/kozalosev/kozRandBot/actions/workflows/ci-build.yml)

A Telegram bot that can help you with:

- getting random numbers;
- choosing one item from a list;
- making decisions;
- password generation.

The bot supports both ways of communication with Telegram: *polling* (intended for debugging) and *web hooks* (for
production use).


Requirements
------------

To run the bot on your server, you need to have [Docker](https://docs.docker.com/install/#supported-platforms),
[Docker Compose](https://docs.docker.com/compose/install/) and [nginx](https://nginx.org/en/linux_packages.html)
installed there.

It's possible to start the bot without them, but this is not recommended for two reasons:

1. Your system must have *Python 3.7* to be installed (Ubuntu 18.04, for example, is still supplied with Python 3.6.6).
2. You may use another front-end web server (not *nginx*) or process requests by the application's built-in server
itself, but it will require you to write configuration files by yourself or even manually edit some lines in the code.
See [this note](https://github.com/kozalosev/textUtilsBot#common-notes) for more information.


How to run the bot
------------------

**First**, create a configuration file for nginx (`/etc/nginx/sites-available/kozRandBot`):

```
server {
    # Telegram supports ports 443, 80, 88 and 8443.
    listen 8443 ssl;
    server_name bots.example.org;

    # You may want to override the global logging settings.
    #access_log /dev/null;
    #error_log /home/username/logs/nginx/kozRandBot.err.log;

    location = /kozRandBot/metrics {
        proxy_pass http://127.0.0.1:8001;
    }

    # Ensure the paths are consistent with the NAME and UNIX_SOCKET constants from 'app/data/config.py'.
    location /kozRandBot/ {
        proxy_pass http://127.0.0.1:8011;
        # or for Unix domain socket:
        #proxy_pass http://unix:/tmp/kozRandBot.sock;
    }
}
```

Ensure, you have SSL certificates configured either inside the file above, or better in the global configuration file
(`/etc/nginx/conf.d/server.conf`, for example) to use one certificate for all bots and websites. The latter option is
especially handy if your server is working through Cloudflare or a similar HTTP proxy service. Anyway, you need the
following lines:

```
ssl_certificate /your/path/to/certificate.pem;
ssl_certificate_key /your/path/to/private.key;
```

**Then** execute the following commands:
  
```bash
# clone the repository
git clone https://github.com/kozalosev/kozRandBot

# at first run, the script copies an exemplary configuration file
./start.sh

# modify the config
vim app/data/config.py

# run the application inside a Docker container
./start.sh
```


Testing
-------

Note that testing facilities are not included in the Docker image. Therefore, to run the tests, you need *Python 3.7*
and to install all dependencies from the `requirements.txt` and `requirements-dev.txt` files.

After that, run the following command on Linux:

```bash
PYTHONPATH=app pytest
```

Or one of these commands on Windows:
* CMD:
    ```cmd
    set PYTHONPATH=app && pytest
    ```
* PowerShell:
    ```powershell
    $env:PYTHONPATH='app'; pytest
    ```
