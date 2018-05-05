# Dash Electrum
The Dash Electrum Lightweight Crypocurrency Desktop Wallet for Fedora Linux

> Please note, this software package is still being tested. Let me know if you
run into any issues please. **DON'T USE THIS FOR SERIOUS MONEY** -issues below.

```
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo dnf install -y https://raw.githubusercontent.com/taw00/electrum-dash-rpm/master/toddpkgs-electrum-dash-repo-1.0-0.1.testing.fc27.taw0.noarch.rpm
sudo dnf list | grep electrum
sudo dnf list --refresh | grep electrum # if it doesn't show up right away
sudo dnf install electrum-dash
```

Then browse your desktop menuing system for Dash Electrum! :)

Primary website for this application is here: <http://electrum.dash.org/>

For feedback or comment: <t0dd@protonmail.com>

## Known issues:

You can send and receive funds, but...

* Segfaults on QR Code click on send
* ```"sni-qt/14318" WARN  20:57:02.778 void StatusNotifierItemFactory::connectToSnw() Invalid interface to SNW_SERVICE```
* Never seems to mark something as "confirmed". Not sure if this is related to the above.
