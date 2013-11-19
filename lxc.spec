#
# Conditional build:
%bcond_without	seccomp	# SecComp syscall filter
%bcond_without	apparmor	# apparmor
%bcond_without	lua	# Lua binding
%bcond_without	python	# Python binding

Summary:	Linux Container Tools
Summary(pl.UTF-8):	Narzędzia do kontenerów linuksowych (LXC)
Name:		lxc
Version:	0.9.0
Release:	6
License:	LGPL v2.1+
Group:		Applications/System
Source0:	http://lxc.sourceforge.net/download/lxc/%{name}-%{version}.tar.gz
# Source0-md5:	8552a4479090616f4bc04d8473765fc9
Source1:	%{name}-pld.in.sh
Patch0:		%{name}-devpts.patch
Patch1:		%{name}-pld.patch
Patch2:		am-1.14.patch
Patch3:		checkconfig-module.patch
Patch4:		checkconfig-vserver-config.patch
Patch5:		fedora-template.patch
URL:		http://lxc.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	docbook-dtd30-sgml
BuildRequires:	docbook-utils
BuildRequires:	docbook2X
%{?with_apparmor:BuildRequires:	libapparmor-devel}
BuildRequires:	libcap-devel
%{?with_seccomp:BuildRequires:	libseccomp-devel}
%{?with_lua:BuildRequires:	lua51-devel >= 5.1}
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python3-devel >= 3.2}
BuildRequires:	rpmbuild(macros) >= 1.612
BuildRequires:	sed >= 4.0
Requires:	rc-scripts >= 0.4.6
Requires:	which
Suggests:	net-tools
Suggests:	rsync
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

%description -l pl.UTF-8
Narzędzia do tworzenia i zarządzania kontenerami. System ten obejmuje
w pełni funkcjonalne kontenery z ilozacją/wirtualizacją pidów, ipc,
utsname, punktów montowania, /proc, /sys, sieci oraz uwzględniające
grupy kontrolne. Jest bardzo lekki, elastyczny i udostępnia narzędzia
do czynności związanych z kontenerami, takich jak monitorowanie z
asynchronicznym powiadamianiem o zdarzeniach czy zamrażanie. Ten
pakiet jest przydatny do tworzenia wirtualnych serwerów prywatnych
oraz uruchamiania izolowanych aplikacji, takich jak bash czy sshd.

%package devel
Summary:	Header files for lxc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki lxc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for lxc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki lxc.

%package -n lua-lxc
Summary:	Lua binding for LXC
Summary(pl.UTF-8):	Wiązanie Lua do LXC
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	lua51-libs >= 5.1

%description -n lua-lxc
Lua binding for LXC.

%description -n lua-lxc -l pl.UTF-8
Wiązanie Lua do LXC.

%package -n python3-lxc
Summary:	Python (3.x) binding for LXC
Summary(pl.UTF-8):	Wiązanie Pythona (3.x) do LXC
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python3-libs >= 3.2

%description -n python3-lxc
Python (3.x) binding for LXC.

%description -n python3-lxc -l pl.UTF-8
Wiązanie Pythona (3.x) do LXC.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

cp -p %{SOURCE1} templates/lxc-pld.in

%build
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	db2xman=docbook2X2man \
	--disable-rpath \
	--enable-doc \
	%{__enable_disable apparmor} \
	%{__enable_disable lua} \
	%{__enable_disable python} \
	%{__enable_disable seccomp} \
	--with-config-path=%{configpath} \
	--with-distro=pld

%{__make}
%{__make} -C doc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{configpath},/var/{cache,log}/lxc}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pcdatadir=%{_pkgconfigdir}

