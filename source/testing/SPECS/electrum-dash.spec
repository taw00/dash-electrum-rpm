# electrum-dash.spec
#
# This SPEC file with appropriate source archives will build and install
# Dash Electrum Light Wallet.
#
# Name confusion: Note that application is sometimes referred to as "Electrum
# Dash" and other times as "Dash Electrum". We will use "Dash Electrum"
# when referring to it formally. And the the executable will be in both
# orderings.
#
# Note that we have a flag 'sourceIsPrebuilt' that chooses one of two methods
# to "build" this application. If flipped off, it will attempt to build the
# whole stack. If flipped on, we build from a semi-prebuilt version of Dash
# Electrum. The release will have an "rp" attached to it which stands for
# "repackage". It's not a blatant repackage, but it is close. Makes for a
# bloated .src.rpm package, but whatever.


Name: electrum-dash
%define name2 Electrum-DASH
%define name3 dash-electrum
Summary: An easy-to-use Dash cryptocurrency light client for the desktop

%define targetIsProduction 0
%define includeSnapinfo 1
%define includeMinorbump 1
%define sourceIsPrebuilt 0


# Package (RPM) name-version-release.
# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]

# VERSION
# eg. 1.0.1
%define vermajor 3.0
%define verminor 6
Version: %{vermajor}.%{verminor}


# RELEASE
# If production - "targetIsProduction 1"
# eg. 1 (and no other qualifiers)
%define pkgrel_prod 1

# If pre-production - "targetIsProduction 0"
# eg. 0.6.testing -- pkgrel_preprod should always equal pkgrel_prod-1
%define pkgrel_preprod 0
%define extraver_preprod 1
%define snapinfo testing
#%%define snapinfo testing.20180424
#%%define snapinfo beta2.41d5c63.gh

# if sourceIsPrebuilt (rp=repackaged)
# eg. 1.rp (prod) or 0.6.testing.rp (pre-prod)
%define snapinfo_rp rp

# if includeMinorbump
%define minorbump taw1

# Building the release string (don't edit this)...

%if %{targetIsProduction}
  %if %{includeSnapinfo}
    %{warn:"Warning: target is production and yet you want snapinfo included. This is not typical."}
  %endif
%else
  %if ! %{includeSnapinfo}
    %{warn:"Warning: target is pre-production and yet you elected not to incude snapinfo (testing, beta, ...). This is not typical."}
  %endif
%endif

# release numbers
%undefine _relbuilder_pt1
%if %{targetIsProduction}
  %define _pkgrel %{pkgrel_prod}
  %define _relbuilder_pt1 %{pkgrel_prod}
%else
  %define _pkgrel %{pkgrel_preprod}
  %define _extraver %{extraver_preprod}
  %define _relbuilder_pt1 %{_pkgrel}.%{_extraver}
%endif

# snapinfo and repackage (pre-built) indicator
%undefine _relbuilder_pt2
%if ! %{includeSnapinfo}
  %undefine snapinfo
%endif
%if 0%{?sourceIsPrebuilt:1}
  %if ! %{sourceIsPrebuilt}
    %undefine snapinfo_rp
  %endif
%else
  %undefine snapinfo_rp
%endif
%if 0%{?snapinfo_rp:1}
  %if 0%{?snapinfo:1}
    %define _relbuilder_pt2 %{snapinfo}.%{snapinfo_rp}
  %else
    %define _relbuilder_pt2 %{snapinfo_rp}
  %endif
%else
  %if 0%{?snapinfo:1}
    %define _relbuilder_pt2 %{snapinfo}
  %endif
%endif

# put it all together
# pt1 will always be defined. pt2 and minorbump may not be
%define _release %{_relbuilder_pt1}
%if ! %{includeMinorbump}
  %undefine minorbump
%endif
%if 0%{?_relbuilder_pt2:1}
  %if 0%{?minorbump:1}
    %define _release %{_relbuilder_pt1}.%{_relbuilder_pt2}%{?dist}.%{minorbump}
  %else
    %define _release %{_relbuilder_pt1}.%{_relbuilder_pt2}%{?dist}
  %endif
%else
  %if 0%{?minorbump:1}
    %define _release %{_relbuilder_pt1}%{?dist}.%{minorbump}
  %else
    %define _release %{_relbuilder_pt1}%{?dist}
  %endif
%endif

Release: %{_release}
# ----------- end of release building section

