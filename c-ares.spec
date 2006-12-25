Summary:	A library that performs asynchronous DNS operations
Summary(pl):	Biblioteka do wykonywania asynchronicznych zapytañ DNS
Name:		c-ares
Version:	1.3.2
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://daniel.haxx.se/projects/c-ares/%{name}-%{version}.tar.gz
# Source0-md5:	3f517655f22531889b2465219f4833fa
URL:		http://daniel.haxx.se/projects/c-ares/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
c-ares is a C library that performs DNS requests and name resolves
asynchronously. c-ares is a fork of the library named 'ares', written
by Greg Hudson at MIT.

%description -l pl
c-ares jest napisan± w C bibliotek± do asynchronicznego wykonywania
zapytañ DNS. c-ares jest to fork biblioteki 'ares' napisanej przez
Grega Hudsona w MIT.

%package devel
Summary:	Development files for c-ares library
Summary:	Pliki nag³ówkowe dla biblioteki c-ares
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for c-ares library.

%description devel -l pl
Pliki nag³ówkowe biblioteki c-ares.

%package static
Summary:	Static c-ares library
Summary(pl):	Statyczna biblioteka c-ares
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static c-ares library.

%description static -l pl
Statyczna biblioteka c-ares.

%prep
%setup -q

%build
%configure \
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
%attr(755,root,root) %{_libdir}/*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
