%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global pypi_name oslo.privsep
%global pkgname oslo-privsep

%global common_desc OpenStack library for privilege separation

Name:           python-%{pkgname}
Version:        XXX
Release:        XXX
Summary:        OpenStack library for privilege separation

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git



%description
%{common_desc}


%package -n     python2-%{pkgname}
Summary:        OpenStack library for privilege separation
%{?python_provide:%python_provide python2-%{pkgname}}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr >= 1.8
BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-babel >= 1.3
BuildRequires:  python2-oslo-log >= 3.36.0
BuildRequires:  python2-oslo-i18n >= 3.15.3
BuildRequires:  python2-oslo-config >= 2:5.2.0
BuildRequires:  python2-oslotest
BuildRequires:  python2-oslo-utils >= 3.33.0
BuildRequires:  python2-eventlet
BuildRequires:  python2-greenlet
%if 0%{?fedora} > 0
BuildRequires:  python2-cffi
BuildRequires:  python2-msgpack >= 0.5.0
%else
BuildRequires:  python-cffi
BuildRequires:  python-msgpack >= 0.5.0
%endif

Requires:       python2-babel >= 1.3
Requires:       python2-eventlet >= 0.18.2
Requires:       python2-greenlet >= 0.4.10
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-config >= 2:5.2.0
Requires:       python2-oslo-utils >= 3.33.0
%if 0%{?fedora} > 0
Requires:       python2-enum34
Requires:       python2-cffi
Requires:       python2-msgpack >= 0.5.0
%else
Requires:       python-enum34
Requires:       python-cffi
Requires:       python-msgpack >= 0.5.0
%endif
Requires:       python-%{pkgname}-lang = %{version}-%{release}

%description -n python2-%{pkgname}
%{common_desc}


%package -n     python2-%{pkgname}-tests
Summary:        OpenStack library for privilege separation tests
Requires:       python2-%{pkgname}

%description -n python2-%{pkgname}-tests
%{common_desc}

This package contains the test files.

%if 0%{?with_python3}
%package -n     python3-%{pkgname}
Summary:        OpenStack library for privilege separation
%{?python_provide:%python_provide python3-%{pkgname}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 1.8
BuildRequires:  python3-babel >= 1.3
BuildRequires:  python3-oslo-log >= 3.36.0
BuildRequires:  python3-oslo-i18n >= 3.15.3
BuildRequires:  python3-oslo-config >= 2:5.2.0
BuildRequires:  python3-oslotest
BuildRequires:  python3-oslo-utils >= 3.33.0
BuildRequires:  python3-cffi
BuildRequires:  python3-eventlet
BuildRequires:  python3-greenlet
BuildRequires:  python3-msgpack >= 0.5.0

Requires:       python3-babel >= 1.3
Requires:       python3-eventlet >= 0.18.2
Requires:       python3-greenlet >= 0.4.10
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-cffi
Requires:       python3-msgpack >= 0.5.0
Requires:       python-%{pkgname}-lang = %{version}-%{release}


%description -n python3-%{pkgname}
%{common_desc}


%package -n     python3-%{pkgname}-tests
Summary:        OpenStack library for privilege separation tests
Requires:       python3-%{pkgname}

%description -n python3-%{pkgname}-tests
%{common_desc}

This package contains the test files.
%endif


%package -n python-%{pkgname}-doc
Summary:        oslo.privsep documentation

%if 0%{?fedora} > 0
BuildRequires:  python2-enum34
%else
BuildRequires:  python-enum34
%endif

%description -n python-%{pkgname}-doc
Documentation for oslo.privsep

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
%py2_build
%if 0%{?with_python3}
%py3_build

%endif
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/oslo_privsep/locale

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/oslo_privsep/locale/*/LC_*/oslo_privsep*po
rm -f %{buildroot}%{python2_sitelib}/oslo_privsep/locale/*pot
mv %{buildroot}%{python2_sitelib}/oslo_privsep/locale %{buildroot}%{_datadir}/locale
%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/oslo_privsep/locale
%endif

# Find language files
%find_lang oslo_privsep --all-name

%check
%if 0%{?with_python3}
%{__python3} setup.py test ||:
%endif
%{__python2} setup.py test ||:


%files -n python2-%{pkgname}
%doc README.rst
%{_bindir}/privsep-helper
%{python2_sitelib}/oslo_privsep
%{python2_sitelib}/%{pypi_name}-*-py?.?.egg-info
%exclude %{python2_sitelib}/oslo_privsep/tests


%files -n python2-%{pkgname}-tests
%{python2_sitelib}/oslo_privsep/tests



%if 0%{?with_python3}
%files -n python3-%{pkgname}
%doc README.rst
# no python3 binary
%{python3_sitelib}/oslo_privsep
%{python3_sitelib}/%{pypi_name}-*-py?.?.egg-info
%exclude %{python3_sitelib}/oslo_privsep/tests


%files -n python3-%{pkgname}-tests
%{python3_sitelib}/oslo_privsep/tests
%endif

%files -n python-%{pkgname}-doc
%license LICENSE
%doc doc/build/html

%files -n python-%{pkgname}-lang -f oslo_privsep.lang
%license LICENSE

%changelog
