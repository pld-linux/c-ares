Summary:	A library that performs asynchronous DNS operations
Summary(pl.UTF-8):	Biblioteka do wykonywania asynchronicznych zapytań DNS
Name:		c-ares
Version:	1.6.0
Release:	2
License:	MIT
Group:		Libraries
Source0:	http://daniel.haxx.se/projects/c-ares/%{name}-%{version}.tar.gz
# Source0-md5:	4503b0db3dd79d3c1f58d87722dbab46
Patch0:		%{name}-resolv.conf-reading-is-not-fatal.patch
URL:		http://daniel.haxx.se/projects/c-ares/
BuildRequires:	autoconf
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
sed -i -e 's/flags_dbg_off=".*"/flags_dbg_off="%{rpmcflags}"/' m4/cares-compilers.m4
sed -i -e 's/flags_opt_yes=".*"/flags_opt_yes="%{rpmcflags}"/' m4/cares-compilers.m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
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
%doc README README.cares CHANGES NEWS
%attr(755,root,root) %{_libdir}/libcares.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcares.so.2

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcares.so
%{_libdir}/libcares.la
%{_includedir}/ares*.h
%{_mandir}/man3/ares_*.3*
%{_pkgconfigdir}/libcares.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcares.a
