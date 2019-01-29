# TODO
# - package apparmor stuff
# - update (cut down, include /usr/share/lxc/config/common.conf) default pld container config

# Conditional build:
%bcond_without	apparmor	# apparmor support
%bcond_without	seccomp		# SecComp syscall filter
%bcond_without	static		# static init.lxc variant
%bcond_with	selinux		# SELinux support
%bcond_with	cgmanager	# cgmanager support
%bcond_without	pam		# cgfs PAM module

Summary:	Linux Containers userspace tools
Summary(pl.UTF-8):	Narzędzia do kontenerów linuksowych (LXC)
Name:		lxc
Version:	3.0.3
Release:	1
License:	LGPL v2.1+
Group:		Applications/System
Source0:	https://linuxcontainers.org/downloads/lxc/%{name}-%{version}.tar.gz
# Source0-md5:	0aa1a982f7dfa4c7b8ce87b7047b0b6e
Source1:	%{name}-pld.in.sh
# lxc-net based on bridge, macvlan is an alternative/supported lxc network
Source2:	%{name}_macvlan.sysconfig
Source3:	%{name}_macvlan
Patch1:		%{name}-net.patch
Patch2:		x32.patch
URL:		https://www.linuxcontainers.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{?with_cgmanager:BuildRequires:	cgmanager-devel}
%{?with_cgmanager:BuildRequires:	dbus-devel >= 1.2.16}
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook2X >= 0.8
BuildRequires:	doxygen
BuildRequires:	gcc >= 6:4.7
%{?with_static:BuildRequires:	glibc-static}
BuildRequires:	gnutls-devel
%{?with_apparmor:BuildRequires:	libapparmor-devel}
BuildRequires:	libcap-devel
%{?with_static:BuildRequires:	libcap-static}
%{?with_cgmanager:BuildRequires:	libnih-devel >= 1.0.2}
%{?with_seccomp:BuildRequires:	libseccomp-devel}
BuildRequires:	libtool >= 2:2
BuildRequires:	libxslt-progs
%{?with_pam:BuildRequires:	pam-devel}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.671
BuildRequires:	sed >= 4.0
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
# lxc_macvlan script
Requires:	gawk
# used in lxc-net script to set bridge nat
Requires:	iproute2
Requires:	iptables
Requires:	rc-scripts >= 0.4.6
Requires:	systemd-units >= 38
Requires:	which
# used in lxc-net script, but not all cases, may break working setups
Suggests:	dnsmasq
Suggests:	gnupg
Suggests:	gnupg-plugin-keys_curl
Suggests:	gnupg-plugin-keys_hkp
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
w pełni funkcjonalne kontenery z izolacją/wirtualizacją pidów, ipc,
utsname, punktów montowania, /proc, /sys, sieci oraz uwzględniające
grupy kontrolne. Jest bardzo lekki, elastyczny i udostępnia narzędzia
do czynności związanych z kontenerami, takich jak monitorowanie z
asynchronicznym powiadamianiem o zdarzeniach czy zamrażanie. Ten
pakiet jest przydatny do tworzenia wirtualnych serwerów prywatnych
oraz uruchamiania izolowanych aplikacji, takich jak bash czy sshd.

%package -n pam-pam_cgfs
Summary:	PAM module to create user cgroups
Summary(pl.UTF-8):	Moduł PAM do tworzenia cgroup użytkownika
Group:		Libraries
Requires:	pam

%description -n pam-pam_cgfs
PAM module that when a user logs in, will create cgroups which the
user may administer.

%description -n pam-pam_cgfs -l pl.UTF-8
Moduł PAM, który przy logowaniu użytkownika tworzy cgroupy, którymi
użytkownik może administrować.

%package libs
Summary:	liblxc library
Summary(pl.UTF-8):	Biblioteka liblxc
Group:		Libraries
Conflicts:	lxc < 2.0.4-2

%description libs
liblxc library.

%description libs -l pl.UTF-8
Biblioteka liblxc.

%package devel
Summary:	Header files for lxc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki lxc
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for lxc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki lxc.

%package static
Summary:	Static lxc library
Summary(pl.UTF-8):	Statyczna biblioteka lxc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static lxc library.

%description static -l pl.UTF-8
Statyczna biblioteka lxc.

