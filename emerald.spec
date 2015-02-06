%define __noautoreq 'pkgconfig\\(libdecoration\\)'

%define major 0
%define libname %mklibname %{name}engine %{major}
%define devname %mklibname -d %{name}engine

Name:		emerald
Version:	0.8.8
Release:	2
Summary:	Window decorator for Compiz
Group:		System/X11
License:	GPLv2
URL:		http://www.compiz.org/
Source:		http://releases.compiz.org/components/emerald/%{name}-%{version}.tar.bz2
BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	subversion-devel
BuildRequires:	compiz0.8-devel
BuildRequires:	pkgconfig(apr-1)
BuildRequires:	pkgconfig(apr-util-1)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libwnck-1.0)
BuildRequires:	pkgconfig(neon)
BuildRequires:	pkgconfig(pango)

Requires:	compiz0.8
Requires:	emerald-themes
Provides:	compiz-decorator = %{version}-%{release}

%description
Themeable window decorator for the Compiz window manager/compositor.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Library files for %{name}
Group:		System/X11
Conflicts:	%{_lib}name

%description -n %{libname}
Library files for %{name}.

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files from %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Requires:	compiz0.8-devel
Provides:	%{name}-devel = %{version}-%{release}
Conflicts:	%{_lib}name-devel

%description -n %{devname}
Development files from %{name}.

#----------------------------------------------------------------------------

%prep
%setup -q

%build
%configure2_5x \
	--disable-mime-update \
	--disable-static

%make LIBS="-ldl -lm"

%install
%makeinstall_std

%find_lang %{name}

desktop-file-install \
  --vendor="" \
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

#----------------------------------------------------------------------------

%files -f %{name}.lang
%doc AUTHORS ChangeLog README COPYING
%{_bindir}/%{name}*
%{_libdir}/%{name}/engines/*.so
%{_datadir}/applications/%{name}*.desktop
%{_datadir}/mime-info/%{name}.mime
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/mimelnk/application/x-%{name}-theme.desktop
%{_datadir}/pixmaps/%{name}*.png
%{_iconsdir}/hicolor/48x48/mimetypes/*.png
%{_datadir}/%{name}/*
%{_mandir}/man1/%{name}*.1*

%files -n %{libname}
%{_libdir}/lib%{name}engine.so.%{major}*

%files -n %{devname}
%{_libdir}/pkgconfig/%{name}engine.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/lib%{name}engine.so

