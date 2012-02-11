#Module-Specific definitions
%define mod_name mod_but
%define mod_conf A44_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Shared Memory / Pre-Authentiation / Reverse Proxy
Name:		apache-%{mod_name}
Version:	3.1
Release:	%mkrel 8
Group:		System/Servers
License:	BSD
URL:		http://www.but.ch/mod_but/
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%{_sbindir}/apxs -c mod_but.c mod_but_access.c mod_but_authorization.c \
    mod_but_config.c mod_but_cookiestore.c mod_but_output_filter.c \
    mod_but_request_filter.c mod_but_session.c mod_but_shm.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc INSTALL LICENSE mod_but_*.pdf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
/var/www/html/addon-modules/*


