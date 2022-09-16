%define vendor_name Realtek
%define vendor_label realtek
%define driver_name r8169

%if %undefined module_dir
%define module_dir override
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{driver_name}-module-alt
Version: 4.19.128
Release: 3%{?dist}
License: GPL

# Source taken from https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/drivers/net/ethernet/realtek?h=v4.19.128
Source0: %{driver_name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{driver_name}-%{version}

%build
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Fri Sep 16 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 4.19.128-3
- Rebuild for XCP-ng 8.3

* Wed Aug 19 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 4.19.128-2
- Rebuild for XCP-ng 8.2

* Wed Jul 01 2020 Rushikesh Jadhav <rushikesh7@gmail.com> - 4.19.128-1
- Adding Realtek driver r8169 from kernel 4.19.128
