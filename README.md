# Dash Electrum
The Dash Electrum Lightweight Crypocurrency Desktop Wallet for Fedora Linux

> **DON'T USE THIS FOR SERIOUS MONEY**
> Please understand that this software package is still being tested. Let me know if you
run into any issues please.

```
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo dnf install -y https://raw.githubusercontent.com/taw00/electrum-dash-rpm/master/toddpkgs-electrum-dash-repo-1.0-0.2.testing.fc28.taw0.noarch.rpm
sudo dnf list | grep electrum
sudo dnf list --refresh | grep electrum # if it doesn't show up right away
sudo dnf install electrum-dash
```

Then browse your desktop menuing system for Dash Electrum! :)

Primary website and github for the originating application is here and here: <http://electrum.dash.org/> - <https://github.com/akhavr/electrum-dash>

For feedback or comment: <t0dd@protonmail.com>

---

## Known issues (still only building test packages):

You can send and receive funds, but...

* Segfaults on Send > QR Code **--FIXED (v3.0.6 - though doesn't work with my camera)**
* ```"sni-qt/14318" WARN  20:57:02.778 void StatusNotifierItemFactory::connectToSnw() Invalid interface to SNW_SERVICE``` **--FIXED (v3.0.6)**
* Never seems to mark something as "confirmed" **--FIXED (v3.0.6)**
* Default directory has permissions 755. Really should be 750. But the wallet is encrypted so... meh.
* Default directory is ~/.electrum-dash. Should really be ~/.config/electrum-dash -- I may address this. We'll see.