%package -n bash-completion-%{name}
Summary:	bash-completion for LXC
Summary(pl.UTF-8):	bashowe uzupełnianie nazw dla LXC
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n bash-completion-%{name}
bash-completion for LXC.

%description -n bash-completion-%{name} -l pl.UTF-8
bashowe uzupełnianie nazw dla LXC.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

cp -p %{SOURCE1} templates/lxc-pld.in

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	bashcompdir=%{bash_compdir} \
	db2xman=docbook2X2man \
	--disable-rpath \
	%{__enable_disable apparmor} \
	--enable-bash \
	%{__enable_disable cgmanager} \
	--enable-doc \
	--enable-examples \
	%{?with_pam:--enable-pam} \
	%{__enable_disable seccomp} \
	%{__enable_disable selinux} \
	--with-config-path=%{configpath} \
	--with-distro=pld \
	--with-init-script=sysvinit,systemd \
	--with-runtime-path=/var/run

%{__make}
%{__make} -C doc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{configpath},%{configpath}snap,/var/{cache,log}/lxc} \
        -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	SYSTEMD_UNIT_DIR=%{systemdunitdir} \
	pcdatadir=%{_pkgconfigdir} \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C doc install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblxc.la

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

# apparmor profiles are not packaged, remove to avoid packagers confusion
%{__rm} -r $RPM_BUILD_ROOT/etc/apparmor.d

# yum plugin, no idea where to package this
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/lxc-patch.py

install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/lxc_macvlan
install -p %{SOURCE3} $RPM_BUILD_ROOT%{_libexecdir}/%{name}/lxc_macvlan

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add lxc
/sbin/chkconfig --add lxc-net
%systemd_post lxc.service lxc-net.service

%preun
if [ "$1" = "0" ]; then
	%service lxc stop
	/sbin/chkconfig --del lxc
	%service lxc-net stop
	/sbin/chkconfig --del lxc-net
fi
%systemd_preun lxc.service lxc-net.service

