%global smtube_ver 1.1

Name:           smplayer
Version:        0.8.0
Release:        2%{?dist}
Summary:        A graphical frontend for mplayer

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://smplayer.sourceforge.net/linux/
Source0:        http://downloads.sourceforge.net/smplayer/smplayer-%{version}.tar.bz2
# Add a servicemenu to enqeue files in smplayer's playlist. 
# see also: 
# https://sourceforge.net/tracker/?func=detail&atid=913576&aid=2052905&group_id=185512
Source1:        smplayer_enqueue_kde4.desktop
Source3:        http://downloads.sourceforge.net/smplayer/smtube-%{smtube_ver}.tar.bz2
# Fix regression in Thunar (TODO: re-check in upcoming versions!)
# https://bugzilla.rpmfusion.org/show_bug.cgi?id=1217
Patch0:         smplayer-0.8.0-desktop-files.patch
Patch1:         smplayer-0.8.0-system-quazip.patch
Patch2:         smplayer-0.8.0-system-qtsingleapplication.patch

BuildRequires:  desktop-file-utils
BuildRequires:  qt4-devel
BuildRequires:  quazip-devel
BuildRequires:  qtsingleapplication-devel
# smplayer without mplayer is quite useless
Requires:       mplayer
Requires:       kde-filesystem

%description
smplayer intends to be a complete front-end for Mplayer, from basic features
like playing videos, DVDs, and VCDs to more advanced features like support
for Mplayer filters and more. One of the main features is the ability to
remember the state of a played file, so when you play it later it will resume
at the same point and with the same settings. smplayer is developed with
the Qt toolkit, so it's multi-platform.

%prep
%setup -qn %{name}-%{version}
%setup -a3 -qn %{name}-%{version}
#remove some bundle sources 
rm -rf zlib-1.2.6
rm -rf src/findsubtitles/quazip
rm -rf src/qtsingleapplication/

%patch0 -p0 -b .desktop-files
%patch1 -p1 -b .quazip
%patch2 -p1 -b .qtsingleapplication

# correction for wrong-file-end-of-line-encoding
%{__sed} -i 's/\r//' *.txt
# fix files which are not UTF-8 
iconv -f Latin1 -t UTF-8 -o Changelog.utf8 Changelog 
mv Changelog.utf8 Changelog

# use lrelease from qt4-devel
sed -i 's|LRELEASE=lrelease|LRELEASE=%{_bindir}/lrelease-qt4|' Makefile

# fix path of docs
sed -i 's|DOC_PATH=$(PREFIX)/share/doc/packages/smplayer|DOC_PATH=$(PREFIX)/share/doc/smplayer-%{version}|' Makefile

# use %{?_smp_mflags}
sed -i '/cd src && $(QMAKE) $(QMAKE_OPTS) && $(DEFS) make/s!$! %{?_smp_mflags}!' Makefile

# don't show smplayer_enqueue.desktop in KDE and use servicemenus instead
echo "NotShowIn=KDE;" >> smplayer_enqueue.desktop

%build
make QMAKE=%{_qt4_qmake} PREFIX=%{_prefix}

pushd smtube-%{smtube_ver}
sed -i 's|lrelease|%{_bindir}/lrelease-qt4|' Makefile
sed -i 's|qmake|%{_qt4_qmake}|' Makefile
sed -i 's|/usr/local|%{_prefix}|' Makefile
sed -i 's|doc/smtube|doc/%{name}-%{version}/smtube|' Makefile
sed -i 's|smtube/translations|smplayer/translations|' Makefile
make PREFIX=%{_prefix}
popd


%install
make QMAKE=%{_qt4_qmake} PREFIX=%{_prefix} DESTDIR=%{buildroot}/ install
pushd smtube-%{smtube_ver}
make install DESTDIR=%{buildroot}
popd

desktop-file-install --delete-original                   \
        --vendor "rpmfusion"                             \
        --dir %{buildroot}%{_datadir}/applications/      \
        %{buildroot}%{_datadir}/applications/%{name}.desktop


desktop-file-install --delete-original                   \
        --vendor "rpmfusion"                             \
        --dir %{buildroot}%{_datadir}/applications/      \
        %{buildroot}%{_datadir}/applications/%{name}_enqueue.desktop

desktop-file-validate %{buildroot}%{_datadir}/applications/smtube.desktop

# Add servicemenus dependend on the version of KDE:
# https://sourceforge.net/tracker/index.php?func=detail&aid=2052905&group_id=185512&atid=913576
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_datadir}/kde4/services/ServiceMenus/smplayer_enqueue.desktop

%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
update-desktop-database &> /dev/null || :

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
update-desktop-database &> /dev/null || :

