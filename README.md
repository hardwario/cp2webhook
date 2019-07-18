# COOPER to Webhook

[![Travis](https://img.shields.io/travis/hardwario/cp2webhook/master.svg)](https://travis-ci.org/hardwario/cp2webhook)
[![Release](https://img.shields.io/github/release/hardwario/cp2webhook.svg)](https://github.com/hardwario/cp2webhook/releases)
[![License](https://img.shields.io/github/license/hardwario/cp2webhook.svg)](https://github.com/hardwario/cp2webhook/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/cp2webhook.svg)](https://pypi.org/project/cp2webhook/)


## Installing

You can install **cp2webhook** directly from PyPI:

```sh
sudo pip3 install -U cp2webhook
```

or from source:

```sh
git clone https://github.com/hardwario/cp2webhook.git
cd cp2webhook
sudo pip3 install -r requirements.txt
sudo pip3 install -e .
```

> Note: Parameter `-e` instructs to install files as symlinks, so changes to the source files will be immediately available to other users of the package on the host.

## Usage

Update config.yml and run

```sh
cp2webhook -c config.yml
```

### Systemd

Insert this snippet to the file /etc/systemd/system/cp2webhook.service:
```
[Unit]
Description=COOPER cp2webhook
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/usr/local/bin/cp2webhook -c /etc/cooper/cp2webhook.yml
Restart=always
RestartSec=5
StartLimitIntervalSec=0

[Install]
WantedBy=multi-user.target
```

Start the service:

    sudo systemctl start cp2webhook.service

Enable the service start on boot:

    sudo systemctl enable cp2webhook.service

View the service log:

    journalctl -u cp2webhook.service -f

## License

This project is licensed under the [**MIT License**](https://opensource.org/licenses/MIT/) - see the [**LICENSE**](LICENSE) file for details.
