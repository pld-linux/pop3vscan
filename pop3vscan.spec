Summary:	pop3.proxy - an application level gateway for the POP3 protocol
Summary(pl):	pop3.proxy - aplikacyjna bramka dla protoko³u POP3
Name:		pop3vscan
Version:	0.4
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz 
Source1:	pop3vscan.init
# Source0-md5:	48783c81cf70590637993aa0082fa467
URL:		http://pop3vscan.sf.net/
PreReq:		rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pop3vscan provides transparent antivirus scanner gateway for the POP3
protocol.

%description -l pl
pop3vscan dostarcza przezroczystej bramki antywirusowej dla protoko³u
POP3.

%prep
%setup -q

%build
%{__make} \
	CC=%{__cc} \
	CFLAGS="%{rpmcflags}"

%{__make} -C ripmime

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},%{_mandir}/man1} \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d/pop3.vscan,/var/spool/pop3vscan}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pop3vscan
install %{name}.{mail,conf} $RPM_BUILD_ROOT%{_sysconfdir}
install %{name} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/pop3vscan ]; then
	/etc/rc.d/init.d/pop3vscan restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/pop3vscan start\" to start inet server" 1>&2
fi

%preun
if [ "$1" = "0" -a -f /var/lock/subsys/pop3vscan ]; then
	/etc/rc.d/init.d/pop3vscan stop
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config %verify(not size mtime md5) /etc/rc.d/init.d/pop3vscan
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}.conf
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}.mail
%dir /var/spool/pop3vscan
