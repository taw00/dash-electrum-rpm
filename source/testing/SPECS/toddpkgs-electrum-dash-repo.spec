Name:		toddpkgs-electrum-dash-repo
Version:	1.0
Release:	0.1.testing%{?dist}.taw0
Summary:	Repository configuration to enable management of Dash Electrum packages

# Note, Group has been deprecated for years.
Group:		Unspecified
License:	MIT
URL:		https://github.com/taw00/electrum-dash-rpm
Source0:	https://raw.githubusercontent.com/taw00/electrum-dash-rpm/master/source/SOURCES/toddpkgs-electrum-dash-repo-1.0.tar.gz
BuildArch:	noarch
#BuildRequires:  tree

# CentOS/RHEL/EPEL can't do "Suggests:"
%if 0%{?fedora:1}
Suggests:	distribution-gpg-keys-copr
%endif


# pulled out of the description below...
#* For CentOS or RHEL:
#  sudo yum clean expire-cache
#  sudo yum install electrum-dash -y

%description
Todd (aka, taw, taw00, t0dd in various communities) packages applications for
Fedora Linux and RHEL/CentOS/EPEL. This package deploys the repository
configuration file necessary to enable on-going management of the Dash Electrum
cryptocurrency wallet RPM package for Fedora Linux (and perhaps, someday,
CentOS and RHEL).

Install this package, then...

* For fedora:
  sudo dnf install electrum-dash -y --refresh

You can edit /etc/yum.repos.d/electrum-dash.repo (as root) and 'enable=1' or '0'
whether you want the stable or the testing repositories.

Notes about GPG keys:
* An RPM signing key is included. It is used to sign RPMs that I build by
  hand. Namely any *.src.rpm found in github.com/taw00/electrum-dash-rpm
* RPMs from the copr repositories are signed by fedoraproject build system
  keys. Those keys are autoinstalled (with an "are you sure" dialogue).


%prep
%setup -q
# For debugging purposes...
#cd .. ; tree -df -L 1  ; cd -


%build
# no-op


%install
# Builds generically. Will need a disto specific RPM though.
install -d %{buildroot}%{_sysconfdir}/yum.repos.d
install -d %{buildroot}%{_sysconfdir}/pki/rpm-gpg

install -D -m644 todd-694673ED-public-2030-01-04.2016-11-07.asc %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-todd-694673ED-public

%if 0%{?fedora:1}
  install -D -m644 electrum-dash-fedora.repo %{buildroot}%{_sysconfdir}/yum.repos.d/electrum-dash.repo
%else
  %if 0%{?rhel:1}
  # no-op for now
  #install -D -m644 electrum-dash-epel.repo %%{buildroot}%%{_sysconfdir}/yum.repos.d/electrum-dash.repo
  %endif
%endif


%files
#%%config(noreplace) %%attr(644, root,root) %%{_sysconfdir}/yum.repos.d/electrum-dash.repo
%config %attr(644, root,root) %{_sysconfdir}/yum.repos.d/electrum-dash.repo
%attr(644, root,root) %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-todd-694673ED-public


%changelog
* Sun Apr 15 2018 Todd Warner <t0dd at protonmail.com> 1.0-0.1.testing.taw[n]
- Initial test build

