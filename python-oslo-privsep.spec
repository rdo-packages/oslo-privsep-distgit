# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name oslo.privsep
%global pkgname oslo-privsep

%global with_doc 1

%global common_desc OpenStack library for privilege separation

Name:           python-%{pkgname}
Version:        1.33.3
Release:        1%{?dist}
Summary:        OpenStack library for privilege separation

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git


%description
%{common_desc}

%package -n     python%{pyver}-%{pkgname}
Summary:        OpenStack library for privilege separation
%{?python_provide:%python_provide python%{pyver}-%{pkgname}}
%if %{pyver} == 3
Obsoletes: python2-%{pkgname} < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr >= 1.8
BuildRequires:  python%{pyver}-babel >= 1.3
BuildRequires:  python%{pyver}-oslo-log >= 3.36.0
BuildRequires:  python%{pyver}-oslo-i18n >= 3.15.3
BuildRequires:  python%{pyver}-oslo-config >= 2:5.2.0
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-oslo-utils >= 3.33.0
BuildRequires:  python%{pyver}-eventlet
BuildRequires:  python%{pyver}-greenlet
BuildRequires:  python%{pyver}-cffi
BuildRequires:  python%{pyver}-msgpack >= 0.5.0
Requires:       python%{pyver}-babel >= 1.3
Requires:       python%{pyver}-eventlet >= 0.18.2
Requires:       python%{pyver}-greenlet >= 0.4.10
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-cffi
Requires:       python%{pyver}-msgpack >= 0.5.0
Requires:       python-%{pkgname}-lang = %{version}-%{release}

# Handle python2 exception
%if %{pyver} == 2
Requires:       python-enum34
Requires:       python2-futures
BuildRequires:  python2-futures
%endif

%description -n python%{pyver}-%{pkgname}
%{common_desc}


%package -n     python%{pyver}-%{pkgname}-tests
Summary:        OpenStack library for privilege separation tests
Requires:       python%{pyver}-%{pkgname}

%description -n python%{pyver}-%{pkgname}-tests
%{common_desc}

This package contains the test files.

%if 0%{?with_doc}
%package -n python-%{pkgname}-doc
Summary:        oslo.privsep documentation
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-sphinxcontrib-apidoc
BuildRequires:  python%{pyver}-openstackdocstheme
# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-enum34
%endif

%description -n python-%{pkgname}-doc
Documentation for oslo.privsep
%endif


%package  -n python-%{pkgname}-lang
Summary:   Translation files for Oslo privsep library

%description -n python-%{pkgname}-lang
Translation files for Oslo privsep library


%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
rm -rf {,test-}requirements.txt

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
# NOTE(jpena): we can re-enable warnings-as-failures once
# https://review.opendev.org/669444 is in a tagged release
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/oslo_privsep/locale

%install
%{pyver_install}

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{pyver_sitelib}/oslo_privsep/locale/*/LC_*/oslo_privsep*po
rm -f %{buildroot}%{pyver_sitelib}/oslo_privsep/locale/*pot
mv %{buildroot}%{pyver_sitelib}/oslo_privsep/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_privsep --all-name

%check
%{pyver_bin} setup.py test ||:


%files -n python%{pyver}-%{pkgname}
%doc README.rst
%{pyver_sitelib}/oslo_privsep
%{pyver_sitelib}/%{pypi_name}-*-py?.?.egg-info
%exclude %{pyver_sitelib}/oslo_privsep/tests
%{_bindir}/privsep-helper


%files -n python%{pyver}-%{pkgname}-tests
%{pyver_sitelib}/oslo_privsep/tests

%if 0%{?with_doc}
%files -n python-%{pkgname}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python-%{pkgname}-lang -f oslo_privsep.lang
%license LICENSE

%changelog
* Tue Sep 17 2019 RDO <dev@lists.rdoproject.org> 1.33.3-1
- Update to 1.33.3

