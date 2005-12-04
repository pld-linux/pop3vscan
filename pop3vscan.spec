Summary:	pop3vscan - an application level gateway for the POP3 protocol
Summary(pl):	pop3vscan - aplikacyjna bramka dla protoko³u POP3
Name:		pop3vscan
Version:	0.4
Release:	1.1
License:	GPL
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/pop3vscan/%{name}-%{version}.tar.gz
# Source0-md5:	48783c81cf70590637993aa0082fa467
Source1:	%{name}.init
Patch0:		%{name}.conf-clamav.patch
URL:		http://pop3vscan.sf.net/
BuildRequires:	pcre-devel
Requires:	pcre
Requires:	rc-scripts
# FIXME: which package in PLD provides 'netfilter' ?
#Requires:	netfilter
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pop3vscan provides transparent antivirus scanner gateway for the POP3
protocol.

%description -l pl
pop3vscan dostarcza przezroczystej bramki antywirusowej dla protoko³u
POP3.

%prep
%setup -q
%patch -p1

%build
rm -fr ripmime/ripmime.a
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},/etc/rc.d/init.d,/var/spool/%{name}}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{name}.{mail,conf} $RPM_BUILD_ROOT%{_sysconfdir}
install %{name} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/%{name} start\" to start inet server" 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.mail
%attr(770,root,mail) %dir /var/spool/%{name}
