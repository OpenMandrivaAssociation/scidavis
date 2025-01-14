Name:		scidavis
Version:	0.2.4
Release:	%mkrel 2
Summary:	An application for Scientific Data Analysis and Visualization
License:	GPLv2
Group:		Sciences/Other
Url:		https://scidavis.sourceforge.net/
Source0:	http://download.sourceforge.net/sourceforge/scidavis/%{name}-%{version}.tar.bz2
Patch0:		scidavis-0.2.4-link-everything-dynamically.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	desktop-file-utils
BuildRequires:	qt4-devel >= 4.3
BuildRequires:	qt-assistant-adp-devel
Buildrequires:	python-qt4-devel >= 4.2
BuildRequires:	python-devel >= 2.5
BuildRequires:	python-sip >= 4.6
BuildRequires:	muparser-devel
BuildRequires:	gsl-devel
Buildrequires:	libqwt-devel >= 5.1.0
BuildRequires:	libqwtplot3d-devel

%description
SciDAVis is a free interactive application aimed at data analysis and
publication-quality plotting. It combines a shallow learning curve and
an intuitive, easy-to-use graphical user interface with powerful
features such as scriptability and extensibility.

%files
%defattr(-,root,root,-)
%doc CHANGES README
%{_sysconfdir}/scidavisrc.py
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_iconsdir}/locolor/*/apps/%{name}.png
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/mimelnk/application/x-sciprj.desktop

#-------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1 -b .dynamically

%build
%qmake_qt4 \
	%if "%{_lib}" != "lib"
		libsuff=64 \
	%endif

%make

%install
rm -rf %{buildroot}
make INSTALL_ROOT=%{buildroot} install

# translations
install -d %{buildroot}%{_datadir}/%{name}/translations
install -D -m644 %{name}/translations/*.qm %{buildroot}%{_datadir}/%{name}/translations/

# fix desktop file
desktop-file-install	--remove-category=Physics \
	--remove-category=Math \
	--remove-category=Graphics \
	--add-category=DataVisualization \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}/%{_datadir}/applications/%{name}.desktop 

%clean
rm -rf %{buildroot}
