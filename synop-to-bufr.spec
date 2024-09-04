%define distnum %(/usr/lib/rpm/redhat/dist.sh --distnum)

%define PACKAGENAME synop-to-bufr
Name:           %{PACKAGENAME}
Version:        24.9.4
Release:        1%{dist}.fmi
Summary:        synop2bufr application
Group:          Applications/System
License:        MIT
URL:            http://www.fmi.fi
Source0: 	%{name}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       python3
Requires:       eccodes >= 2.33.0
Requires:       python3-numpy

Provides:	synop2bufr.py

AutoReqProv: no

%global debug_package %{nil}

%description
python tool to create BUFR files from ASCII files

%prep
%setup -q -n "%{PACKAGENAME}"

%build

%install
rm -rf $RPM_BUILD_ROOT
install -m 755 -d %{buildroot}/%{_bindir}
install -m 755 -d %{buildroot}/%{_libdir}/python3.6/site-packages/synop_to_bufr
cp -a *.py %{buildroot}/%{_libdir}/python3.6/site-packages/synop_to_bufr
ln -s %{_libdir}/python3.6/site-packages/synop_to_bufr/synop2bufr.py %{buildroot}/%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%{_libdir}/python3.6/site-packages/synop_to_bufr
%{_bindir}/synop2bufr.py

%changelog
* Wed Sep  4 2024 Tytti Mustonen <tytti.mustonen@fmi.fi> - 24.9.4-1.fmi
- New verion
* Wed Feb  2 2022 Mikko Partio <mikko.partio@fmi.fi> - 22.2.2-1.fmi
- Initial build
