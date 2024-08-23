#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	A library that performs asynchronous DNS operations
Summary(pl.UTF-8):	Biblioteka do wykonywania asynchronicznych zapytań DNS
Name:		c-ares
Version:	1.33.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://c-ares.org/download/
Source0:	https://github.com/c-ares/c-ares/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f9f2ff0c63ddec8ea17989ca5992848d
Patch0:		%{name}-resolv.conf-reading-is-not-fatal.patch
URL:		https://c-ares.org/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.9.6
# for tests
#BuildRequires:	gmock-devel
#BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libtool >= 2:2
BuildRequires:	rpmbuild(macros) >= 1.527
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

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{__enable_disable static_libs static} \
	--disable-tests \
	--enable-shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no external dependencies + obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcares.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE.md README.md RELEASE-NOTES.md SECURITY.md
%attr(755,root,root) %{_libdir}/libcares.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcares.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcares.so
%{_includedir}/ares.h
%{_includedir}/ares_build.h
%{_includedir}/ares_dns.h
%{_includedir}/ares_dns_record.h
%{_includedir}/ares_nameser.h
%{_includedir}/ares_version.h
%{_mandir}/man3/ares_*.3*
%{_pkgconfigdir}/libcares.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcares.a
%endif
