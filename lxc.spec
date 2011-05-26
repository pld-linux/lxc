Summary:	Linux Container Tools
Name:		lxc
Version:	0.7.4.2
Release:	1
License:	GPL
Group:		Base
Source0:	http://lxc.sourceforge.net/download/lxc/%{name}-%{version}.tar.gz
# Source0-md5:	36fcb0f6a39d2f55130421f342f24ef3
URL:		http://lxc.sourceforge.net
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	docbook-dtd30-sgml
BuildRequires:	docbook-utils
BuildRequires:	libcap-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		configpath	/var/lib/lxc

%description
Tools to create and manage containers. It contains a full featured
container with the isolation / virtualization of the pids, the ipc,
the utsname, the mount points, /proc, /sys, the network and it takes
into account the control groups. It is very light, flexible, and
provides a set of tools around the container like the monitoring with
asynchronous events notification, or the freeze of the container. This
package is useful to create Virtual Private Server, or to run isolated
applications like bash or sshd.

%package devel
Summary:	Header files and develpment documentation for lxc
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
lxc development files.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__automake}
%configure \
	--with-config-path=%{configpath}

%{__make}
%{__make} -C doc

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pcdatadir=%{_pkgconfigdir}
%{__make} -C doc install \
	DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc

install -d $RPM_BUILD_ROOT%{configpath}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog CONTRIBUTING MAINTAINERS README TODO doc/FAQ.txt doc/examples/*.conf 
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/liblxc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblxc.so.0
%{_libdir}/lxc/rootfs/README
%{_mandir}/man?/lxc*
%dir %{configpath}
%dir %{_libdir}/lxc
%dir %{_libdir}/lxc/templates
%dir %{_libdir}/lxc/rootfs
%attr(755,root,root) %{_libdir}/lxc/lxc-init
%attr(755,root,root) %{_libdir}/lxc/templates/lxc-*

%files devel
%defattr(644,root,root,755)
%{_includedir}/lxc
%attr(755,root,root) %{_libdir}/liblxc.so
%{_pkgconfigdir}/lxc.pc
