# TODO
# - package apparmor stuff

# Conditional build:
%bcond_without	seccomp	# SecComp syscall filter
%bcond_without	apparmor	# apparmor
%bcond_without	lua	# Lua binding
%bcond_without	python	# Python binding
%bcond_with	selinux	# SELinux
%bcond_with	cgmanager	# Enable cgmanager (BR: libcgmanager, libnih >= 1.0.2, libnih-dbus >= 1.0.0, dbus-1 >= 1.2.16)

Summary:	Linux Containers userspace tools
Summary(pl.UTF-8):	Narzędzia do kontenerów linuksowych (LXC)
Name:		lxc
Version:	1.0.7
Release:	3
License:	LGPL v2.1+
Group:		Applications/System
Source0:	https://www.linuxcontainers.org/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	b48f468a9bef0e4e140dd723f0a65ad0
Source1:	%{name}-pld.in.sh
Source2:	%{name}.init
Source3:	%{name}_macvlan.init
Source4:	%{name}_macvlan.sysconfig
Patch1:		%{name}-pld.patch
URL:		https://www.linuxcontainers.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	docbook-dtd30-sgml
BuildRequires:	docbook-utils
BuildRequires:	docbook2X
BuildRequires:	gnutls-devel
%{?with_apparmor:BuildRequires:	libapparmor-devel}
BuildRequires:	libcap-devel
%{?with_seccomp:BuildRequires:	libseccomp-devel}
BuildRequires:	libxslt-progs
%{?with_lua:BuildRequires:	lua51-devel >= 5.1}
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python3-devel >= 3.2}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.612
BuildRequires:	sed >= 4.0
Requires:	rc-scripts >= 0.4.6
Requires:	which
Requires:	iproute2
Requires(post,preun):	/sbin/chkconfig
Requires(post):	/sbin/ldconfig
Suggests:	gnupg
Suggests:	gnupg-plugin-keys_curl
Suggests:	gnupg-plugin-keys_hkp
Suggests:	net-tools
Suggests:	python3-lxc
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
Requires:	python3-modules

%description -n python3-lxc
Python (3.x) binding for LXC.

%description -n python3-lxc -l pl.UTF-8
Wiązanie Pythona (3.x) do LXC.

%package -n bash-completion-%{name}
Summary:	bash-completion for LXC
Summary(pl.UTF-8):	bashowe uzupełnianie nazw dla LXC
Group:		Applications/Shells
Requires:	%{name}
Requires:	bash-completion

%description -n bash-completion-%{name}
bash-completion for LXC.

%description -n bash-completion-%{name} -l pl.UTF-8
bashowe uzupełnianie nazw dla LXC.

%prep
%setup -q
%patch1 -p1

cp -p %{SOURCE1} templates/lxc-pld.in

%build
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	db2xman=docbook2X2man \
	--disable-rpath \
	--enable-bash \
	--enable-doc \
	--enable-examples \
	%{__enable_disable apparmor} \
	%{__enable_disable lua} %{?with_lua:--with-lua-pc=lua51} \
	%{__enable_disable python} \
	%{__enable_disable seccomp} \
	%{__enable_disable selinux} \
	--with-config-path=%{configpath} \
	--with-init-script=sysvinit,systemd \
	--with-runtime-path=/var/run \
	--with-distro=pld

%{__make}
%{__make} -C doc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{configpath},%{configpath}snap,/var/{cache,log}/lxc}  \
        -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	SYSTEMD_UNIT_DIR=%{systemdunitdir} \
	pcdatadir=%{_pkgconfigdir} \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C doc install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

# apparmor profiles are not packaged, remove to avoid packagers confusion
%{__rm} -r $RPM_BUILD_ROOT/etc/apparmor.d

# yum plugin, no idea where to package this
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/lxc-patch.py

install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/lxc
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/lxc_macvlan
install -p %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/lxc_macvlan

%if %{with python}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}/lxc
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}/lxc
%endif
%if %{with lua}
%{__sed} -i -e '1s,#!/usr/bin/env lua,#!/usr/bin/lua5.1,' $RPM_BUILD_ROOT%{_bindir}/lxc-top
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	
/sbin/ldconfig
/sbin/chkconfig --add lxc
/sbin/chkconfig --add lxc_macvlan

%preun
if [ "$1" = "0" ]; then
	%service lxc stop
	/sbin/chkconfig --del lxc
	%service lxc_macvlan stop
	/sbin/chkconfig --del lxc_macvlan
fi

%postun	-p /sbin/ldconfig