# You can/should use URLs for sources as well. That is beyond the scope of
# this example.
# https://fedoraproject.org/wiki/Packaging:SourceURL
Source0: %{name}-%{version}.tar.gz
Source1: %{name}-%{vermajor}-contrib.tar.gz
%if %{sourceIsPrebuilt}
Source10: %{name2}-%{version}.tar.gz
%endif

Requires: python3 python3-qt5
Requires: python3-jsonrpclib python3-pbkdf2 python3-protobuf
Requires: python3-qrcode python3-ecdsa python3-pyaes python3-dns
Requires: python3-requests python3-six python3-mnemonic python3-hidapi
Requires: python3-trezor python3-libusb1

# Turn off the brp-python-bytecompile automagic (RPM's auto-bytecompile)
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation
#%%?disable_automagic_pybytecompile
# That didn't work. Trying option two...
# https://fedoraproject.org/wiki/Packaging:Python_Appendix#Manual_byte_compilation
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# Force Python3 as __python default even if Python2 is present (and it usually is).
# Note, this is going away as an advised path.
%global __python %{__python3}

# So I can introspect the mock build environment...
BuildRequires: tree
#BuildRequires: tree vim-enhanced less

# Required for desktop applications (validation of .desktop and .xml files)
BuildRequires: desktop-file-utils libappstream-glib

# may not need git
BuildRequires: git

# For pyrcc5 (python3-qt5), protoc (protobuf-compiler)
BuildRequires: python3 python3-devel protobuf-compiler
BuildRequires: python3-qt5 python3-qt5-devel
# For pycurl, gettext, libusb.h, libudev.so
BuildRequires: python3-pycurl gettext libusb-devel systemd-devel
BuildRequires: python3-jsonrpclib python3-pbkdf2 python3-protobuf
BuildRequires: python3-qrcode python3-ecdsa python3-pyaes python3-dns
BuildRequires: python3-requests python3-six python3-mnemonic python3-hidapi
BuildRequires: python3-trezor python3-libusb1


# CentOS/RHEL/EPEL can't do "Suggests:"
%if 0%{?fedora:1}
#Suggests:
%endif

License: MIT
URL: https://github.com/taw00/electrum-dash-rpm
# Group is deprecated. Don't use it. Left here as a reminder...
# https://fedoraproject.org/wiki/RPMGroups 
#Group: Unspecified

# If you comment out "debug_package" RPM will create additional RPMs that can
# be used for debugging purposes. I am not an expert at this, BUT ".build_ids"
# are associated to debug packages, and I have lately run into packaging
# conflicts because of them. This is a topic I can't share a whole lot of
# wisdom about, but for now... I turn all that off.
# 
# How debug info and build_ids managed (I only halfway understand this):
# https://github.com/rpm-software-management/rpm/blob/master/macros.in
%define debug_package %{nil}
%define _unique_build_ids 1
%define _build_id_links alldebug

# https://fedoraproject.org/wiki/Changes/Harden_All_Packages
# https://fedoraproject.org/wiki/Packaging:Guidelines#PIE
%define _hardened_build 1

# Extracted source tree structure (extracted in .../BUILD)
#   srcroot               {name}-1.0
#      \_srccodetree        \_{name}-1.0.1
#      \_srccodetree2       \_{name2}-1.0.1
#      \_srccontribtree     \_{name}-1.0-contrib
%define srcroot %{name}-%{vermajor}
%define srccodetree %{name}-%{version}
%define srccodetree2 %{name2}-%{version}
%define srccontribtree %{name}-%{vermajor}-contrib
# /usr/share/electrum-dash
%define installtree %{_datadir}/%{name}


%description
Dash Electrum is a fully featured cryptocurrency light wallet for the desktop.
The Dash Crytocurrency is a revolutionary digital money system. Instant,
private, and secure.

%prep
# an rpm creation step (right prior to %%build step)
# Prep section starts us in directory .../BUILD -or- {_builddir}
# 
# References (the docs for this universally suck):
# * http://ftp.rpm.org/max-rpm/s1-rpm-inside-macros.html
# * http://rpm.org/user_doc/autosetup.html
# * autosetup -q and setup -q leave out the root directory.
# I create a root dir and place the source and contribution trees under it.
# Extracted source tree structure (extracted in .../BUILD)
#   srcroot               {name}-{vermajor}
#      \_srccodetree        \_{name}-{version}
#      \_srccodetree2       \_{name2}-{version}
#      \_srccontribtree     \_{name}-{vermajor}-contrib

