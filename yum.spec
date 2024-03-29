%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
 
Summary: RPM installer/updater
Name: yum
Version: 3.2.27
Release: 14%{?dist}
License: GPLv2+
Group: System Environment/Base
Source0: http://yum.baseurl.org/download/3.2/%{name}-%{version}.tar.gz
Source1: yum.conf.fedora
Source2: yum-updatesd.conf.fedora
Patch0: installonlyn-enable.patch
Patch1: yum-mirror-priority.patch
Patch2: yum-manpage-files.patch
Patch3: yum-multilib-policy-best.patch
Patch4: no-more-exactarchlist.patch
Patch5: geode-arch.patch
Patch6: BZ-528738-bugtracker.patch

Patch32: yum-distro-sync.patch
Patch33: yum-install-cmd-exit+provides-msgs+docs.patch
Patch34: yum-history-user.patch
Patch35: yum-PK-search-API.patch
Patch36: yum-history-list-errors+summary-user-column.patch
Patch37: yum-groupremove-leaf-only.patch
Patch38: yum-md-reget+yumvars+searchPrco.patch

Patch39: BZ-588911-yum.log-perms.patch
Patch40: BZ-577627-installroot-double-prefix.patch
Patch41: BZ-588910-nocontext-tsflag.patch
Patch42: BZ-588908-many-install-update-speedup.patch
Patch43: BZ-590340-move-rpmdb-from-cache.patch
Patch44: BZ-590339-edge-case-depsolving.patch
Patch45: BZ-593522-install-obs-arch.patch
Patch46: BZ-595553-akmods-cache-defense.patch
Patch47: BZ-602354-plugin-hooks-verify-transaction.patch
Patch48: BZ-584262-downgrade-dep-chain-remove.patch
Patch49: BZ-572770-int-flags-miscutils.patch
Patch50: BZ-598639-rpm-bindings-api-change-fix.patch
Patch51: BZ-603002-group_remove_leaf-empty-transaction.patch
Patch52: BZ-604080-localinstall-obsoleted.patch
Patch53: BZ-614496-traceback-no-proc-mounted.patch


Patch64: yum-ppc64-preferred.patch
Patch65: yum-3.2.27-i18n-off.patch

URL: http://yum.baseurl.org/
BuildArch: noarch
BuildRequires: python
BuildRequires: gettext
BuildRequires: intltool
Conflicts: pirut < 1.1.4
Requires: python >= 2.4, rpm-python, rpm >= 0:4.4.2
Requires: python-iniparse
Requires: python-sqlite
Requires: python-urlgrabber >= 3.9.0-8
Requires: yum-metadata-parser >= 1.1.0
Requires: pygpgme
Obsoletes: yum-skip-broken, yum-basearchonly
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Yum is a utility that can check for and automatically download and
install updated RPM packages. Dependencies are obtained and downloaded 
automatically prompting the user as necessary.

%package updatesd
Summary: Update notification daemon
Group: Applications/System
Requires: yum = %{version}-%{release}
Requires: dbus-python
Requires: pygobject2
Requires(preun): /sbin/chkconfig
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(post): /sbin/service

%description updatesd
yum-updatesd provides a daemon which checks for available updates and 
can notify you when they are available via email, syslog or dbus. 

%prep
%setup -q
%patch1 -p0
%patch2 -p1
%patch3 -p0
%patch4 -p0
%patch5 -p1
%patch6 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch64 -p0
%patch65 -p1

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/yum.conf
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum/pluginconf.d $RPM_BUILD_ROOT/usr/lib/yum-plugins

# for now, move repodir/yum.conf back
mv $RPM_BUILD_ROOT/%{_sysconfdir}/yum/repos.d $RPM_BUILD_ROOT/%{_sysconfdir}/yum.repos.d
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/yum/yum.conf

