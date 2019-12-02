%define major         0
%define libname       %mklibname emeraldengine %major
%define libname_devel %mklibname emeraldengine -d

# don't provide theme engine .so
%global __provides_exclude_from %{_libdir}/%{name}/engines/.*\\.so

Name:               emerald
Version:            0.8.16
Release:            1
Summary:            Window Decorator for Compiz
Group:              System/X11
License:            GPLv2+
URL:                https://github.com/compiz-reloaded/%{name}
Source0:            https://gitlab.com/compiz/emerald/-/archive/v%{version}/%{name}-v%{version}.tar.bz2

BuildRequires:      gettext-devel
BuildRequires:      intltool
BuildRequires:      pkgconfig(gtk+-3.0)
BuildRequires:      pkgconfig(libwnck-3.0)
BuildRequires:      pkgconfig(libdecoration)
BuildRequires:      pkgconfig(cairo)
BuildRequires:      pkgconfig(pangocairo)
BuildRequires:      pkgconfig(xrender)
BuildRequires:      pkgconfig(xi)

Requires:           compiz >= 1:0.8.16
Provides:           compiz-decorator

Conflicts:          %{_lib}emerald0 < 0.8.16-2

Recommends:         %{name}-themes

%description
Themeable window decorator for the Compiz window manager/compositor.

#----------------------------------------------------------------------------

%package -n %libname
Summary:   Library files for %{name}
Group:     System/X11
Requires:  %{name} = %{version}-%{release}
Obsoletes: %{_lib}emerald0 < 0.8.16-2

%description -n %{libname}
Emerald Window Decorator for Compiz.

This package contains library files for %{name}

#----------------------------------------------------------------------------

%package -n %libname_devel
Group:     Development/C
Summary:   Devel package for %{name}

Requires:  %{name} = %{version}-%{release}
Requires:  %{libname} = %{version}-%{release}
Provides:  %{name}-devel = %{version}
Obsoletes: %{_lib}emerald-devel < 0.8.16-2

%description -n %libname_devel
Emerald - Window Decorator for Compiz.

This package contains static libraries and header files needed for development.

#----------------------------------------------------------------------------

%prep
%setup -qn %{name}-v%{version}

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
    --disable-rpath \
    --disable-static \
    --disable-mime-update \
    --with-gtk=3.0

%make_build

%install
%make_install

desktop-file-install \
  --vendor="" \
  --add-category="GTK" \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/*.desktop

mkdir -p %{buildroot}%{_datadir}/mimelnk/application
cat >%{buildroot}%{_datadir}/mimelnk/application/x-%{name}-theme.desktop <<EOF
[Desktop Entry]
Type=MimeType
Comment=%{name} Theme
MimeType=application/x-%{name}-theme
Patterns=*.%{name}
EOF

find %{buildroot} -name '*.la' -delete

%find_lang %{name}

#----------------------------------------------------------------------------

%files -f %{name}.lang
%doc AUTHORS NEWS
%license COPYING
%{_bindir}/%{name}*
%dir %{_libdir}/%{name}/
%dir %{_libdir}/%{name}/engines/
%{_libdir}/%{name}/engines/*.so
%{_datadir}/applications/%{name}-theme-manager.desktop
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/theme
%{_datadir}/%{name}/theme/*
%{_datadir}/%{name}/settings.ini
%{_datadir}/mime-info/%{name}.mime
%{_datadir}/mime/packages/%{name}.xml
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/apps/*.svg
%{_datadir}/mimelnk/application/x-%{name}-theme.desktop
%{_mandir}/man1/*.1*

%files -n %libname
%{_libdir}/libemeraldengine.so.%{major}{,.*}

%files -n %libname_devel
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/libemeraldengine.so
%{_libdir}/pkgconfig/emeraldengine.pc
