# dash-electrum.spec
# vim:tw=0:ts=2:sw=2:et:
#
# This SPEC file with appropriate source archives will build and install
# Dash Electrum Light Wallet.
#
# Name confusion: Note that application is sometimes referred to as "Electrum
# Dash" and other times as "Dash Electrum". We will use "Dash Electrum"
# when referring to it formally. And the the executable will be in both
# orderings.
#
# UPDATE (2018-10-14):
# Upstream now refers to this application as Dash Electrum (and Dash-Electrum),
# though the source code is still exported as electrum-dash-*.tar.gz
#
# Note that we have a flag '%sourceIsPrebuilt' that chooses one of two methods
# to "build" this application. If flipped off, it will attempt to build the
# whole stack. If flipped on, we build from a semi-prebuilt version of Dash
# Electrum. The release will have an "rp" attached to it which stands for
# "repackage". It's not a blatant repackage, but it is close. Makes for a
# bloated .src.rpm package, but whatever.

%define name0 dash-electrum
%define name1 electrum-dash
%define name2 Dash-Electrum
%define name3 Electrum-Dash
Name: %{name0}

Summary: An easy-to-use Dash cryptocurrency light client for the desktop

%define targetIsProduction 0
%define sourceIsPrebuilt 0

# Is the version number 3 or 4 component? x.y.z or x.y.z.zz?
# Eg. (3) 2.9.4, 3.0.6, 3.1.3 ...or (4) 3.0.6.3
%define versionIsFourComponents 1


# Package (RPM) name-version-release.
# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]

# VERSION
%define vermajor 3.3
%define verminor 8
%define verminor2 2
%if %{versionIsFourComponents}
Version: %{vermajor}.%{verminor}.%{verminor2}
%else
Version: %{vermajor}.%{verminor}
%endif

# RELEASE
%define _pkgrel 1
%if ! %{targetIsProduction}
  %define _pkgrel 1.1
%endif

# MINORBUMP
# (for very small or rapid iterations)
%define minorbump taw
#%%undefine minorbump taw

#
# Build the release string - don't edit this
#

# rp = repackaged
# eg. 1.rp (prod) or 0.6.testing.rp (pre-prod)
%define _snapinfo testing
%define _snapinfo_rp rp

%if %{targetIsProduction}
  %undefine snapinfo
%endif

%if ! %{sourceIsPrebuilt}
   %undefine _snapinfo_rp
%endif

%if 0%{?_snapinfo:1}
  %if 0%{?_snapinfo_rp:1}
    %define snapinfo %{_snapinfo}.%{_snapinfo_rp}
  %else
    %define snapinfo %{_snapinfo}
  %endif
%else
  %if 0%{?_snapinfo_rp:1}
    %define snapinfo %{_snapinfo_rp}
  %else
    %undefine snapinfo
  %endif
%endif

# pkgrel will be defined, snapinfo and minorbump may not be
%define _release %{_pkgrel}
%if 0%{?snapinfo:1}
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}
  %endif
%else
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}%{?dist}
  %endif
%endif

Release: %{_release}

# ----------- end of release building section

# how are debug info and build_ids managed (I only halfway understand this):
# https://github.com/rpm-software-management/rpm/blob/master/macros.in
%define debug_package %{nil}
%define _unique_build_ids 1
%define _build_id_links alldebug

# https://fedoraproject.org/wiki/Changes/Harden_All_Packages
%define _hardened_build 1

# Needed because of naming change from electrum-dash to dash-electrum as of
# version 3.2.3 (otherwise package will not update).
Provides: electrum-dash = 3.2.3
Obsoletes: electrum-dash < 3.2.3

# You can/should use URLs for sources.
# https://fedoraproject.org/wiki/Packaging:SourceURL
Source0: https://github.com/akhavr/electrum-dash/archive/%{version}/%{name1}-%{version}.tar.gz
#Source0: %%{name1}-%%{version}.tar.gz
Source1: https://github.com/taw00/electrum-dash-rpm/blob/master/SOURCES/%{name}-%{vermajor}-contrib.tar.gz
%if %{sourceIsPrebuilt}
Source10: %{name2}-%{version}.tar.gz
%endif

# Challenging: Unsure of what "Requires" are required for build versus runtime.
# Thus they closely mirror.
Requires: python3 python3-qt5
Requires: python3-jsonrpclib python3-pbkdf2 python3-protobuf
Requires: python3-qrcode python3-ecdsa python3-pyaes python3-dns
Requires: python3-requests python3-six python3-mnemonic python3-hidapi
Requires: python3-trezor python3-libusb1
# additional requires from ./contrib/requirements.txt
Requires: python3-certifi python3-chardet python3-idna python3-pysocks