%{__make} -C doc install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%if %{with python}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}/lxc
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}/lxc
%endif
%if %{with lua}
%{__sed} -i -e '1s,#!/usr/bin/env lua,#!/usr/bin/lua51,' $RPM_BUILD_ROOT%{_bindir}/lxc-top
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog CONTRIBUTING MAINTAINERS README TODO doc/FAQ.txt doc/examples/*.conf
%attr(755,root,root) %{_bindir}/lxc-attach
%attr(755,root,root) %{_bindir}/lxc-cgroup
%attr(755,root,root) %{_bindir}/lxc-checkconfig
%attr(755,root,root) %{_bindir}/lxc-checkpoint
%attr(755,root,root) %{_bindir}/lxc-clone
%attr(755,root,root) %{_bindir}/lxc-console
%attr(755,root,root) %{_bindir}/lxc-create
%attr(755,root,root) %{_bindir}/lxc-destroy
%attr(755,root,root) %{_bindir}/lxc-execute
%attr(755,root,root) %{_bindir}/lxc-freeze
%attr(755,root,root) %{_bindir}/lxc-info
%attr(755,root,root) %{_bindir}/lxc-kill
%attr(755,root,root) %{_bindir}/lxc-monitor
%attr(755,root,root) %{_bindir}/lxc-netstat
%attr(755,root,root) %{_bindir}/lxc-ps
%attr(755,root,root) %{_bindir}/lxc-restart
%attr(755,root,root) %{_bindir}/lxc-shutdown
%attr(755,root,root) %{_bindir}/lxc-start
%attr(755,root,root) %{_bindir}/lxc-stop
%attr(755,root,root) %{_bindir}/lxc-unfreeze
%attr(755,root,root) %{_bindir}/lxc-unshare
%attr(755,root,root) %{_bindir}/lxc-version
%attr(755,root,root) %{_bindir}/lxc-wait
%attr(755,root,root) %{_libdir}/liblxc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblxc.so.0
%dir %{_libdir}/lxc
%dir %{_libdir}/lxc/rootfs
%{_libdir}/lxc/rootfs/README
%attr(755,root,root) %{_libdir}/lxc/lxc-init
%dir %{_sysconfdir}/lxc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lxc/default.conf
%dir %{_datadir}/lxc
%{_datadir}/%{name}/lxc.functions
%dir %{_datadir}/%{name}/hooks
%dir %{_datadir}/%{name}/templates
%attr(755,root,root) %{_datadir}/%{name}/hooks/mount*
%attr(755,root,root) %{_datadir}/%{name}/templates/lxc-*
%{_mandir}/man1/lxc-attach.1*
%{_mandir}/man1/lxc-cgroup.1*
%{_mandir}/man1/lxc-checkconfig.1*
%{_mandir}/man1/lxc-checkpoint.1*
%{_mandir}/man1/lxc-clone.1*
%{_mandir}/man1/lxc-console.1*
%{_mandir}/man1/lxc-create.1*
%{_mandir}/man1/lxc-destroy.1*
%{_mandir}/man1/lxc-execute.1*
%{_mandir}/man1/lxc-freeze.1*
%{_mandir}/man1/lxc-info.1*
%{_mandir}/man1/lxc-kill.1*
%{_mandir}/man1/lxc-monitor.1*
%{_mandir}/man1/lxc-netstat.1*
%{_mandir}/man1/lxc-ps.1*
%{_mandir}/man1/lxc-restart.1*
%{_mandir}/man1/lxc-shutdown.1*
%{_mandir}/man1/lxc-start.1*
%{_mandir}/man1/lxc-stop.1*
%{_mandir}/man1/lxc-unfreeze.1*
%{_mandir}/man1/lxc-unshare.1*
%{_mandir}/man1/lxc-version.1*
%{_mandir}/man1/lxc-wait.1*
%{_mandir}/man5/lxc.conf.5*
%{_mandir}/man7/lxc.7*
%if %{without python}
# legacy version
%attr(755,root,root) %{_bindir}/lxc-ls
%{_mandir}/man1/lxc-ls.1*
%endif

%dir %{configpath}
%dir %attr(750,root,root) /var/log/lxc
%dir %attr(750,root,root) /var/cache/lxc

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblxc.so
%{_includedir}/lxc
%{_pkgconfigdir}/lxc.pc

%if %{with lua}
%files -n lua-lxc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lxc-top
%dir %{_libdir}/lua/5.1/lxc
%attr(755,root,root) %{_libdir}/lua/5.1/lxc/core.so
%{_datadir}/lua/5.1/lxc.lua
%{_mandir}/man1/lxc-top.1*
%endif

%if %{with python}
%files -n python3-lxc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lxc-device
%attr(755,root,root) %{_bindir}/lxc-ls
%attr(755,root,root) %{_bindir}/lxc-start-ephemeral
%{py3_sitedir}/lxc
%attr(755,root,root) %{py3_sitedir}/_lxc.cpython-*.so
%{py3_sitedir}/_lxc-0.1-py*.egg-info
%{_mandir}/man1/lxc-device.1*
%{_mandir}/man1/lxc-ls.1*
%{_mandir}/man1/lxc-start-ephemeral.1*
%endif
