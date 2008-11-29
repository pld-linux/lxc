# TODO: FHS (/var/lxc -> /var/lib/lxc)
Summary:	Linux Container Tools
Name:		lxc
Version:	0.4.0
Release:	1
License:	GPL
Group:		Base
Source0:	http://dl.sourceforge.net/lxc/%{name}-%{version}.tar.gz
# Source0-md5:	327f0e700858ab5b916aa36517680256
URL:		http://sourceforge.net/projects/lxc
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package static
Summary:	Static lxc library
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static lxc library.

%prep
%setup -q
sed -i -e 's#^lxcpath=.*#lxcpath=/var/lxc#g' src/lxc/Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/lxc

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README etc/*.conf etc/*-config
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/liblxc-*.so
%dir %{_sysconfdir}/lxc
%dir /var/lxc

%files devel
%defattr(644,root,root,755)
%{_includedir}/lxc
%attr(755,root,root) %{_libdir}/liblxc.so
%{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