# yum-updatesd has moved to the separate source version
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/yum/yum-updatesd.conf 
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/yum-updatesd
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/dbus-1/system.d/yum-updatesd.conf
rm -f $RPM_BUILD_ROOT/%{_sbindir}/yum-updatesd
rm -f $RPM_BUILD_ROOT/%{_mandir}/man*/yum-updatesd*
rm -f $RPM_BUILD_ROOT/%{_datadir}/yum-cli/yumupd.py*

# Ghost files:
mkdir -p $RPM_BUILD_ROOT/var/lib/yum/history
mkdir -p $RPM_BUILD_ROOT/var/lib/yum/plugins
mkdir -p $RPM_BUILD_ROOT/var/lib/yum/yumdb
touch $RPM_BUILD_ROOT/var/lib/yum/uuid

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root, -)
%doc README AUTHORS COPYING TODO INSTALL ChangeLog
%config(noreplace) %{_sysconfdir}/yum.conf
%dir %{_sysconfdir}/yum
%config(noreplace) %{_sysconfdir}/yum/version-groups.conf
# %dir %{_sysconfdir}/yum/protected.d
%dir %{_sysconfdir}/yum.repos.d
%dir %{_sysconfdir}/yum/vars
%config(noreplace) %{_sysconfdir}/logrotate.d/yum
%{_sysconfdir}/bash_completion.d
%dir %{_datadir}/yum-cli
%{_datadir}/yum-cli/*
%{_bindir}/yum
%{python_sitelib}/yum
%{python_sitelib}/rpmUtils
%dir /var/cache/yum
%dir /var/lib/yum
%ghost /var/lib/yum/uuid
%ghost /var/lib/yum/history
%ghost /var/lib/yum/plugins
%ghost /var/lib/yum/yumdb
%{_mandir}/man*/yum.*
%{_mandir}/man*/yum-shell*
# plugin stuff
%dir %{_sysconfdir}/yum/pluginconf.d 
%dir /usr/lib/yum-plugins

%changelog
* Tue Aug 24 2010 Seth Vidal <svidal@redhat.com> - 3.2.27-14
- fixed 588911 patch to be correct patch
- add patch file for 572770 to take the old date from the wrong patch from 588911

* Tue Jul 27 2010 James Antill <james.antill@redhat.com> - 3.2.27-13
- Don't traceback when proc isn't mounted.
- Resolves: rhbz#614496
- Own the /etc/yum/vars dir.
- Resolves: rhbz#611906

* Wed Jun 16 2010 James Antill <james.antill@redhat.com> - 3.2.27-12
- Stop allowing installation of obsoleted, only by installed.
- Resolves: rhbz#604080

* Fri Jun 11 2010 James Antill <james.antill@redhat.com> - 3.2.27-10
- Stop downgrade dep. chain removals
- Resolves: rhbz#584262
- Fix for rpm bindings api change
- Resolves: rhbz#598639
- Add plugin hooks for verify transaction pre/post.
- Resolves: rhbz#602354
- Fix groupremove_leaf_only when it empties the transaction.
- Resolves: rhbz#603002

* Tue May 25 2010 James Antill <james.antill@redhat.com> - 3.2.27-9
- Fix installs of obsoleted multiarch packages.
- Resolves: rhbz#593522
- Create a defense against akmod style postinst install hacks.
- Resolves: rhbz#595553

* Tue May 11 2010 James Antill <james.antill@redhat.com> - 3.2.27-8
- Move rpmdb cache/indexes to /var/lib
- Resolves: rhbz#590340
- Fix old missing recheck in depsolve
- Resolves: rhbz#590339

* Tue May  4 2010 James Antill <james.antill@redhat.com> - 3.2.27-7
- A few minor bugfixes from upstream
- yum.log perms
- Resolves: rhbz#588911
- installroot double prefixing, on anaconda/kickstart install
- Resolves: rhbz#577627
- Add nocontexts flag to tsflags, if available.
- Resolves: rhbz#588910
- Speedup many install/update of same pkg.
- Resolves: rhbz#588908
- Correct os.path.link => os.path.islink typo, for dynamic yum vars.
- Resolves: rhbz#588907

