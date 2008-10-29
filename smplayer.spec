# define correct path to used binaries
# works on: fedora >= 7, centos >= 5
%if 0%{?rhel} > 1
  %define _qt4_qmake %{_libdir}/qt4/bin/qmake
  %define _qt4_lrelease %{_libdir}/qt4/bin/lrelease
%else
  %define _qt4_lrelease %{_bindir}/lrelease-qt4
%endif

Name:           smplayer
Version:        0.6.4
Release:        1%{?dist}
Summary:        A graphical frontend for mplayer

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://smplayer.sourceforge.net/linux/
Source0:        http://download.berlios.de/smplayer/smplayer-%{version}.tar.bz2
# Add a servicemenu to enqeue files in smplayer's playlist. 
# The first one is for KDE4, the second one for KDE3.
# see also: 
# https://sourceforge.net/tracker/?func=detail&atid=913576&aid=2052905&group_id=185512
Source1:        smplayer_enqueue_kde4.desktop
Source2:        smplayer_enqueue_kde3.desktop
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  qt4-devel
# smplayer without mplayer is quite useless
Requires:       mplayer

%description
smplayer intends to be a complete front-end for Mplayer, from basic features
like playing videos, DVDs, and VCDs to more advanced features like support
for Mplayer filters and more. One of the main features is the ability to
remember the state of a played file, so when you play it later it will resume
at the same point and with the same settings. smplayer is developed with
the Qt toolkit, so it's multi-platform.

%prep
%setup -qn %{name}-%{version}

# correction for wrong-file-end-of-line-encoding
%{__sed} -i 's/\r//' *.txt
# fix files which are not UTF-8 
iconv -f Latin1 -t UTF-8 -o Changelog.utf8 Changelog 
mv Changelog.utf8 Changelog

# use lrelease from qt4-devel
sed -i 's|LRELEASE=lrelease|LRELEASE=%{_qt4_lrelease}|' Makefile

# fix path of docs
sed -i 's|DOC_PATH=$(PREFIX)/share/doc/packages/smplayer|DOC_PATH=$(PREFIX)/share/doc/smplayer-%{version}|' Makefile

# use %{?_smp_mflags}
sed -i '/cd src && $(QMAKE) $(QMAKE_OPTS) && $(DEFS) make/s!$! %{?_smp_mflags}!' Makefile

# don't show smplayer_enqueue.desktop in KDE and use servicemenus instead
echo "NotShowIn=KDE;" >> smplayer_enqueue.desktop

%build
make QMAKE=%{_qt4_qmake} PREFIX=%{_prefix}

%install
rm -rf %{buildroot}
make PREFIX=%{_prefix} DESTDIR=%{buildroot}/ install

desktop-file-install --delete-original                   \
        --vendor "rpmfusion"                             \
        --dir %{buildroot}%{_datadir}/applications/      \
        %{buildroot}%{_datadir}/applications/%{name}.desktop


desktop-file-install --delete-original                   \
        --vendor "rpmfusion"                             \
        --dir %{buildroot}%{_datadir}/applications/      \
        %{buildroot}%{_datadir}/applications/%{name}_enqueue.desktop

# Add servicemenus dependend on the version of KDE:
# https://sourceforge.net/tracker/index.php?func=detail&aid=2052905&group_id=185512&atid=913576
%if 0%{?fedora} >= 9
  install -Dpm 0644 %{SOURCE1} %{buildroot}%{_datadir}/kde4/services/ServiceMenus/smplayer_enqueue.desktop
%else
  install -Dpm 0644 %{SOURCE2} %{buildroot}%{_datadir}/apps/konqueror/servicemenus/smplayer_enqueue.desktop
%endif


%clean
rm -rf %{buildroot}

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
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}/
%{_bindir}/smplayer
%{_datadir}/applications/rpmfusion-smplayer*.desktop
%{_datadir}/icons/hicolor/*/apps/smplayer.png
%{_datadir}/smplayer/
%{_mandir}/man1/smplayer.1.gz

%if 0%{?fedora} >= 9
  %dir %{_datadir}/kde4/services/ServiceMenus/
  %{_datadir}/kde4/services/ServiceMenus/smplayer_enqueue.desktop
%else
  %dir %{_datadir}/apps/konqueror/
  %dir %{_datadir}/apps/konqueror/servicemenus/
  %{_datadir}/apps/konqueror/servicemenus/smplayer_enqueue.desktop
%endif

%changelog
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