# For Kivy? Fedora doesn't ship python3-kivy unfortunately
Requires: mtdev python3-pillow python3-pygame

# Turn off the brp-python-bytecompile automagic (RPM's auto-bytecompile)
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation
#%%?disable_automagic_pybytecompile
# That didn't work. Trying option two...
# https://fedoraproject.org/wiki/Packaging:Python_Appendix#Manual_byte_compilation
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# Force Python3 as __python default even if Python2 is present (and it usually is).
# Note, this is going away as an advised path.
%global __python %{__python3}

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
# additional requires from ./contrib/requirements.txt
BuildRequires: python3-certifi python3-chardet python3-idna python3-pysocks
# /usr/bin/pip3 and /usr/bin/pip
BuildRequires: python3-pip python2-pip
# For Kivy? Fedora doesn't ship python3-kivy unfortunately
# Same as above: python3-devel git
BuildRequires: mesa-libGL-devel python3-Cython
BuildRequires: gstreamer1-devel SDL2_ttf-devel SDL2_image-devel SDL2_mixer-devel
BuildRequires: SDL2_image SDL2_mixer SDL2_ttf python3-pygame
#BuildRequires: ImageMagick

#t0dd: for build environment introspection
%if ! %{targetIsProduction}
BuildRequires: tree vim-enhanced less findutils dnf
%endif


License: MIT
URL: https://github.com/taw00/electrum-dash-rpm
ExclusiveArch: x86_64 i686 i386

# Extracted source tree structure (extracted in .../BUILD)
#   srcroot               {name}-1.0
#      \_srccodetree        \_{name1}-1.0.1
#      \_srccodetree2       \_{name2}-1.0.1
#      \_srccontribtree     \_{name}-1.0-contrib
%define srcroot %{name}-%{vermajor}
%define srccodetree %{name1}-%{version}
#%%define srccodetree2 %%{name2}-%%{version}
%define srccontribtree %{name}-%{vermajor}-contrib
# /usr/share/dash-electrum
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
#      \_srccodetree        \_{name1}-{version}
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
cp %{srccodetree}/LICENCE %{srccontribtree}/LICENSE
%if %{sourceIsPrebuilt}
  ####cp %%{srccodetree2}/LICENCE %%{srccontribtree}/LICENSE
%endif

# For debugging purposes...
cd .. ; /usr/bin/tree -df -L 1 %{srcroot} ; cd -


%build
# an rpm creation step (right prior to %%install step)
# This section starts us in directory {_builddir}/{srcroot}

## Man Pages - not used as of yet
#gzip %%{buildroot}%%{_mandir}/man1/*.1

cd %{srccontribtree}
####/usr/bin/pip3 install kivy --user
####/usr/bin/pip3 install kivy -t ./
####python3 setup.py install --prefix=%%{_prefix} --root=%%{buildroot}
###/usr/bin/pip3 install x11_hash.akhavr-master-20180514.zip --user
###/usr/bin/pip3 install x11_hash.akhavr-master-20180514.zip -t ./
####/usr/bin/pip3 install trezor-0.9.0.tar.gz --user
####/usr/bin/pip3 install trezor-0.9.0.tar.gz -t ./
cd ..

%if %{sourceIsPrebuilt}
  # XXX going away soon
  #cd %%{srccodetree2}
  # Doin' like this (sorta): https://docs.dash.org/en/latest/wallets/electrum/installation.html`
  #/usr/bin/pip install . --user

# Source is NOT prebuilt...
%else
  cd %{srccodetree}
  #/usr/bin/pip3 install pip==18.1
  /usr/bin/pip3 install .[fast] -t ./
  # ImageMagick conversion of svg's to png's -- not needed for versions after 3.2.5?
  #for i in lock unlock confirmed status_lagging status_disconnected status_connected_proxy status_connected status_waiting preferences; do convert -background none icons/$i.svg icons/$i.png; done
  # compile icons for QT -- not needed for versions after 3.2.5?
  #mkdir -p gui/qt
  #/usr/bin/pyrcc5 icons.qrc -o gui/qt/icons_rc.py
  # protobuf-compiler
  /usr/bin/protoc --proto_path=electrum_dash --python_out=electrum_dash electrum_dash/paymentrequest.proto
  # python3-requests gettext -- translations (OPTIONAL)
  ./contrib/make_locale
  # make the packages -- not needed for versions after 3.2.5?
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
# This is used to quiet rpmlint who can't seem to understand that /usr/lib is
# still used for certain things.
%define _rawlib lib
%define _usr_lib /usr/%{_rawlib}
# These three are already defined in newer versions of RPM, but not in el7
%if 0%{?rhel} && 0%{?rhel} < 8
  %define _tmpfilesdir %{_usr_lib}/tmpfiles.d
  %define _unitdir %{_usr_lib}/systemd/system
  %define _metainfodir %{_datadir}/metainfo