* Fri Apr 16 2010 James Antill <james.antill@redhat.com> - 3.2.27-4
- A few minor bugfixes from upstream
- Add dynamic FS based yumvars
- Resolves: rhbz#576703

* Fri Mar 26 2010 James Antill <james.antill@redhat.com> - 3.2.27-3
- 3.2.27 from Fedora, and a couple of minor patches
- Resolves: rhbz#576703

* Thu Mar 18 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.27-1
- 3.2.27 from upstream (more or less the same as 3.2.26-6 but with a new number

* Thu Mar 11 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.26-6
- should be the final HEAD update before 3.2.27

* Thu Feb 24 2010 James Antill <james@fedoraproject.org> - 3.2.26-5
- new HEAD, minor features and speed.

* Wed Feb 17 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.26-4
- new HEAD to fix the fix to the fix

* Tue Feb 16 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.26-3
- latest head - including fixes to searchPrcos

* Wed Feb 10 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.26-2
- grumble.

* Tue Feb  9 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.26-1
- final 3.2.26

* Mon Feb  8 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.25-14
- $uuid, pkgtags searching, latest HEAD patch - pre 3.2.26

* Fri Jan 28 2010 James Antill <james at fedoraproject.org> - 3.2.25-13
- A couple of bugfixes, most notably:
-  you can now install gpg keys again!
-  bad installed file requires don't get cached.

* Fri Jan 22 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.25-12
- someone forgot to push their changes

* Fri Jan 22 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.25-11
- more fixes, more fun

* Fri Jan 15 2010 James Antill <james at fedoraproject.org> - 3.2.25-10
- latest head
- Fixes for pungi, rpmdb caching and kernel-PAE-devel duplicates finding
- among others.

* Mon Jan  4 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.2.25-8
- latest head

* Thu Dec 10 2009 James Antill <james at fedoraproject.org> - 3.2.25-7
- Fixes the mash bug, lookup in the tsInfo too. :(
- And fix the txmbr/po confusion ... third build the charm.

* Fri Dec  4 2009 James Antill <james at fedoraproject.org> - 3.2.25-4
- Fixes for yum clean all, BZ 544173
- Also allow "yum clean rpmdb" to work, bad tester, bad.

* Thu Dec  3 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.25-2
- rebuild yum with latest HEAD patch
- add rpmdb caching patch james wrote to see if it breaks everyone :)


* Wed Oct 14 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.25-1
- 3.2.25

* Wed Sep 30 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.24-9
- revert yum. import patch b/c it breaks a bunch of things

* Wed Sep 30 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.24-8
- fix up broken build b/c of version-groups.conf file

* Tue Sep 29 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.24-7
- fixes for odd outputs from ts.run and logs for what we store in history

* Wed Sep 23 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.24-6
- new head patch - fixes some issues with history and chroots

* Mon Sep 21 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.24-5
- latest head patch - includes yum history feature.

* Tue Sep 15 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.24-4
- new head patch - translation updates and a few bug fixes

* Wed Sep  9 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.24-3
- add geode arch patch for https://bugzilla.redhat.com/show_bug.cgi?id=518415


* Thu Sep  3 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.24-2
- modify cachedir to include variables

* Thu Sep  3 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.24-1
- 3.2.24

* Wed Sep  2 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.23-16
- fix globbing issue 520810

* Mon Aug 31 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.23-15
- one more head update - fixes some fairly ugly but kind of minor bugs

* Tue Aug 18 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.23-14
- update to latest head pre 3.2.24
- add requirement on python-urlgrabber 3.9.0 and up

* Wed Aug  5 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.23-13
- latest head - right after freeze

* Tue Aug  4 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.23-12
- latest head - right before freeze :)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.23-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.23-10
- remove exactarchlist by request for rawhide

* Thu Jul  2 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.23-9
- update to latest head - make livecd creation work again in rawhide
- disable one of the man page patches until after 3.2.24 is released b/c
  of the changes to the man page in the head patch


* Mon Jun 22 2009 James Antill <james at fedoraproject.org> - 3.2.23-8
- Update to latest head:
- Fix old recursion bug, found by new code.
- Resolves: bug#507220

