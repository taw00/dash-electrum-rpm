# Dash Electrum
**The Dash Electrum Lightweight Crypocurrency Desktop Wallet for Fedora Linux**

Send and recieve Dash cryptocurrency on your desktop without the burden of
running a full node. I.e., this is a light client for the desktop.

## Important commentary

> Please understand that this software package is still being tested. Let me
> know if you run into any issues.

> **A key difference between Dash Electrum on Fedora (this version) and upstream's version**
> 
> This version of Dash Electrum effectively runs in this manner:<br />
> `/usr/share/org.dash.electrum.dash-electrum/dash-electrum --dir .config/electrum-dash --wallet .config/electrum-dash/default_wallet`<br />
> ...whereas by default, the data directory would have been `~/.electrum-dash/`
> 
> BUT! If your data directory is already established at the legacy location, this
> version for Dash Electrum will continue to utilize that location.

## Initial installation

```
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo dnf install -y https://raw.githubusercontent.com/taw00/dash-electrum-rpm/master/toddpkgs-electrum-dash-repo-1.0-0.2.testing.fc28.taw0.noarch.rpm
sudo dnf list | grep electrum
sudo dnf list --refresh | grep electrum # if it doesn't show up right away
sudo dnf install electrum-dash
```

Then browse your desktop menuing system for Dash Electrum! :)

_**There is a flatpak available**_

I do not maintain it (and therefore I advise caution) but there is a flatpak
available for Dash Electrum. Check it out if you prefer package installation in
that manner: <https://flathub.org/apps/details/org.dash.electrum.electrum_dash>

## More information

* Home for these RPMs (you are here): <https://github.com/taw00/dash-electrum-rpm/>
* Website for the originating application: <http://electrum.dash.org/>
* Github for the originating application: <https://github.com/akhavr/electrum-dash>
* Documentation (at dash.org): <https://docs.dash.org/en/stable/wallets/index.html#dash-electrum-wallet>

For feedback or comment: **`t0dd_at_protonmail.com`**

---

## Known issues:

* None at this time.

