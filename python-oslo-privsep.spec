%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name oslo.privsep
%global pkgname oslo-privsep

%global with_doc 1

%global common_desc OpenStack library for privilege separation

Name:           python-%{pkgname}
Version:        XXX
Release:        XXX
Summary:        OpenStack library for privilege separation

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:  git-core


%description
%{common_desc}

%package -n     python3-%{pkgname}
Summary:        OpenStack library for privilege separation
%{?python_provide:%python_provide python3-%{pkgname}}
Obsoletes: python2-%{pkgname} < %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 1.8
BuildRequires:  python3-babel >= 1.3
BuildRequires:  python3-oslo-log >= 3.36.0
BuildRequires:  python3-oslo-i18n >= 3.15.3
BuildRequires:  python3-oslo-config >= 2:5.2.0
BuildRequires:  python3-oslotest
BuildRequires:  python3-oslo-utils >= 3.33.0
BuildRequires:  python3-eventlet
BuildRequires:  python3-greenlet
BuildRequires:  python3-cffi
BuildRequires:  python3-msgpack >= 0.5.0
Requires:       python3-eventlet >= 0.21.0
Requires:       python3-greenlet >= 0.4.14
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-cffi
Requires:       python3-msgpack >= 0.6.0
Requires:       python-%{pkgname}-lang = %{version}-%{release}


%description -n python3-%{pkgname}
%{common_desc}


%package -n     python3-%{pkgname}-tests
Summary:        OpenStack library for privilege separation tests
Requires:       python3-%{pkgname}

%description -n python3-%{pkgname}-tests
%{common_desc}

This package contains the test files.

%if 0%{?with_doc}
%package -n python-%{pkgname}-doc
Summary:        oslo.privsep documentation
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinxcontrib-apidoc
BuildRequires:  python3-openstackdocstheme

%description -n python-%{pkgname}-doc
Documentation for oslo.privsep
%endif


%package  -n python-%{pkgname}-lang
Summary:   Translation files for Oslo privsep library

%description -n python-%{pkgname}-lang
Translation files for Oslo privsep library


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
rm -rf {,test-}requirements.txt

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

# Generate i18n files
%{__python3} setup.py compile_catalog -d build/lib/oslo_privsep/locale --domain oslo_privsep

%install
%{py3_install}

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_privsep/locale/*/LC_*/oslo_privsep*po
rm -f %{buildroot}%{python3_sitelib}/oslo_privsep/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_privsep/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_privsep --all-name

%check
%{__python3} setup.py test ||:


%files -n python3-%{pkgname}
%doc README.rst
%{python3_sitelib}/oslo_privsep
%{python3_sitelib}/%{pypi_name}-*-py%{python3_version}.egg-info
%exclude %{python3_sitelib}/oslo_privsep/tests
%{_bindir}/privsep-helper


%files -n python3-%{pkgname}-tests
%{python3_sitelib}/oslo_privsep/tests

%if 0%{?with_doc}
%files -n python-%{pkgname}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python-%{pkgname}-lang -f oslo_privsep.lang
%license LICENSE

%changelog
