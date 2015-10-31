%global modname nibabel

Name:           python-%{modname}
Version:        2.0.1
Release:        1%{?dist}
Summary:        Python package to access a cacophony of neuro-imaging file formats

License:        MIT and PDDL-1.0
URL:            http://nipy.org/nibabel/
Source0:        https://github.com/nipy/nibabel/archive/%{version}/%{modname}-%{version}.tar.gz
# https://github.com/nipy/nibabel/pull/358
Patch0:         0001-BF-Set-strided_scalar-as-not-writeable.patch
BuildRequires:  git-core
BuildArch:      noarch

%description
Read / write access to some common neuroimaging file formats

This package provides read +/- write access to some common medical and
neuroimaging file formats, including: ANALYZE (plain, SPM99, SPM2 and
later), GIFTI, NIfTI1, NIfTI2, MINC1, MINC2, MGH and ECAT as well as Philips
PAR/REC. We can read and write Freesurfer geometry, and read Freesurfer
morphometry and annotation files. There is some very limited support for DICOM.
NiBabel is the successor of PyNIfTI.

The various image format classes give full or selective access to header (meta)
information and access to the image data is made available via NumPy arrays.

%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel python-setuptools
# Test deps
BuildRequires:  numpy
BuildRequires:  python-six scipy
BuildRequires:  python2-pydicom h5py
Requires:       numpy
Requires:       python-six scipy
Recommends:     python2-pydicom

%description -n python2-%{modname}
Read / write access to some common neuroimaging file formats

This package provides read +/- write access to some common medical and
neuroimaging file formats, including: ANALYZE (plain, SPM99, SPM2 and
later), GIFTI, NIfTI1, NIfTI2, MINC1, MINC2, MGH and ECAT as well as Philips
PAR/REC. We can read and write Freesurfer geometry, and read Freesurfer
morphometry and annotation files. There is some very limited support for DICOM.
NiBabel is the successor of PyNIfTI.

The various image format classes give full or selective access to header (meta)
information and access to the image data is made available via NumPy arrays.

Python 2 version.

%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel python3-setuptools
BuildRequires:  python3-numpy
# Test deps
BuildRequires:  python3-nose
BuildRequires:  python3-six python3-scipy
BuildRequires:  python3-pydicom python3-h5py
Requires:       python3-numpy
Requires:       python3-six python3-scipy
Recommends:     python3-pydicom

%description -n python3-%{modname}
Read / write access to some common neuroimaging file formats

This package provides read +/- write access to some common medical and
neuroimaging file formats, including: ANALYZE (plain, SPM99, SPM2 and
later), GIFTI, NIfTI1, NIfTI2, MINC1, MINC2, MGH and ECAT as well as Philips
PAR/REC. We can read and write Freesurfer geometry, and read Freesurfer
morphometry and annotation files. There is some very limited support for DICOM.
NiBabel is the successor of PyNIfTI.

The various image format classes give full or selective access to header (meta)
information and access to the image data is made available via NumPy arrays.

Python 3 version.

%prep
%autosetup -n %{modname}-%{version} -S git
rm -vrf %{modname}/externals/
# Hard fix for bundled libs
find -type f -name '*.py' -exec sed -i \
  -e "s/from \.*[ ]*externals.six/from six/"        \
  -e "s/from \.*externals.netcdf/from scipy.io.netcdf/"  \
  {} ';'
sed -i -e "/externals/d" setup.py

%build
%py2_build
%py3_build

%install
%py3_install
%py2_install

# Rename binaries
pushd %{buildroot}%{_bindir}
  for mod in parrec2nii nib-ls nib-dicomfs nib-nifti-dx
  do
    mv $mod python2-$mod

    sed -i '1s|^.*$|#!/usr/bin/env %{__python2}|' python2-$mod
    for i in $mod $mod-2 $mod-%{python2_version}
    do
      ln -s python2-$mod $i
    done

    cp python2-$mod python3-$mod
    sed -i '1s|^.*$|#!/usr/bin/env %{__python3}|' python3-$mod

    for i in $mod-3 $mod-%{python3_version}
    do
      ln -s python3-$mod $i
    done
  done
popd

%check
nosetests-%{python2_version} -v
nosetests-%{python3_version} -v

%files -n python2-%{modname}
%license COPYING
%{_bindir}/python2-parrec2nii
%{_bindir}/parrec2nii
%{_bindir}/parrec2nii-2
%{_bindir}/parrec2nii-%{python2_version}
%{_bindir}/python2-nib-ls
%{_bindir}/nib-ls
%{_bindir}/nib-ls-2
%{_bindir}/nib-ls-%{python2_version}
%{_bindir}/python2-nib-dicomfs
%{_bindir}/nib-dicomfs
%{_bindir}/nib-dicomfs-2
%{_bindir}/nib-dicomfs-%{python2_version}
%{_bindir}/python2-nib-nifti-dx
%{_bindir}/nib-nifti-dx
%{_bindir}/nib-nifti-dx-2
%{_bindir}/nib-nifti-dx-%{python2_version}
%{python2_sitelib}/%{modname}*
%{python2_sitelib}/nisext/

%files -n python3-%{modname}
%license COPYING
%{_bindir}/python3-parrec2nii
%{_bindir}/parrec2nii-3
%{_bindir}/parrec2nii-%{python3_version}
%{_bindir}/python3-nib-ls
%{_bindir}/nib-ls-3
%{_bindir}/nib-ls-%{python3_version}
%{_bindir}/python3-nib-dicomfs
%{_bindir}/nib-dicomfs-3
%{_bindir}/nib-dicomfs-%{python3_version}
%{_bindir}/python3-nib-nifti-dx
%{_bindir}/nib-nifti-dx-3
%{_bindir}/nib-nifti-dx-%{python3_version}
%{python3_sitelib}/%{modname}*
%{python3_sitelib}/nisext/

%changelog
* Sat Oct 31 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.1-1
- Initial package