* Sun Jun 21 2009 James Antill <james at fedoraproject.org> - 3.2.23-6
- Update to latest head:
- Unbreak delPackage() excludes.
- Other fixes/etc.

* Fri Jun 19 2009 James Antill <james at fedoraproject.org> - 3.2.23-5
- Actually apply the HEAD patch included yesterday :).

* Thu Jun 18 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.23-4
- update to latest head

* Mon Jun  8 2009 Seth Vidal <skvidal at fedoraproject.org>
- truncate changelog

* Wed May 20 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.23-2
- add patch to close rpmdb completely

* Tue May 19 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.23-1
- 3.2.23

* Mon May 11 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.22-5
- jump up to almost 3.2.23. 
- had to move patch0 around a bit until we rebase to 3.2.23

* Thu Apr  9 2009 James Antill <james at fedoraproject.org> - 3.2.22-4
- fix typo for yum-complete-transaction message.

* Wed Apr  8 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.22-3
- fix for file:// urls which makes things in pungi/mash work

* Tue Apr  7 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.22-2
- yum-HEAD minus the yumdb patches

* Tue Mar 24 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.22-1
- 3.2.22 - 3 patches beyond 3.2.21-16

* Mon Mar 16 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.21-16
- fix for 490490

* Fri Mar 13 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.21-15
- update to upstream git to fix conditionals problem on anaconda installs

* Thu Mar 12 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.21-14
- latest HEAD

* Tue Mar 10 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.21-13
- f11beta build

* Wed Mar  4 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.21-12
- second verse, same as the first

* Fri Feb 27 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.21-10
- merge up a lot of fixes from latest HEAD

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.21-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.21-9
- merge up to latest yum head - sort of a pre 3.2.22

* Wed Feb  4 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.21-8
- fix for YumHeaderPackages so it plays nicely w/createrepo and mergerepo, etc

* Thu Jan 29 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.21-7
- update HEAD patch to fix repodiff (and EVR comparisons in certain cases)

* Tue Jan 27 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.21-6
- patch to keep anaconda (and other callers) happy
- remove old 6hr patch which is now upstream

* Mon Jan 26 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.21-4
- patch to latest HEAD to test a number of fixes for alpha

* Tue Jan 20 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.21-3
- add a small patch to make things play a bit nicer with the logging module
  in 2.6


* Wed Jan  7 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.2.21-1
- bump to 3.2.21

* Thu Dec 18 2008 James Antill <james@fedoraproject.org> - 3.2.20-8
- merge latest from upstream
- move to 6hr metadata

* Mon Dec  8 2008 Seth Vidal <skvidal at fedoraproject.org> - 3.2.20-7
- merge patch from upstream and remove now old obsoletes patch

* Thu Dec 04 2008 Jesse Keating <jkeating@redhat.com> - 3.2.20-6
- Add patch from upstream to fix cases where obsoletes are disabled. (jantill)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.2.20-5
- Rebuild for Python 2.6

* Wed Nov 26 2008 Seth Vidal <skvidal at fedoraproject.org> - 3.2.20-4
- update head patch

* Wed Oct 29 2008 Seth Vidal <skvidal at fedoraproject.org> - 3.2.20-3
- full patch against HEAD for skipbroken fixes (among others)

* Mon Oct 27 2008 James Antill <james@fedoraproject.org> - 3.2.20-2
- Fix listTransaction for skipped packages.

* Mon Oct 27 2008 Seth Vidal <skvidal at fedoraproject.org> - 3.2.20-1
- 3.2.20

* Thu Oct 23 2008 Seth Vidal <skvidal at fedoraproject.org> - 3.2.19-6
- update HEAD patch

* Wed Oct 15 2008 Seth Vidal <skvidal at fedoraproject.org> - 3.2.19-5
- rebase against 3.2.X HEAD

* Tue Oct 14 2008 Seth Vidal <skvidal at fedoraproject.org> - 3.2.19-4
- pull patch from git to bring us up to current(ish)

