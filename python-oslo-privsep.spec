%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global pypi_name oslo.privsep
%global pkgname oslo-privsep

%global with_doc 1

%global common_desc OpenStack library for privilege separation

Name:           python-%{pkgname}
Version:        3.2.0
Release:        1%{?dist}
Summary:        OpenStack library for privilege separation

License:        Apache-2.0
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
Obsoletes: python2-%{pkgname} < %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
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

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i '/sphinx-build/ s/-W//' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif


%install
%pyproject_install

# Generate i18n files
%{__python3} setup.py compile_catalog -d %{buildroot}%{python3_sitelib}/oslo_privsep/locale --domain oslo_privsep


# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_privsep/locale/*/LC_*/oslo_privsep*po
rm -f %{buildroot}%{python3_sitelib}/oslo_privsep/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_privsep/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_privsep --all-name

%check
%tox -e %{default_toxenv}


%files -n python3-%{pkgname}
%doc README.rst
%{python3_sitelib}/oslo_privsep
%{python3_sitelib}/%{pypi_name}-*.dist-info
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
* Fri Sep 01 2023 RDO <dev@lists.rdoproject.org> 3.2.0-1
- Update to 3.2.0

