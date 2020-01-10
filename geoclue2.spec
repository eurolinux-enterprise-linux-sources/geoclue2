Name:           geoclue2
Version:        2.1.10
Release:        2%{?dist}
Summary:        Geolocation service

License:        GPLv2+
URL:            http://www.freedesktop.org/wiki/Software/GeoClue/
Source0:        http://www.freedesktop.org/software/geoclue/releases/2.1/geoclue-%{version}.tar.xz

# Fixes from 2.2.0
Patch01: locator-Correct-source-accuracy-comparison.patch
Patch02: service-client-Delay-unrefing-ServiceLocation.patch
Patch03: modem-gps-Fix-GPS-coordinates-parsing.patch
Patch04: service-client-Gracefully-handle-NULL-agent.patch
Patch05: modem-manager-Don-t-enable-the-modem.patch
Patch06: wifi-Remove-a-redundant-condition.patch
Patch07: modem-manager-Wait-for-modem-to-be-enabled.patch

BuildRequires:  glib2-devel
BuildRequires:  intltool
BuildRequires:  itstool
BuildRequires:  json-glib-devel
BuildRequires:  libsoup-devel
BuildRequires:  ModemManager-glib-devel
BuildRequires:  systemd
Requires(pre):  shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires:       dbus

Obsoletes:      geoclue2-server < 2.1.8

%description
Geoclue is a D-Bus service that provides location information. The primary goal
of the Geoclue project is to make creating location-aware applications as
simple as possible, while the secondary goal is to ensure that no application
can access location information without explicit permission from user.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains files for developing applications that
use %{name}.


%prep
%setup -q -n geoclue-%{version}

%patch01 -p1 -b .locator-Correct-source-accuracy-comparison
%patch02 -p1 -b .service-client-Delay-unrefing-ServiceLocation
%patch03 -p1 -b .modem-gps-Fix-GPS-coordinates-parsing
%patch04 -p1 -b .service-client-Gracefully-handle-NULL-agent
%patch05 -p1 -b .modem-manager-Don-t-enable-the-modem
%patch06 -p1 -b .wifi-Remove-a-redundant-condition
%patch07 -p1 -b .modem-manager-Wait-for-modem-to-be-enabled

%build
%configure --with-dbus-service-user=geoclue
make %{?_smp_mflags} V=1


%install
%make_install

# Home directory for the 'geoclue' user
mkdir -p $RPM_BUILD_ROOT/var/lib/geoclue

# Remove demo files
rm $RPM_BUILD_ROOT%{_datadir}/applications/geoclue-demo-agent.desktop
rm $RPM_BUILD_ROOT%{_datadir}/applications/geoclue-where-am-i.desktop
rm $RPM_BUILD_ROOT%{_libexecdir}/geoclue-2.0/demos/where-am-i


%pre
# Update the home directory for existing users
getent passwd geoclue >/dev/null && \
    usermod -d /var/lib/geoclue geoclue &>/dev/null
# Create a new user and group if they don't exist
getent group geoclue >/dev/null || groupadd -r geoclue
getent passwd geoclue >/dev/null || \
    useradd -r -g geoclue -d /var/lib/geoclue -s /sbin/nologin \
    -c "User for geoclue" geoclue
exit 0

%post
%systemd_post geoclue.service

%preun
%systemd_preun geoclue.service

%postun
%systemd_postun_with_restart geoclue.service


%files
%doc COPYING NEWS
%config %{_sysconfdir}/geoclue/
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.GeoClue2.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.GeoClue2.Agent.conf
%{_libexecdir}/geoclue
%{_datadir}/dbus-1/system-services/org.freedesktop.GeoClue2.service
%{_unitdir}/geoclue.service
%attr(755,geoclue,geoclue) %dir /var/lib/geoclue

%files devel
%{_datadir}/dbus-1/interfaces/org.freedesktop.GeoClue2*.xml
%{_libdir}/pkgconfig/geoclue-2.0.pc


%changelog
* Fri Apr 17 2015 Zeeshan Ali <zeenix@redhat.com> 2.1.10-2
- Backport fixes from 2.2.0.

* Wed Apr  1 2015 Zeeshan Ali <zeenix@redhat.com> 2.1.10-1
- Update to 2.1.10

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 21 2014 Kalev Lember <kalevlember@gmail.com> - 2.1.9-1
- Update to 2.1.9

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Kalev Lember <kalevlember@gmail.com> - 2.1.8-1
- Update to 2.1.8
- Remove and obsolete the -server subpackage

* Wed Mar 26 2014 Kalev Lember <kalevlember@gmail.com> - 2.1.7-1
- Update to 2.1.7

* Fri Mar 07 2014 Kalev Lember <kalevlember@gmail.com> - 2.1.6-1
- Update to 2.1.6

* Thu Feb 06 2014 Kalev Lember <kalevlember@gmail.com> - 2.1.2-2
- Add systemd rpm scripts
- Don't install the demo .desktop files

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 2.1.2-1
- Update to 2.1.2

* Sun Oct 06 2013 Kalev Lember <kalevlember@gmail.com> - 2.0.0-1
- Update to 2.0.0
- Create a home directory for the 'geoclue' user

* Thu Sep 19 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.4-2
- Run the service as 'geoclue' user

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.4-1
- Update to 1.99.4

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.3-1
- Update to 1.99.3

* Sun Aug 25 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.2-3
- Update -devel subpackage description (#999153)

* Sat Aug 24 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.2-2
- Review fixes (#999153)
- Drop ldconfig calls that are unnecessary now that the shared library is gone
- Drop the build dep on gobject-introspection-devel
- Include API-Documentation.txt in the -server subpackage

* Fri Aug 23 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.2-1
- Update to 1.99.2
- The shared library is gone in this release and all users should use the
  dbus service directly

* Wed Aug 21 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.1-3
- Include geoip-lookup in the -server subpackage as well

* Wed Aug 21 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.1-2
- Ship geoip-update in -server subpackage

* Tue Aug 20 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.1-1
- Initial Fedora packaging
