Summary:	A library that performs asynchronous DNS operations
Summary(pl.UTF-8):	Biblioteka do wykonywania asynchronicznych zapytań DNS
Name:		c-ares
Version:	1.12.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://c-ares.haxx.se/download/%{name}-%{version}.tar.gz
# Source0-md5:	2ca44be1715cd2c5666a165d35788424
Patch0:		%{name}-resolv.conf-reading-is-not-fatal.patch
URL:		https://c-ares.haxx.se/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
c-ares is a C library that performs DNS requests and name resolves
asynchronously. c-ares is a fork of the library named 'ares', written
by Greg Hudson at MIT.

%description -l pl.UTF-8
c-ares jest napisaną w C biblioteką do asynchronicznego wykonywania
zapytań DNS. c-ares jest to fork biblioteki 'ares' napisanej przez
Grega Hudsona w MIT.

%package devel
Summary:	Development files for c-ares library
Summary(pl.UTF-8):	Pliki nagłówkowe dla biblioteki c-ares
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for c-ares library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki c-ares.

%package static
Summary:	Static c-ares library
Summary(pl.UTF-8):	Statyczna biblioteka c-ares
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static c-ares library.

%description static -l pl.UTF-8
Statyczna biblioteka c-ares.

%prep
%setup -q
%patch0 -p1

# we want our own debug flags, if any
%{__sed} -i -e 's/flags_dbg_off=".*"/flags_dbg_off="%{rpmcflags}"/' m4/cares-compilers.m4
%{__sed} -i -e 's/flags_opt_yes=".*"/flags_opt_yes="%{rpmcflags}"/' m4/cares-compilers.m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-optimize="%{rpmcflags}" \
	--enable-shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES LICENSE.md NEWS README.cares README.md RELEASE-NOTES TODO
%attr(755,root,root) %{_libdir}/libcares.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcares.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcares.so
%{_libdir}/libcares.la
%{_includedir}/ares.h
%{_includedir}/ares_build.h
%{_includedir}/ares_dns.h
%{_includedir}/ares_rules.h
%{_includedir}/ares_version.h
%{_mandir}/man3/ares_*.3*
%{_pkgconfigdir}/libcares.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcares.a
