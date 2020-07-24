#!/usr/bin/bash
#
# This script is triggered by Dash Electrum selected in the menuing system.
# It looks for and defaults to ~/.config/electrum-dash as the default data
# directory as opposed to the upstream (but not very linuxy) ~/.electrum-dash
#
# If the user is already using the legacy location, the application will
# continue to use that old location.
#
# If the user wants to do something fancy (different wallet location for
# example), they will have to run
# /usr/share/org.dash.electrum.dash_electrum/dash-electrum from the commandline.
#
# Note, I really wish I had settled on .config/dash-electrum instead, but the
# project kinda had an issue with the naming for some time until it settled.

_name0=electrum-dash
_name1=dash-electrum
_appid=org.dash.electrum.dash_electrum
_appdir=/usr/share/${_appid}
_datadir=$HOME/.config/${_name0}
_config=${_datadir}/config
_legacy_datadir=.${_name0}
_legacy_config=${_legacy_datadir}/config

# explicitly configuring a walletpath is a bit overkill. The default behavior is the same.
_walletpath=${_datadir}/wallets/default_wallet
_legacy_walletpath=${_legacy_datadir}/wallets/default_wallet
if [ $1 == "testnet" ] ; then
    _testnet=" --testnet"
    _walletpath=${_datadir}/testnet/wallets/default_wallet
    _legacy_walletpath=${_legacy_datadir}/testnet/wallets/default_wallet
fi

# Create ~/.config/electrum directory if it doesn't exist. Set the
# permissions to something better than 755 and kick off the main process.

# When you run "dash-electrum" from the system menus, the echo will be written to journald
# journalctl -f -t dash-electrum
echo "Kicking off '${_appdir}/${_name1}${_testnet} --dir ~/${_datadir} --wallet ~/${_walletpath}'"
echo "... first looking in '~/${_datadir}/'"
echo "... then looking in '~/${_legacy_datadir}/'"
if [ ! -e ${_datadir} ] && [ -e ${_legacy_datadir} ] && [ -d ${_legacy_datadir} ]
then
  echo "... found ~/${_legacy_datadir}/ instead. Using that."
  _datadir=${_legacy_datadir}
  _config=${_legacy_config}
  _walletpath=${_legacy_walletpath}
else
  if [ ! -e $HOME/.config ]
  then
    echo "... directory ~/.config/ doesn't exist. Create it."
    /usr/bin/mkdir -p $HOME/.config
  elif [ ! -d $HOME/.config ]
  then
    echo "... location ~/.config is not a directory!!! ABORT ABORT!"
    notify-send "Dash Electrum" "Location ~/.config is not a directory!!! ABORT ABORT!" -t 5000
    exit 1
  fi
  # At this point, we created ~/.config/ or we aborted
  if [ ! -e ${_datadir} ]
  then
    echo "... ~/${_datadir}/ does not exist. Create it."
    /usr/bin/mkdir -p -m750 ${_datadir}
  elif [ ! -d ${_datadir} ]
  then
    echo "... we found ~/${_datadir}/ but it is not a directory. ABORT ABORT!"
    notify-send "Dash Electrum" "We found ~/${_datadir}/ but it is not a directory. ABORT ABORT!" -t 5000
    exit 1
  else
    # Really should think about not forcing this. Or at least something better.
    echo "... found ~/${_datadir}/ ... setting to m750 for better protection."
    chmod 750 ${_datadir}
  fi
fi

echo "Data dir and wallet path settled: ${_appdir}/${_name1}${_testnet} --dir $_datadir --wallet $_walletpath"
if [ ! -e $_walletpath ]
then
  echo "...but wallet does not exist. creating wallet when application starts - if desire using a separate wallet elsewhere, run '${_appdir}/${_name1}${_testnet}' from the commandline and explicitely reference datadir and path to wallet: '${_appdir}/${_name1}${_testnet} --dir $_datadir --wallet FULL_PATH_TO_YOUR_WALLET'"
  ${_appdir}/${_name1}${_testnet} --dir $_datadir
else
  ${_appdir}/${_name1}${_testnet} --dir $_datadir --wallet $_walletpath
fi
