%define oname vid.stab
%define	major	1.2
%define	libname	%mklibname vidstab %{major}
%define	devname	%mklibname vidstab -d

Summary:	Video stabilization library
Name:		vidstab
Version:	1.1.1
Release:	1
License:	GPLv2
Group:		Sound
Url:		https://public.hronopik.de/vid.stab
Source0:	https://github.com/georgmartius/vid.stab/archive/refs/tags/v%{version}/%{oname}-%{version}.tar.gz
BuildRequires:	cmake

%description
Video stabilization library with plugins for transcode and ffmpeg.

%package -n	%{libname}
Summary:	Shared library for vidstab
Group:		System/Libraries

%description -n	%{libname}
Shared library required for using %{name}.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n	%{devname}
This package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n %{oname}-%{version} -p1

# (tpg) use OMP form llvm
sed -i -e 's/-lgomp/-fopenmp/g' CMakeLists.txt
sed -i -e 's/vidstab gomp/vidstab omp/g' CMakeLists.txt

%build
%global optflags %{optflags} -Ofast -fopenmp
%global ldflags %{ldflags} -fopenmp

%cmake	-DUSE_OMP:BOOL=ON \
%ifnarch %{ix86} %{x86_64}
	-DSSE2_FOUND:BOOL=OFF
%endif

%make_build

%install
%make_install -C build

%files -n %{libname}
%{_libdir}/libvidstab.so.%{major}

%files -n %{devname}
%{_libdir}/libvidstab.so
%dir %{_includedir}/vid.stab
%{_includedir}/vid.stab/*.h
%{_libdir}/pkgconfig/vidstab.pc
