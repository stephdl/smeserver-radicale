%define name smeserver-roundcube
%define version 0.0.1
%define release 1

Summary: smserver rpm to setup radicale, a carddav and caldav client
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Source: %{name}-%{version}.tar.gz
License: GNU GPL version 2
URL: http://www.contribs.org
Group: SMEserver/addon
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildArchitectures: noarch
BuildRequires: e-smith-devtools
Requires: e-smith-release >= 9.0
Requires: python-pip
AutoReqProv: no

%description
smserver rpm to setup the roundcube IMAP mail client.

%changelog
* Thu Oct 1 2015 stephane de labrusse <stephdl@de-labrusse.fr> 0.0.1-1
- First release

%prep
%setup


%build
perl createlinks
%{__mkdir_p} root/home/e-smith/files/.radicale/collections

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-filelist
/sbin/e-smith/genfilelist \
   --dir /home/e-smith/files/.radicale/collections 'attr(0755,radicale,radicale)' \
$RPM_BUILD_ROOT > %{name}-%{version}-filelist
echo "%doc COPYING"  >> %{name}-%{version}-filelist

%clean
cd ..
rm -rf %{name}-%{version}

%pre

echo "### Radicale Installation"
pip install --upgrade radicale 2>&1 1>/dev/null

%preun

%post
chkconfig --add radicaled  2>&1 1>/dev/null
/sbin/e-smith/create-system-user radicale 911 "Radicale server" /home/e-smith/files/.radicale/ /bin/false

%postun

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
