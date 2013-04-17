# TODO: move lua/python-dependent utils to lya-/python-
#
# Conditional build:
%bcond_without	seccomp	# SecComp syscall filter
%bcond_without	lua	# Lua binding
%bcond_without	python	# Python binding
#
Summary:	Linux Container Tools
Summary(pl.UTF-8):	Narzędzia do kontenerów linuksowych (LXC)
Name:		lxc
Version:	0.9.0
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://lxc.sourceforge.net/download/lxc/%{name}-%{version}.tar.gz
# Source0-md5:	8552a4479090616f4bc04d8473765fc9
Patch0:		%{name}-devpts.patch
Patch1:		%{name}-pld.patch
URL:		http://lxc.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	docbook2X
BuildRequires:	docbook-dtd30-sgml
BuildRequires:	docbook-utils
BuildRequires:	libapparmor-devel
BuildRequires:	libcap-devel
%{?with_seccomp:BuildRequires:	libseccomp-devel}
%{?with_lua:BuildRequires:	lua51-devel >= 5.1}
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python3-devel >= 3.2}
BuildRequires:	rpmbuild(macros) >= 1.612
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

%build
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	db2xman=docbook2X2man \
	--disable-rpath \
	--enable-doc \
	%{?with_lua:--enable-lua} \
	%{?with_python:--enable-python} \
	%{?with_seccomp:--enable-seccomp} \
	--with-config-path=%{configpath} \
	--with-distro=pld

%{__make}
%{__make} -C doc

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pcdatadir=%{_pkgconfigdir}

%{__make} -C doc install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/doc

install -d $RPM_BUILD_ROOT%{configpath}

%if %{with python}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}/lxc
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}/lxc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog CONTRIBUTING MAINTAINERS README TODO doc/FAQ.txt doc/examples/*.conf
%attr(755,root,root) %{_bindir}/lxc-*
%attr(755,root,root) %{_libdir}/liblxc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblxc.so.0
%dir %{configpath}
%dir %{_libdir}/lxc
%dir %{_libdir}/lxc/rootfs
%{_libdir}/lxc/rootfs/README
%attr(755,root,root) %{_libdir}/lxc/lxc-init
%dir %{_sysconfdir}/lxc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lxc/default.conf
%{_datadir}/lxc
%{_mandir}/man1/lxc-*.1*
%{_mandir}/man5/lxc.conf.5*
%{_mandir}/man7/lxc.7*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblxc.so
%{_includedir}/lxc
%{_pkgconfigdir}/lxc.pc

%if %{with lua}
%files -n lua-lxc
%defattr(644,root,root,755)
%dir %{_libdir}/lua/5.1/lxc
%attr(755,root,root) %{_libdir}/lua/5.1/lxc/core.so
%{_datadir}/lua/5.1/lxc.lua
%endif

%if %{with python}
%files -n python3-lxc
%defattr(644,root,root,755)
%{py3_sitedir}/lxc
%attr(755,root,root) %{py3_sitedir}/_lxc.cpython-*.so
%{py3_sitedir}/_lxc-0.1-py*.egg-info
%endif