%endif

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
## XXX might be going away
## /usr/lib/python2.7/site-packages/ (python2) or /usr/lib/python3.6/site-packages/ (python3)
#%%define _site_packages2 %%(%%__python2 -c "import site; print(site.getsitepackages()[0])")
#install -d %%{buildroot}%%{_site_packages2}
%define _site_packages3 %(%__python3 -c "import site; print(site.getsitepackages()[0])")
install -d %{buildroot}%{python3_sitearch}

# XXX -- experimental and holdover stuff from 2.9.4 -todd
# /usr/[lib,lib64]/dash-electrum/
#install -d %%{buildroot}%%{_libdir}/%%{name}
# /etc/electrum-dash/
#install -d %%{buildroot}%%{_sysconfdir}/%%{name}
# /var/lib/electrum-dash/...
#install -d %%{buildroot}%%{_sharedstatedir}/%%{name}
# /var/log/electrum-dash/
#install -d -m750 %%{buildroot}%%{_localstatedir}/log/%%{name}
# Binaries
#install -D -p %%{srccodetree}/%%{name}-process.sh %%{buildroot}%%{installtree}/%%{name}-process.sh

%if %{sourceIsPrebuilt}
  # XXX Going away soon
  ### cp -a %%{srccodetree2}/* %%{buildroot}%%{installtree}/
