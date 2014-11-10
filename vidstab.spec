%define	major	0.9
%define	libname	%mklibname vidstab %{major}
%define	devname	%mklibname vidstab -d

Name:		vidstab
Version:	0.98b
Release:	1
Summary:	Video stabilization library
Source0:	%{name}-%{version}.tar.xz
License:	GPLv2
Group:		Sound
Url:		http://public.hronopik.de/vid.stab
BuildRequires:	cmake gomp-devel

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

%description -n	%{name}
This package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q

%build
%global optflags %{optflags} -Ofast -fopenmp
%cmake	-DUSE_OMP:BOOL=ON \
%ifnarch %{ix86} x86_64
	-DSSE2_FOUND:BOOL=OFF
%endif
%make

%install
%makeinstall_std -C build

%files -n %{libname}
%{_libdir}/libvidstab.so.%{major}

%files -n %{devname}
%{_libdir}/libvidstab.so
%dir %{_includedir}/vid.stab
%{_includedir}/vid.stab/*.h
%{_libdir}/pkgconfig/vidstab.pc