* Wed Sep  3 2008 Seth Vidal <skvidal at fedoraproject.org> - 3.2.19-3
- add patch to fix yum install name.arch matching

* Thu Aug 28 2008 Seth Vidal <skvidal at fedoraproject.org> - 3.2.19-2
- add patch to fix mash's parser use.

* Wed Aug 27 2008 Seth Vidal <skvidal at fedoraproject.org> - 3.2.19-1
- 3.2.19

* Thu Aug  7 2008 Seth Vidal <skvidal at fedoraproject.org> - 3.2.18-1
- 3.2.18

* Wed Jul 10 2008 Seth Vidal <skvidal@fedoraproject.org> - 3.2.17-2
- add patch from upstream for bug in compare_providers

* Wed Jul  9 2008 Seth Vidal <skvidal@fedoraproject.org> - 3.2.17-1
- 3.2.17

* Tue Jun 24 2008 Jesse Keating <jkeating@redhat.com> - 3.2.16-4
- Add a couple more upstream patches for even more multilib fixes

* Tue Jun 24 2008 Jesse Keating <jkeating@redhat.com> - 3.2.16-3
- Add another patch from upstream for multilib policy and noarch

* Sun May 18 2008 Seth Vidal <skvidal at fedoraproject.org> 3.2.16-2
- stupid, stupid, stupid


* Fri May 16 2008 Seth Vidal <skvidal at fedoraproject.org> 3.2.16-1
- 3.2.16

* Tue Apr 15 2008 Seth Vidal <skvidal at fedoraproject.org> 3.2.14-9
- nine is the luckiest number that there will ever be

* Tue Apr 15 2008 Seth Vidal <skvidal at fedoraproject.org> 3.2.14-8
- after many tries - this one fixes translations AND pungi

* Thu Apr 10 2008 Seth Vidal <skvidal at fedoraproject.org> 3.2.14-5
- once more, with feeling

* Thu Apr 10 2008 Seth Vidal <skvidal at fedoraproject.org> 3.2.14-4
- another big-head-patch

* Wed Apr  9 2008 Seth Vidal <skvidal at fedoraproject.org> 3.2.14-3
- apply patch to bring this up to where HEAD is now.

* Tue Apr  8 2008 Seth Vidal <skvidal at fedoraproject.org> 3.2.14-1
- remove committed patch
- obsoletes yum-basearchonly

* Tue Apr  1 2008 Seth Vidal <skvidal at fedoraproject.org> 3.2.13-2
- fix minor typo in comps.py for jkeating

* Thu Mar 20 2008 Seth Vidal <skvidal at fedoraproject.org> 3.2.13-1
- 3.2.13

* Mon Mar 17 2008 Seth Vidal <skvidal at fedoraproject.org> 3.2.12-5
- update manpage patch to close bug 437703. Thakns to Kulbir Saini for the patch


* Fri Mar 14 2008 Seth Vidal <skvidal at fedoraproject.org> 3.2.12-4
- multilib_policy=best is  now the default

* Thu Mar 13 2008 Seth Vidal <skvidal at fedoraproject.org> 
- add jeff sheltren's patch to close rh bug 428825

* Tue Mar  4 2008 Seth Vidal <skvidal at fedoraproject.org> 3.2.12-3
- set failovermethod to 'priority' to make jkeating happy

* Tue Mar  4 2008 Seth Vidal <skvidal at fedoraproject.org> 3.2.12-2
- fix mutually obsoleting providers (like glibc!)

* Mon Mar  3 2008 Seth Vidal <skvidal at fedoraproject.org> - 3.2.12-1
- 3.2.12

* Fri Feb  8 2008 Seth Vidal <skvidal at fedoraproject.org> - 3.2.11-1
- 3.2.11

* Sun Jan 27 2008 James Bowes <jbowes@redhat.com> 3.2.10-3
- Remove yumupd.py

* Fri Jan 25 2008 Seth Vidal <skvidal at fedoraproject.org> - 3.2.10-1
- 3.2.10
- add pygpgme dep