mkdir -p %{srcroot}
# sourcecode
%setup -q -T -D -a 0 -n %{srcroot}
# contrib
%setup -q -T -D -a 1 -n %{srcroot}
# sourcecode
%if %{sourceIsPrebuilt}
%setup -q -T -D -a 10 -n %{srcroot}
%endif

# Libraries ldconfig file - we create it, because lib or lib64
#echo "%%{_libdir}/%%{name}" > %%{srccontribtree}/etc-ld.so.conf.d_%%{name}.conf

# misspelled filename
mv %{srccodetree}/LICENCE %{srccodetree}/LICENSE
%if %{sourceIsPrebuilt}
mv %{srccodetree2}/LICENCE %{srccodetree2}/LICENSE
%endif
## to quiet a syntax error
## XXX holdover from v2.9.4 - going away
#cp %%{srccontribtree}/srcroot/lib_paymentrequest.proto %%{srccodetree}/lib/paymentrequest.proto
#%if %{sourceIsPrebuilt}
#cp %%{srccontribtree}/srcroot/lib_paymentrequest.proto %%{srccodetree2}/lib/paymentrequest.proto
#%endif

# For debugging purposes...
cd .. ; /usr/bin/tree -df -L 1 %{srcroot} ; cd -


%build
# an rpm creation step (right prior to %%install step)
# This section starts us in directory {_builddir}/{srcroot}

## Man Pages - not used as of yet
#gzip %%{buildroot}%%{_mandir}/man1/*.1

cd %{srccontribtree}
#/usr/bin/pip install x11-hash-1.4.zip --user
#/usr/bin/pip install x11-hash-1.4.zip -t ./
#/usr/bin/pip install trezor-0.9.0.tar.gz --user
#/usr/bin/pip install trezor-0.9.0.tar.gz -t ./
cd ..

%if %{sourceIsPrebuilt}
  cd %{srccodetree2}
  # Doin' like this (sorta): https://docs.dash.org/en/latest/wallets/electrum/installation.html`
  /usr/bin/pip install . --user
%else
  # I've had issues getting this to build still solidifying
  cd %{srccodetree}
  # we don't have root access to /usr/lib/python2.7/site-packages/ (or python3.6)
  # Need to build everything locally
  # https://docs.python.org/3/install/index.html#alternate-installation
  %__python3 setup.py install --user
  
  /usr/bin/pyrcc5 icons.qrc -o gui/qt/icons_rc.py
  /usr/bin/protoc --proto_path=lib/ --python_out=lib/ lib/paymentrequest.proto
  #./contrib/make_locale
  #./contrib/make_packages
%endif


%install
# an rpm creation step (right prior to %%files step)
# This section starts us in directory {_builddir}/{srcroot}
#
# Cheatsheet for built-in RPM macros:
#   _builddir = /.../BUILD
#   buildroot = /.../BUILDROOT
#   _bindir = /usr/bin
#   _sbindir = /usr/sbin
#   _datadir = /usr/share
#   _mandir = /usr/share/man
#   _sysconfdir = /etc
#   _localstatedir = /var
#   _sharedstatedir is /var/lib
#   _prefix = /usr
#   _libdir = /usr/lib or /usr/lib64 (depending on system)
#   https://fedoraproject.org/wiki/Packaging:RPMMacros
# These three are defined in newer versions of RPM (Fedora not el7)
%define _tmpfilesdir /usr/lib/tmpfiles.d
%define _unitdir /usr/lib/systemd/system
%define _metainfodir %{_datadir}/metainfo

# Create directories
# /usr/bin/ and /usr/sbin/
install -d -m755 -p %{buildroot}%{_bindir}
install -d -m755 -p %{buildroot}%{_sbindir}
# /usr/share/applications/
install -d %{buildroot}%{_datadir}/applications
# /etc/ld.so.conf.d/
install -d %{buildroot}%{_sysconfdir}/ld.so.conf.d
# /usr/share/electrum-dash/
install -d %{buildroot}%{installtree}

