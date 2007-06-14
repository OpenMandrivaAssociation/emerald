%define rname emerald
%define name %{rname}
%define version 0.2.1
%define release %mkrel 1

%define lib_major 0
%define lib_name %mklibname %{name} %lib_major
%define lib_name_devel %mklibname -d %{name} %lib_major

Name: %name
Version: %version
Release: %release
Summary: Window decorator for beryl
Group: System/X11
URL: http://www.beryl-project.org/
Source: http://releases.beryl-project.org/%{version}/%{name}-%{version}.tar.bz2
Patch1: %name-0.2.1-no_wnck_modal.patch
License: GPL
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: beryl-core-devel = %{version}
BuildRequires: apr-devel
BuildRequires: apr-util-devel
BuildRequires: subversion-devel
BuildRequires: neon-devel
BuildRequires: intltool
BuildRequires: desktop-file-utils
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

Requires: beryl-core
Requires: emerald-themes

# cgwd was renamed to emerald
Provides: cgwd
Obsoletes: cgwd

%description
Themable window decorator for the Beryl window manager/compositor

%post
%update_menus
%{update_desktop_database}

%postun
%clean_menus
%{clean_desktop_database}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS  ChangeLog README COPYING 
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}*.desktop
%{_datadir}/mime-info/%{name}.mime
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/mimelnk/application/x-%{name}-theme.desktop
%{_datadir}/pixmaps/%{name}*.png
%{_datadir}/icons/hicolor/48x48/mimetypes/*.png
%{_datadir}/%{name}/*
%{_mandir}/man1/%{name}*.1*

#----------------------------------------------------------------------------

%package -n %lib_name
Summary: Library files for %{name}
Group: System/X11
Requires: %{name} = %{version}
Provides: %lib_name = %version

%description -n %lib_name
Library files for %{name}

%post -n %lib_name -p /sbin/ldconfig

%postun -n %lib_name -p /sbin/ldconfig

%files -n %lib_name
%defattr(-,root,root)
%{_libdir}/lib%{name}engine.so.*
%{_libdir}/%{name}/engines/*.so

#----------------------------------------------------------------------------

%package -n %lib_name_devel
Summary: Development files from %{name}
Group: Development/Other
Requires: %lib_name = %{version}
Provides: lib%{name}-devel = %{version}
Provides: %{name}-devel = %{version}
Obsoletes: %{name}-devel
Obsoletes: cgwd-devel

%description -n %lib_name_devel
Headers files for %{name}

%post -n %lib_name_devel -p /sbin/ldconfig

%files -n %lib_name_devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/%{name}engine.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/lib%{name}engine.so
%{_libdir}/lib%{name}engine.a
%{_libdir}/lib%{name}engine.la
%{_libdir}/%{name}/engines/*.a
%{_libdir}/%{name}/engines/*.la

#----------------------------------------------------------------------------

%prep
%setup -q
%patch1 -p1

%build
%configure2_5x \
                --disable-mime-update \
                --with-apr-config=apr-1-config \
                --with-apu-config=apu-1-config \
                --with-svn-lib=%_libdir

%make

%install
rm -rf %{buildroot}
%makeinstall_std
%find_lang %{name}

sed -i 's/Exec=emerald-theme-manager -i//' %{buildroot}%{_datadir}/applications/emerald-theme-manager.desktop

desktop-file-install \
  --vendor="" \
  --remove-category="Settings" \
  --add-category="X-MandrivaLinux-System-Configuration-Other" \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/*.desktop

mkdir -p %{buildroot}%{_datadir}/mimelnk/application
cat >%{buildroot}%{_datadir}/mimelnk/application/x-%{name}-theme.desktop <<EOF
[Desktop Entry]
Type=MimeType
Comment=Emerald Theme
MimeType=application/x-emerald-theme
Patterns=*.emerald
EOF

%clean
rm -rf %{buildroot}


