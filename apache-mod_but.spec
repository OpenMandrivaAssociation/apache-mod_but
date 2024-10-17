#Module-Specific definitions
%define mod_name mod_but
%define mod_conf A44_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Shared Memory / Pre-Authentiation / Reverse Proxy
Name:		apache-%{mod_name}
Version:	3.1
Release:	9
Group:		System/Servers
License:	BSD
URL:		https://www.but.ch/mod_but/
Source0:	http://www.but.ch/mod_but/download/mod_but_latest.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= 2.0.54
Requires(pre):  apache >= 2.0.54
Requires:       apache-conf >= 2.0.54
Requires:       apache >= 2.0.54
BuildRequires:  apache-devel >= 2.0.54
BuildRequires:	file

%description
mod_but is an Apache 2.x module designed to operate as
reverse-proxy enhancement component. mod_but integrates with
mod_rewrite, mod_replace, mod_proxy, mod_security, mod_headers and
other standard modules.

%prep

%setup -q -n mod_but_V%{version}

cp %{SOURCE1} %{mod_conf}

cp modules/mod_but/*.[ch] .

chmod 644 INSTALL LICENSE mod_but_*.pdf

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_bindir}/apxs -c mod_but.c mod_but_access.c mod_but_authorization.c \
    mod_but_config.c mod_but_cookiestore.c mod_but_output_filter.c \
    mod_but_request_filter.c mod_but_session.c mod_but_shm.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}/var/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}/var/www/html/addon-modules/%{name}-%{version}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc INSTALL LICENSE mod_but_*.pdf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
/var/www/html/addon-modules/*




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 3.1-8mdv2012.0
+ Revision: 772599
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 3.1-7
+ Revision: 678285
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 3.1-6mdv2011.0
+ Revision: 587943
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 3.1-5mdv2010.1
+ Revision: 516071
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 3.1-4mdv2010.0
+ Revision: 406555
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 3.1-3mdv2009.0
+ Revision: 234794
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 3.1-2mdv2009.0
+ Revision: 215550
- fix rebuild

* Fri May 09 2008 Oden Eriksson <oeriksson@mandriva.com> 3.1-1mdv2009.0
+ Revision: 205099
- 3.1

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 2.9-4mdv2008.1
+ Revision: 181706
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 2.9-3mdv2008.0
+ Revision: 82538
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 2.9-2mdv2007.1
+ Revision: 140652
- rebuild

* Mon Feb 12 2007 Oden Eriksson <oeriksson@mandriva.com> 2.9-1mdv2007.1
+ Revision: 118917
- 2.9

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.1-2mdv2007.0
+ Revision: 79357
- Import apache-mod_but

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.1-2mdv2007.0
- rebuild

* Wed Mar 29 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.1-1mdk
- 2.2

* Wed Dec 21 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0-1mdk
- initial Mandriva package