%else
  cp -a %{srccodetree}/* %{buildroot}%{installtree}/
%endif

# Desktop
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.16.png  %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.22.png  %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.24.png  %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.32.png  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.48.png  %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.hicolor.svg     %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.svg

install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.128.png %{buildroot}%{_datadir}/icons/HighContrast/128x128/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.16.png  %{buildroot}%{_datadir}/icons/HighContrast/16x16/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.22.png  %{buildroot}%{_datadir}/icons/HighContrast/22x22/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.24.png  %{buildroot}%{_datadir}/icons/HighContrast/24x24/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.256.png %{buildroot}%{_datadir}/icons/HighContrast/256x256/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.32.png  %{buildroot}%{_datadir}/icons/HighContrast/32x32/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.48.png  %{buildroot}%{_datadir}/icons/HighContrast/48x48/apps/%{name}.png
install -D -m644 -p %{srccontribtree}/desktop/%{name}.highcontrast.svg     %{buildroot}%{_datadir}/icons/HighContrast/48x48/apps/%{name}.svg

# dash-electrum.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications/ %{srccontribtree}/desktop/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

# dash-electrum.appdata.xml
install -D -m644 -p %{srccontribtree}/desktop/%{name}.appdata.xml %{buildroot}%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

# Binaries
install -D -m755 -p %{srccontribtree}/desktop/%{name}-desktop-script.sh %{buildroot}%{installtree}/
ln -s %{installtree}/%{name1} %{buildroot}%{_bindir}/%{name}
ln -s %{installtree}/%{name1} %{buildroot}%{_bindir}/%{name1}
ln -s %{installtree}/%{name}-desktop-script.sh %{buildroot}%{_bindir}/%{name}-desktop-script.sh

## Special needs
## XXX -- may be going away
cp -a %{srccontribtree}/x11_hash* %{buildroot}%{python3_sitearch}/
#cp -a %%{srccontribtree}/kivy* %%{buildroot}%%{_site_packages3}/
#cp -a %%{srccontribtree}/trezor* %%{buildroot}%%{_site_packages3}/


%files
# an rpm creation step
# This section starts us in directory {_buildrootdir}
# (note, macros like %%docs, etc may locate in {_builddir}
%defattr(-,root,root,-)
%license %{srccontribtree}/LICENSE

# The directories...
# /usr/share/electrum-dash/
%dir %{installtree}

%{installtree}/*

# Binaries
%{_bindir}/%{name}-desktop-script.sh
%{_bindir}/%{name}
%{_bindir}/%{name1}
# included via {installtree}/* above
#%%{installtree}/%%{name}-desktop-script.sh

# Desktop
%{_datadir}/applications/%{name}.desktop
%{_metainfodir}/%{name}.appdata.xml
# Desktop icons
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.svg
%{_datadir}/icons/HighContrast/128x128/apps/%{name}.png
%{_datadir}/icons/HighContrast/16x16/apps/%{name}.png
%{_datadir}/icons/HighContrast/22x22/apps/%{name}.png
%{_datadir}/icons/HighContrast/24x24/apps/%{name}.png
%{_datadir}/icons/HighContrast/256x256/apps/%{name}.png
%{_datadir}/icons/HighContrast/32x32/apps/%{name}.png
%{_datadir}/icons/HighContrast/48x48/apps/%{name}.png
%{_datadir}/icons/HighContrast/48x48/apps/%{name}.svg

# Special needs
# XXX may be going away soon
%{python3_sitearch}/*
#%%{_site_packages3}/x11_hash*
#%%{_site_packages3}/kivy*
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
* Mon Dec 9 2019 Todd Warner <t0dd_at_protonmail.com> 3.3.8.2-1.1.testing.taw
* Mon Dec 9 2019 Todd Warner <t0dd_at_protonmail.com> 3.3.8.2-0.1.testing.taw
  - 3.3.8.2 -- Yes, .2 added for god knows what reason
  - release 1.1.testing -- fixing incorrect desktop icon placement

* Mon Nov 25 2019 Todd Warner <t0dd_at_protonmail.com> 3.3.8.1-0.1.testing.taw
  - 3.3.8.1 -- Yes, .1 added for god knows what reason

* Sun Sep 01 2019 Todd Warner <t0dd_at_protonmail.com> 3.3.8-0.1.testing.taw
  - 3.3.8
  - F30 version will not build because of a python3-trezor dependence build  
    failure.  
    See bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=1703628

* Fri Apr 26 2019 Todd Warner <t0dd_at_protonmail.com> 3.3.4-0.2.testing.taw
* Fri Apr 26 2019 Todd Warner <t0dd_at_protonmail.com> 3.3.4-0.1.testing.taw
  - 3.3.4
  - build section changes

* Thu Feb 21 2019 Todd Warner <t0dd_at_protonmail.com> 3.2.5-0.2.testing.taw
* Wed Feb 20 2019 Todd Warner <t0dd_at_protonmail.com> 3.2.5-0.1.testing.taw
  - 3.2.5

* Thu Jan 17 2019 Todd Warner <t0dd_at_protonmail.com> 3.2.4-0.1.testing.taw
  - 3.2.4

* Mon Oct 15 2018 Todd Warner <t0dd_at_protonmail.com> 3.2.3.1-0.1.testing.taw
  - 3.2.3.1
  - electrum-dash is now dash-electrum via upstream's change to  
    Dash Electrum/Dash-electrum
  - support for Tor proxy  
    https://github.com/akhavr/electrum-dash/releases/tag/3.2.3.1

* Wed Jul 04 2018 Todd Warner <t0dd_at_protonmail.com> 3.2.2.1-0.1.testing.taw
  - 3.2.2.1

* Wed Jul 04 2018 Todd Warner <t0dd_at_protonmail.com> 3.1.3-0.1.testing.taw
  - 3.1.3 (back to x.y.z and not x.y.z.zz)

* Thu Jun 21 2018 Todd Warner <t0dd_at_protonmail.com> 3.0.6.3-0.1.testing.taw
  - 3.0.6.3
  - adjustment to versioning expansion (x.y.z to x.y.z.zz)
  - some spec file tweaks

* Mon May 14 2018 Todd Warner <t0dd_at_protonmail.com> 3.0.6-0.3.testing.taw
  - Incorporates X11_hash testing fix:  
    https://github.com/akhavr/x11_hash/commit/23ca7f09d13945e5d95fa83b477baea0c6f7a1d8
  - Trezor still not showing up in list of plugins.

* Sat May 12 2018 Todd Warner <t0dd_at_protonmail.com> 3.0.6-0.2.testing.taw
  - Added script that places the data directory in a more linuxy place:  
    ~/.config/electrum-dash (versus the upstream default of ~/.electrum-dash

* Sat May 12 2018 Todd Warner <t0dd_at_protonmail.com> 3.0.6-0.1.testing.taw
  - 3.0.6
  - python3 and QT5 stuff and turn off automated byte-compiling of python
    since it is so error-prone:  
    https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation  
    https://fedoraproject.org/wiki/Packaging:Python_Appendix#Manual_byte_compilation
  - Added a whole pile of app icons (in -contrib tarball)
  - desktop-file-validate and appstream-util validate-relax added as is  
    required of desktop applications.
  - spec file change: mkdir -p instead of just mkdir, otherwise repeated  
    rpmbuilds without full cleanup will explode

* Fri May 4 2018 Todd Warner <t0dd_at_protonmail.com> 2.9.4-0.1.testing.taw
  - spec file change: update the desktop database upon post installation or  
    uninstallation
  
* Fri May 4 2018 Todd Warner <t0dd_at_protonmail.com> 2.9.4-0.1.testing.taw
  - Initial test build.
