%define name emerald
%define version 0.7.8
%define rel 1
%define git 20080912
%define _disable_ld_no_undefined 1

%define major 0
%define libname %mklibname %{name} %major
%define libname_devel %mklibname -d %{name}

%if  %{git}
%define srcname %{name}-%{git}
%define distname %{name}
%define release %mkrel 0.%{git}.%{rel}
%else
%define srcname %{name}-%{version}
%define distname %{name}-%{version}
%define release %mkrel %{rel}
%endif

Name: %name
Version: %version
Release: %release
Summary: Window decorator for Compiz
Group: System/X11
URL: http://www.compiz-fusion.org/
Source: %{srcname}.tar.bz2
License: GPL
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: compiz-devel
BuildRequires: apr-devel
BuildRequires: apr-util-devel
BuildRequires: subversion-devel
BuildRequires: neon-devel
BuildRequires: intltool
BuildRequires: gtk2-devel
BuildRequires: libwnck-devel
BuildRequires: pango-devel
BuildRequires: desktop-file-utils
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

Requires: compiz
Requires: emerald-themes
Provides: compiz-decorator

%description
Themable window decorator for the Compiz window manager/compositor

%if %mdkversion < 200900
%post
%update_menus
%{update_desktop_database}
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%{clean_desktop_database}
%endif


%package -n %libname
Summary: Library files for %{name}
Group: System/X11
Requires: %{name} = %{version}
Provides: %libname = %version

%description -n %libname
Library files for %{name}

# Don't put a spacer comment below as it breaks things :/
%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif



%package -n %libname_devel
Summary: Development files from %{name}
Group: Development/Other
Requires: %libname = %{version}
Provides: lib%{name}-devel = %{version}
Provides: %{name}-devel = %{version}
Obsoletes: %{name}-devel
Obsoletes: %mklibname -d %name 0
Obsoletes: cgwd-devel

%description -n %libname_devel
Headers files for %{name}

#----------------------------------------------------------------------------

%prep
%setup -q -n %{distname}

%build
%if %{git}
  # This is a GIT snapshot, so we need to generate makefiles.
  sh autogen.sh -V
%endif
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

desktop-file-install \
  --vendor="" \
  --add-category="GTK" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
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

#----------------------------------------------------------------------------

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

%files -n %libname
%defattr(-,root,root)
%{_libdir}/lib%{name}engine.so.*
%{_libdir}/%{name}/engines/*.so

%files -n %libname_devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/%{name}engine.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/lib%{name}engine.so
%{_libdir}/lib%{name}engine.a
%{_libdir}/lib%{name}engine.la
%{_libdir}/%{name}/engines/*.a
%{_libdir}/%{name}/engines/*.la

