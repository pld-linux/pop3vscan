# $Revision: #
Summary:	pop3.proxy is an application level gateway for the POP3 protocol
Summary(pl):	pop3.proxy jest aplikacyjn± bramk± dla protoko³u POP3
Name:		pop3vscan
Version:	0.4
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	http://heanet.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz 
# Source0-md5:	9e6bf2493f1c12edaa11c97b7ef8d657
URL:		http://pop3vscan.sf.net
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pop3vscan provides transparent antivirus scanner gateway for the POP3 protocol 

%description -l pl
pop3vscan dostarcza przezroczystej bramki antywirusowej protoko³u POP3.

%prep
%setup -q

%build
%{__make} \
	CC=%{__cc} \
	CFLAGS="%{rpmcflags}"

%{__make} -C ripmime

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1,\
/etc/sysconfig/rc-inetd,/var/spool/pop3vscan}

install stuff/stuff/pop3vscan.rc.suse \
$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/pop3proxy
install %{name}.{mail,conf} $RPM_BUILD_ROOT/etc/
install %{name} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/rc-inetd/pop3proxy
%attr(755,root,root) %{_sbindir}/*
%config %verify(not md5 size mtime) /etc/%{name}.conf
%config %verify(not md5 size mtime) /etc/%{name}.mail
%dir /var/spool/pop3vscan
      
