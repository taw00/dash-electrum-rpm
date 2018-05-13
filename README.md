# Dash Electrum
**The Dash Electrum Lightweight Crypocurrency Desktop Wallet for Fedora Linux**

## Important commentary

> **DON'T USE THIS FOR SERIOUS MONEY**
>
> Please understand that this software package is still being tested. Let me
> know if you run into any issues.

> **A key difference between Dash Electrum on Fedora (this version) and upstream's version**
> 
> When invoking Dash Electrum from your desktop menus, the default location of
> the data directory and wallet are different.  The "correct" location for an
> application's datadir on a standards-compliant linux system is under the
> subdirectory `~/.config/`. I.e., `~/.config/electrum-dash`.  Therefore...

> Data directory (if launched from menus):  `~/.config/electrum-dash/`  
> Legacy (upstream's default) data dir: `~/.electrum-dash/`  
> 
> If your data directory is already established at the legacy location, this
> version for Dash Electrum will continue to utilize that location. If you run
> `electrum-dash` from the commandline, the behavior is to, by default, use the
> legacy location. I may change that in the future.

## Initial installation

```
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo dnf install -y https://raw.githubusercontent.com/taw00/electrum-dash-rpm/master/toddpkgs-electrum-dash-repo-1.0-0.2.testing.fc28.taw0.noarch.rpm
sudo dnf list | grep electrum
sudo dnf list --refresh | grep electrum # if it doesn't show up right away
sudo dnf install electrum-dash
```

Then browse your desktop menuing system for Dash Electrum! :)

## More information

* Home for these RPMs (you are here): <https://github.com/taw00/electrum-dash-rpm/>
* Website for the originating application: <http://electrum.dash.org/>
* Github for the originating application: <https://github.com/akhavr/electrum-dash>
* Documentation (at dash.org): <https://docs.dash.org/en/latest/wallets/index.html#dash-electrum-wallet>

For feedback or comment: **`t0dd_at_protonmail.com`**

---

## Known issues:

* No known significant issues.

Past issues...

* Segfaults on Send > QR Code **--FIXED in v3.0.6 - though doesn't work with my camera**
* ```"sni-qt/14318" WARN  20:57:02.778 void StatusNotifierItemFactory::connectToSnw() Invalid interface to SNW_SERVICE``` **--FIXED (v3.0.6)**
* Never seems to mark something as "confirmed" **--FIXED (v3.0.6)**
* Default directory has permissions 755. Really should be 751. But the wallet
  is encrypted so... meh. **--FIXED in launched-from-menus version**
* Default directory is `~/.electrum-dash`. Should really be
  `~/.config/electrum-dash` **--implemented in launched-from-menus version**