%files
%{_docdir}/%{name}-%{version}/
%{_bindir}/smplayer
%{_bindir}/smtube
%{_datadir}/applications/rpmfusion-smplayer*.desktop
%{_datadir}/applications/smtube.desktop
%{_datadir}/icons/hicolor/*/apps/smplayer.png
%{_datadir}/icons/hicolor/*/apps/smtube.png
%{_datadir}/smplayer/
%{_mandir}/man1/smplayer.1.gz
%dir %{_datadir}/kde4/services/ServiceMenus/
%{_datadir}/kde4/services/ServiceMenus/smplayer_enqueue.desktop

%changelog
* Sat Apr 28 2012 Sérgio Basto <sergio@serjux.com> - 0.8.0-2
- fix smtube translations.
- drop support for Fedora < 9 and EPEL 5, since we need kde4.

* Sat Apr 28 2012 Sérgio Basto <sergio@serjux.com> - 0.8.0-1 
- New release
- add smtube support
- use system qtsingleapplication
- a little review with: fedora-review -n smplayer --mock-config fedora-16-i386

* Sat Mar 24 2012 Sérgio Basto <sergio@serjux.com> - 0.7.1-1
- New upstream version: 0.7.1, changelog says "This version includes some bug fixes, 
  some of them important. It's highly recommended to update." 
- Remove some bundle sources.
- Small fixes in patches to fit on 0.7.1.

* Sat Mar 24 2012 Sérgio Basto <sergio@serjux.com> - 0.7.0-3
- Add a patch to remove bundled quazip shlibs and Requires kde-filesystem, bug rfbz #1164
- Removed tag BuildRoot.

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.0-2
- Rebuilt for c++ ABI breakage

* Tue Feb 7 2012 Sérgio Basto <sergio@serjux.com> - 0.7.0-1
- new upstream version: 0.7.0

* Mon May 24 2010 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.9-2
- #1217: fix regression in Thunar

* Sat Apr 24 2010 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.9-1
- new upstream version: 0.6.9

* Sun Jul 28 2009 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.8-1
- new upstream version: 0.6.8

* Sun Mar 29 2009 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.7-1
- new upstream version: 0.6.7

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.6.6-2
- rebuild for new F11 features

* Sat Jan 10 2009 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.6-1
- new upstream version: 0.6.6

* Thu Nov 13 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.5.1-1
- new upstream version: 0.6.5.1

* Wed Oct 29 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.4-1
- new upstream version: 0.6.4

* Mon Sep 29 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.3-1
- new upstream version: 0.6.3

* Fri Aug 15 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.2-1
- new upstream version: 0.6.2
- add servicemenus depending on the KDE version

* Wed Jul 30 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.6.1-4
- rebuild for buildsys cflags issue

* Tue Jul 22 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.1-3
- import into rpmfusion

* Tue Jul 08 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.1-2
- fix packaging of FAQs

* Tue Jun 17 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.1-1
- update to latest upstream version

* Sat Feb 24 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.0-0.3.rc2
- add %%{?_smp_mflags} in Makefile to really use it
- finally fix usage of macros
- mode 0644 for desktop-file isn't needed anymore

* Sat Feb 23 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.0-0.2.rc2
- Update %%post and %%postun scriplets
- use %%{?_smp_mflags} in make
- change vendor to rpmfusion in desktop-file-install
- some minor spec cleanups

* Thu Feb 14 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.0-0.1.rc2
- new upstream version: 0.6.0rc2

* Tue Feb 12 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.0-0.1.rc1
- new upstream version: 0.6.0rc1
- added docs: Changelog Copying.txt Readme.txt Release_notes.txt
- fix path of %%docdir in Makefile

* Tue Dec 18 2007 Sebastian Vahl <fedora@deadbabylon.de> - 0.5.62-1
- new version: 0.5.62
- specify license as GPLv2+

* Thu Sep 20 2007 Sebastian Vahl <fedora@deadbabylon.de> - 0.5.60-1
- Update to development version of qt4

* Thu Sep 20 2007 Sebastian Vahl <fedora@deadbabylon.de> - 0.5.21-1
- new upstream version: 0.5.21
- don't add category "Multimedia" to desktop-file
- correct url of Source0

* Mon Jul 29 2007 Sebastian Vahl <fedora@deadbabylon.de> - 0.5.20-1
- new upstream version: 0.5.20

* Mon Jun 18 2007 Sebastian Vahl <fedora@deadbabylon.de> - 0.5.14-1
- new upstream version: 0.5.14

* Thu Jun 14 2007 Sebastian Vahl <fedora@deadbabylon.de> - 0.5.7-1
- Initial Release