%postun
%systemd_reload

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING MAINTAINERS README  doc/FAQ.txt doc/examples/*.conf
%attr(755,root,root) %{_bindir}/lxc-attach
%attr(755,root,root) %{_bindir}/lxc-autostart
%attr(755,root,root) %{_bindir}/lxc-cgroup
%attr(755,root,root) %{_bindir}/lxc-checkconfig
%attr(755,root,root) %{_bindir}/lxc-checkpoint
%attr(755,root,root) %{_bindir}/lxc-copy
%attr(755,root,root) %{_bindir}/lxc-config
%attr(755,root,root) %{_bindir}/lxc-console
%attr(755,root,root) %{_bindir}/lxc-create
%attr(755,root,root) %{_bindir}/lxc-destroy
%attr(755,root,root) %{_bindir}/lxc-device
%attr(755,root,root) %{_bindir}/lxc-execute
%attr(755,root,root) %{_bindir}/lxc-freeze
%attr(755,root,root) %{_bindir}/lxc-info
%attr(755,root,root) %{_bindir}/lxc-ls
%attr(755,root,root) %{_bindir}/lxc-monitor
%attr(755,root,root) %{_bindir}/lxc-snapshot
%attr(755,root,root) %{_bindir}/lxc-start
%attr(755,root,root) %{_bindir}/lxc-stop
%attr(755,root,root) %{_bindir}/lxc-top
%attr(755,root,root) %{_bindir}/lxc-unfreeze
%attr(755,root,root) %{_bindir}/lxc-unshare
%attr(755,root,root) %{_bindir}/lxc-update-config
%attr(755,root,root) %{_bindir}/lxc-usernsexec
%attr(755,root,root) %{_bindir}/lxc-wait
%attr(755,root,root) %{_sbindir}/init.lxc
%if %{with static}
%attr(755,root,root) %{_sbindir}/init.lxc.static
%endif
%attr(754,root,root) /etc/rc.d/init.d/lxc
%attr(754,root,root) /etc/rc.d/init.d/lxc-net

%{systemdunitdir}/lxc.service
%{systemdunitdir}/lxc@.service
%{systemdunitdir}/lxc-net.service
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/rootfs
%{_libdir}/%{name}/rootfs/README
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/%{name}
%endif
%attr(755,root,root) %{_libexecdir}/%{name}/lxc-apparmor-load
%attr(755,root,root) %{_libexecdir}/%{name}/lxc-containers
%attr(755,root,root) %{_libexecdir}/%{name}/lxc-monitord
%attr(755,root,root) %{_libexecdir}/%{name}/lxc-net
%attr(755,root,root) %{_libexecdir}/%{name}/lxc-user-nic
%attr(755,root,root) %{_libexecdir}/%{name}/lxc_macvlan
%dir %{_libexecdir}/%{name}/hooks
%attr(755,root,root) %{_libexecdir}/%{name}/hooks/unmount-namespace
%dir %{_sysconfdir}/lxc
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/lxc_macvlan
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/lxc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lxc/default.conf
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/lxc.functions
%dir %{_datadir}/%{name}/config
%{_datadir}/%{name}/config/common.conf
%dir %{_datadir}/%{name}/config/common.conf.d
%{_datadir}/%{name}/config/common.conf.d/README
%{_datadir}/%{name}/config/common.seccomp
%{_datadir}/%{name}/config/nesting.conf
%{_datadir}/%{name}/config/oci.common.conf
%{_datadir}/%{name}/config/userns.conf
%dir %{_datadir}/%{name}/hooks
%dir %{_datadir}/%{name}/selinux
%{_datadir}/%{name}/selinux/*
%dir %{_datadir}/%{name}/templates
%attr(755,root,root) %{_datadir}/%{name}/hooks/clonehostname
%attr(755,root,root) %{_datadir}/%{name}/hooks/dhclient
%attr(755,root,root) %{_datadir}/%{name}/hooks/dhclient-script
%attr(755,root,root) %{_datadir}/%{name}/hooks/mount*
%attr(755,root,root) %{_datadir}/%{name}/hooks/nvidia
%attr(755,root,root) %{_datadir}/%{name}/hooks/squid-deb-proxy-client
%attr(755,root,root) %{_datadir}/%{name}/hooks/ubuntu-cloud-prep
%attr(755,root,root) %{_datadir}/%{name}/templates/lxc-*
%{_mandir}/man1/lxc-attach.1*
%{_mandir}/man1/lxc-autostart.1*
%{_mandir}/man1/lxc-cgroup.1*
%{_mandir}/man1/lxc-checkconfig.1*
%{_mandir}/man1/lxc-checkpoint.1*
%{_mandir}/man1/lxc-copy.1*
%{_mandir}/man1/lxc-config.1*
%{_mandir}/man1/lxc-console.1*
%{_mandir}/man1/lxc-create.1*
%{_mandir}/man1/lxc-destroy.1*
%{_mandir}/man1/lxc-device.1*
%{_mandir}/man1/lxc-execute.1*
%{_mandir}/man1/lxc-freeze.1*
%{_mandir}/man1/lxc-info.1*
%{_mandir}/man1/lxc-ls.1*
%{_mandir}/man1/lxc-monitor.1*
%{_mandir}/man1/lxc-snapshot.1*
%{_mandir}/man1/lxc-start.1*
%{_mandir}/man1/lxc-stop.1*
%{_mandir}/man1/lxc-top.1*
%{_mandir}/man1/lxc-unfreeze.1*
%{_mandir}/man1/lxc-unshare.1*
%{_mandir}/man1/lxc-update-config.1*
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
%lang(ko) %{_mandir}/ko/man1/lxc*.1*
%lang(ko) %{_mandir}/ko/man5/lxc-usernet.5*
%lang(ko) %{_mandir}/ko/man5/lxc.conf.5*
%lang(ko) %{_mandir}/ko/man5/lxc.container.conf.5*
%lang(ko) %{_mandir}/ko/man5/lxc.system.conf.5*
%lang(ko) %{_mandir}/ko/man7/lxc.7*

%dir %{configpath}
%dir %{configpath}snap
%dir %attr(750,root,root) /var/log/lxc
%dir %attr(750,root,root) /var/cache/lxc

%if %{with pam}
%files -n pam-pam_cgfs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_cgfs.so
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblxc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblxc.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblxc.so
%{_includedir}/lxc
%{_pkgconfigdir}/lxc.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblxc.a

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/lxc