# XXX -- experimental and holdover stuff from 2.9.4 -todd
# /usr/[lib,lib64]/electrum-dash/
#install -d %%{buildroot}%%{_libdir}/%%{name}
# /etc/electrum-dash/
#install -d %%{buildroot}%%{_sysconfdir}/%%{name}
# /var/lib/electrum-dash/...
#install -d %%{buildroot}%%{_sharedstatedir}/%%{name}
# /var/log/electrum-dash/
#install -d -m750 %%{buildroot}%%{_localstatedir}/log/%%{name}
## /usr/lib/python2.7/site-packages/ (python2) or /usr/lib/python3.6/site-packages/ (python3)
## XXX holdover from v2.9.4 - going away
#%%define _site_packages2 %%(%%__python2 -c "import site; print(site.getsitepackages()[0])")
#%%define _site_packages3 %%(%%__python3 -c "import site; print(site.getsitepackages()[0])")
#install -d %%{buildroot}%%{_site_packages2}
#install -d %%{buildroot}%%{_site_packages3}
# Binaries
#install -D -p %%{srccodetree}/%%{name}-process.sh %%{buildroot}%%{installtree}/%%{name}-process.sh

%if %{sourceIsPrebuilt}
  cp -a %{srccodetree2}/* %{buildroot}%{installtree}/
%else
  cp -a %{srccodetree}/* %{buildroot}%{installtree}/
%endif

# Desktop
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.16x16.png   %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.22x22.png   %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.24x24.png   %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.256x256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.32x32.png   %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.48x48.png   %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.svg         %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.svg

install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.128x128.png %{buildroot}%{_datadir}/icons/highcontrast/128x128/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.16x16.png   %{buildroot}%{_datadir}/icons/highcontrast/16x16/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.22x22.png   %{buildroot}%{_datadir}/icons/highcontrast/22x22/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.24x24.png   %{buildroot}%{_datadir}/icons/highcontrast/24x24/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.256x256.png %{buildroot}%{_datadir}/icons/highcontrast/256x256/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.32x32.png   %{buildroot}%{_datadir}/icons/highcontrast/32x32/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.48x48.png   %{buildroot}%{_datadir}/icons/highcontrast/48x48/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.svg         %{buildroot}%{_datadir}/icons/highcontrast/48x48/apps/%{name}.svg

# electrum-dash.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications/ %{srccontribtree}/desktop/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

# electrum-dash.appdata.xml
install -D -m644 -p %{srccontribtree}/desktop/%{name}.appdata.xml %{buildroot}%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

# Binaries
ln -s %{installtree}/%{name} %{buildroot}%{_bindir}/%{name}
ln -s %{installtree}/%{name} %{buildroot}%{_bindir}/%{name3}

## Special needs
## XXX holdover from v2.9.4 - going away
#cp -a %%{srccontribtree}/x11_hash* %%{buildroot}%%{_site_packages2}/
#cp -a %%{srccontribtree}/trezor* %%{buildroot}%%{_site_packages}/


%files
# an rpm creation step
# This section starts us in directory {_buildrootdir}
# (note, macros like %%docs, etc may locate in {_builddir}
%defattr(-,root,root,-)
%license %{srccodetree}/LICENSE

# The directories...
# /usr/share/electrum-dash/
%dir %{installtree}

%{installtree}/*

# Desktop
%{_datadir}/icons/*
%{_datadir}/applications/%{name}.desktop
%{_metainfodir}/%{name}.appdata.xml

# Binaries
%{_bindir}/%{name}
%{_bindir}/%{name3}

# Special needs
# XXX holdover from v2.9.4 - going away
#%%{_site_packages3}/x11_hash*
#%%{_site_packages3}/trezor*


%pre
# an installation step (runs right prior to installation)

%post
# an installation step (runs after install process is complete)
/usr/bin/update-desktop-database &> /dev/null || :

%postun
# an uninstallation step (runs after uninstall process is complete)
/usr/bin/update-desktop-database &> /dev/null || :


%changelog
* Sat May 12 2018 Todd Warner <t0dd@protonmail.com> 3.0.6-0.1.testing.taw[n]
  - v3.0.6
  - python3 and QT5 stuff and turn off automated byte-compiling of python
    since it is so error-prone:  
    https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation  
    https://fedoraproject.org/wiki/Packaging:Python_Appendix#Manual_byte_compilation
  - Added a whole pile of app icons (in -contrib tarball)
  - desktop-file-validate and appstream-util validate-relax added as is  
    required of desktop applications.
  - spec file change: mkdir -p instead of just mkdir, otherwise repeated  
    rpmbuilds without full cleanup will explode

* Fri May 4 2018 Todd Warner <t0dd@protonmail.com> 2.9.4-0.1.testing.taw[n]
  - spec file change: update the desktop database upon post installation or  
    uninstallation
  
* Fri May 4 2018 Todd Warner <t0dd@protonmail.com> 2.9.4-0.1.testing.taw[n]
  - Initial test build.
