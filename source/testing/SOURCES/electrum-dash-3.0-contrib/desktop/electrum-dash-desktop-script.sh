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
# example), they will have to run electrum-dash from the commandline.

_name=electrum-dash
_datadir=.config/${_name}
_walletpath=${_datadir}/wallets/default_wallet
_config=${_datadir}/config
_legacy_datadir=.${_name}
_legacy_config=${_legacy_datadir}/config
_legacy_walletpath=${_legacy_datadir}/wallets/default_wallet

# Create ~/.config/electrum directory if it doesn't exist. Set the
# permissions to something better than 755 and kick off the main process.

# When you run "electrum-dash" from the system menus, the echo will be written to journald
# journalctl -f -t electrum-dash.desktop
echo "Kicking off 'electrum --dir ~/${_datadir} --wallet ~/${_walletpath}'"
echo "... first looking in '~/${_datadir}/'"
echo "... then looking in '~/${_legacy_datadir}/'"
if [ ! -e ${_datadir} ] && [ -e ${_legacy_datadir} ] && [ -d ${_legacy_datadir} ]
then
  echo "... found ~/${_legacy_datadir}/ instead. Using that."
  _datadir=${_legacy_datadir}
  _config=${_legacy_config}
  _walletpath=${_legacy_walletpath}
else
  if [ ! -e .config ]
  then
    echo "... directory ~/.config/ doesn't exist. Create it."
    /usr/bin/mkdir -p .config
  elif [ ! -d .config ]
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
    notify-send "Electrum Dash" "We found ~/${_datadir}/ but it is not a directory. ABORT ABORT!" -t 5000
    exit 1
  else
    # Really should think about not forcing this. Or at least something better.
    echo "... found ~/${_datadir}/ ... setting to m750 for better protection."
    chmod 750 ${_datadir}
  fi
fi

echo "Data dir and wallet path settled: ${_name} --dir $_datadir --wallet $_walletpath"
if [ ! -e $_walletpath ]
then
  echo "...but wallet does not exist. creating wallet when application starts - if desire using a separate wallet elsewhere, run '${_name}' from the commandline and explicitely reference datadir and path to wallet: '${_name} --dir $_datadir --wallet FULL_PATH_TO_YOUR_WALLET'"
  /usr/share/${_name}/${_name} --dir $_datadir
else
  /usr/share/${_name}/${_name} --dir $_datadir --wallet $_walletpath
fi