%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING MAINTAINERS README  doc/FAQ.txt doc/examples/*.conf
%attr(755,root,root) %{_bindir}/lxc-attach
%attr(755,root,root) %{_bindir}/lxc-autostart
%attr(755,root,root) %{_bindir}/lxc-cgroup
%attr(755,root,root) %{_bindir}/lxc-checkconfig
%attr(755,root,root) %{_bindir}/lxc-clone
%attr(755,root,root) %{_bindir}/lxc-config
%attr(755,root,root) %{_bindir}/lxc-console
%attr(755,root,root) %{_bindir}/lxc-create
%attr(755,root,root) %{_bindir}/lxc-destroy
%attr(755,root,root) %{_bindir}/lxc-execute
%attr(755,root,root) %{_bindir}/lxc-freeze
%attr(755,root,root) %{_bindir}/lxc-info
%attr(755,root,root) %{_bindir}/lxc-monitor
%attr(755,root,root) %{_bindir}/lxc-snapshot
%attr(755,root,root) %{_bindir}/lxc-start
%attr(755,root,root) %{_bindir}/lxc-stop
%attr(755,root,root) %{_bindir}/lxc-unfreeze
%attr(755,root,root) %{_bindir}/lxc-unshare
%attr(755,root,root) %{_bindir}/lxc-usernsexec
%attr(755,root,root) %{_bindir}/lxc-wait
%attr(755,root,root) %{_sbindir}/init.lxc
%attr(755,root,root) %{_libdir}/liblxc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblxc.so.1
%attr(754,root,root) /etc/rc.d/init.d/lxc
%attr(754,root,root) /etc/rc.d/init.d/lxc_macvlan

%{systemdunitdir}/lxc.service
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/rootfs
%{_libdir}/%{name}/rootfs/README
%attr(755,root,root) %{_libdir}/%{name}/lxc-devsetup
%attr(755,root,root) %{_libdir}/%{name}/lxc-monitord
%attr(755,root,root) %{_libdir}/%{name}/lxc-user-nic
%attr(755,root,root) %{_libdir}/%{name}/lxc-autostart-helper
%dir %{_sysconfdir}/lxc
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/lxc_macvlan
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lxc/default.conf
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/lxc.functions
%dir %{_datadir}/%{name}/config
%{_datadir}/%{name}/config/centos.*.conf
%{_datadir}/%{name}/config/common.seccomp
%{_datadir}/%{name}/config/debian.*.conf
%{_datadir}/%{name}/config/fedora.*.conf
%{_datadir}/%{name}/config/gentoo.*.conf
%{_datadir}/%{name}/config/oracle.*.conf
%{_datadir}/%{name}/config/plamo.*.conf
%{_datadir}/%{name}/config/ubuntu-cloud.*.conf
%{_datadir}/%{name}/config/ubuntu.*.conf
%dir %{_datadir}/%{name}/hooks
%dir %{_datadir}/%{name}/templates
%attr(755,root,root) %{_datadir}/%{name}/hooks/clonehostname
%attr(755,root,root) %{_datadir}/%{name}/hooks/mount*
%attr(755,root,root) %{_datadir}/%{name}/hooks/squid-deb-proxy-client
%attr(755,root,root) %{_datadir}/%{name}/hooks/ubuntu-cloud-prep
%attr(755,root,root) %{_datadir}/%{name}/templates/lxc-*
%{_mandir}/man1/lxc-attach.1*
%{_mandir}/man1/lxc-autostart.1*
%{_mandir}/man1/lxc-cgroup.1*
%{_mandir}/man1/lxc-checkconfig.1*
%{_mandir}/man1/lxc-clone.1*
%{_mandir}/man1/lxc-config.1*
%{_mandir}/man1/lxc-console.1*
%{_mandir}/man1/lxc-create.1*
%{_mandir}/man1/lxc-destroy.1*
%{_mandir}/man1/lxc-execute.1*
%{_mandir}/man1/lxc-freeze.1*
%{_mandir}/man1/lxc-info.1*
%{_mandir}/man1/lxc-monitor.1*
%{_mandir}/man1/lxc-snapshot.1*
%{_mandir}/man1/lxc-start.1*
%{_mandir}/man1/lxc-stop.1*
%{_mandir}/man1/lxc-unfreeze.1*
%{_mandir}/man1/lxc-unshare.1*
%{_mandir}/man1/lxc-user-nic.1*
%{_mandir}/man1/lxc-usernsexec.1*
%{_mandir}/man1/lxc-wait.1*
%{_mandir}/man5/lxc-usernet.5*
%{_mandir}/man5/lxc.conf.5*
%{_mandir}/man5/lxc.container.conf.5*
%{_mandir}/man5/lxc.system.conf.5*
%{_mandir}/man7/lxc.7*
%lang(ja) %{_mandir}/ja/man1/lxc*.1*
%lang(ja) %{_mandir}/ja/man5/lxc-usernet.5*
%lang(ja) %{_mandir}/ja/man5/lxc.conf.5*
%lang(ja) %{_mandir}/ja/man5/lxc.container.conf.5*
%lang(ja) %{_mandir}/ja/man5/lxc.system.conf.5*
%lang(ja) %{_mandir}/ja/man7/lxc.7*
%exclude %{_mandir}/ja/man1/lxc-device.1*
%exclude %{_mandir}/ja/man1/lxc-ls.1*
%exclude %{_mandir}/ja/man1/lxc-start-ephemeral.1*
%exclude %{_mandir}/ja/man1/lxc-top.1*


%if %{without python}
# legacy version
%attr(755,root,root) %{_bindir}/lxc-ls
%{_mandir}/man1/lxc-ls.1*
%endif

%dir %{configpath}
%dir %{configpath}snap
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
%dir %{_libdir}/lua/lxc
%attr(755,root,root) %{_libdir}/lua/lxc/core.so
%{_datadir}/lua/lxc.lua
%{_mandir}/man1/lxc-top.1*
%lang(ja) %{_mandir}/ja/man1/lxc-top.1*
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
%lang(ja) %{_mandir}/ja/man1/lxc-device.1*
%lang(ja) %{_mandir}/ja/man1/lxc-ls.1*
%lang(ja) %{_mandir}/ja/man1/lxc-start-ephemeral.1*
%endif

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/lxc
