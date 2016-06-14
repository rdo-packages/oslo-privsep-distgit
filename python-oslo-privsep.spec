%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global pypi_name oslo.privsep
%global pkgname oslo-privsep

Name:           python-%{pkgname}
Version:        XXX
Release:        XXX
Summary:        OpenStack library for privilege separation

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch



%description
OpenStack library for privilege separation


%package -n     python2-%{pkgname}
Summary:        OpenStack library for privilege separation
%{?python_provide:%python_provide python2-%{pkgname}}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr >= 1.8
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-babel >= 1.3
BuildRequires:  python-oslo-log >= 1.14.0
BuildRequires:  python-oslo-i18n >= 2.1.0
BuildRequires:  python-oslo-config >= 3.9.0
BuildRequires:  python-oslotest
BuildRequires:  python-oslo-utils >= 3.5.0
BuildRequires:  python-cffi
BuildRequires:  python-eventlet
BuildRequires:  python-greenlet
BuildRequires:  python-msgpack >= 0.4.0

Requires:       python-babel >= 1.3
Requires:       python-oslo-log >= 1.14.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-config >= 3.9.0
Requires:       python-oslo-utils >= 3.5.0
Requires:       python-cffi
Requires:       python-enum34
Requires:       python-msgpack >= 0.4.0


%description -n python2-%{pkgname}
OpenStack library for privilege separation


%package -n     python2-%{pkgname}-tests
Summary:        OpenStack library for privilege separation tests
Requires:       python2-%{pkgname}

%description -n python2-%{pkgname}-tests
OpenStack library for privilege separation tests



%if 0%{?with_python3}
%package -n     python3-%{pkgname}
Summary:        OpenStack library for privilege separation
%{?python_provide:%python_provide python3-%{pkgname}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 1.8
BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx
BuildRequires:  python3-babel >= 1.3
BuildRequires:  python3-oslo-log >= 1.14.0
BuildRequires:  python3-oslo-i18n >= 2.1.0
BuildRequires:  python3-oslo-config >= 3.9.0
BuildRequires:  python3-oslotest
BuildRequires:  python3-oslo-utils >= 3.5.0
BuildRequires:  python3-cffi
BuildRequires:  python3-eventlet
BuildRequires:  python3-greenlet
BuildRequires:  python3-msgpack >= 0.4.0

Requires:       python3-babel >= 1.3
Requires:       python3-oslo-log >= 1.14.0
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-oslo-config >= 3.9.0
Requires:       python3-oslo-utils >= 3.5.0
Requires:       python3-cffi
Requires:       python3-msgpack >= 0.4.0


%description -n python3-%{pkgname}
OpenStack library for privilege separation


%package -n     python3-%{pkgname}-tests
Summary:        OpenStack library for privilege separation tests
Requires:       python3-%{pkgname}

%description -n python3-%{pkgname}-tests
OpenStack library for privilege separation tests
%endif


%package -n python-%{pkgname}-doc
Summary:        oslo.privsep documentation
%description -n python-%{pkgname}-doc
Documentation for oslo.privsep

%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
rm -rf {,test-}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build

%endif
# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%check
%if 0%{?with_python3}
%{__python3} setup.py test ||:
%endif
%{__python2} setup.py test ||:


%files -n python2-%{pkgname}
%doc README.rst
%license LICENSE
%{_bindir}/privsep-helper
%{python2_sitelib}/oslo_privsep
%{python2_sitelib}/%{pypi_name}-*-py?.?.egg-info
%exclude %{python2_sitelib}/oslo_privsep/tests


%files -n python2-%{pkgname}-tests
%{python2_sitelib}/oslo_privsep/tests



%if 0%{?with_python3}
%files -n python3-%{pkgname}
%doc README.rst
%license LICENSE
# no python3 binary
%{python3_sitelib}/oslo_privsep
%{python3_sitelib}/%{pypi_name}-*-py?.?.egg-info
%exclude %{python3_sitelib}/oslo_privsep/tests


%files -n python3-%{pkgname}-tests
%{python3_sitelib}/oslo_privsep/tests
%endif

%files -n python-%{pkgname}-doc
%doc html

%changelog