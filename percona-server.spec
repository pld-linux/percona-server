# TODO:
# - mysqldump ... (invalid usage) prints to stdout not stderr (idiotic if you want to create dump and get usage in .sql)
# - http://bugs.mysql.com/bug.php?id=16470
# - innodb are dynamic (= as plugins) ?
# - missing have_archive, have_merge
# - is plugin_dir lib64 safe?
# - Using NDB Cluster... could not find sci transporter in /{include, lib}
# - !!! Makefiles for libmysqld.so !!!
# - segfaults on select from non-mysql user (caused by builder environment):
#     https://bugs.launchpad.net/pld-linux/+bug/381904
#     (profiling disabled temporaily to workaround this)
# NOTE:
# - mysql 'root' user will be 'root' not 'mysql' with 5.7 package
#   this is to make pld consistent what the rest of the world uses.
#
# Conditional build:
%bcond_with	autodeps	# BR packages needed only for resolving deps
%bcond_without	innodb		# InnoDB storage engine support
%bcond_without	big_tables	# Support tables with more than 4G rows even on 32 bit platforms
%bcond_without	federated	# Federated storage engine support
%bcond_without	raid		# RAID support
%bcond_without	ssl		# OpenSSL support
%bcond_with	systemtap	# systemtap/dtrace probes
%bcond_without	tcpd		# libwrap (tcp_wrappers) support
%bcond_without	sphinx		# Sphinx storage engine support
%bcond_without	tokudb		# TokuDB
%bcond_without	rocksdb		# RocksDB
# mysql needs boost 1.59.0 and doesn't support newer/older boost versions
%bcond_with	system_boost	# Use system boost package
%bcond_with	tests		# FIXME: don't run correctly
%bcond_with	ndb		# NDB is now a separate product, this here is broken, so disable it
%bcond_without	coredumper	# coredumper support

# tokudb is only supported on x86_64
%ifnarch %{x8664}
%undefine	with_rocksdb
%undefine	with_tokudb
%endif

%ifarch x32
%undefine	with_coredumper
%endif

%define		rel	1
%define		percona_git_rel	52
%define		percona_rel	48
Summary:	Percona Server: a very fast and reliable SQL database engine
Summary(de.UTF-8):	Percona Server: ist eine SQL-Datenbank
Summary(fr.UTF-8):	Percona Server: un serveur SQL rapide et fiable
Summary(pl.UTF-8):	Percona Server: bardzo szybka i niezawodna baza danych (SQL)
Summary(pt_BR.UTF-8):	Percona Server: Um servidor SQL rápido e confiável
Summary(ru.UTF-8):	Percona Server - быстрый SQL-сервер
Summary(uk.UTF-8):	Percona Server - швидкий SQL-сервер
Summary(zh_CN.UTF-8):	Percona Server数据库服务器
Name:		percona-server
Version:	5.7.44
Release:	%{percona_git_rel}.%{rel}
License:	GPL + Percona Server FLOSS Exception
Group:		Applications/Databases
Source0:	https://downloads.percona.com/downloads/Percona-Server-5.7/LATEST/source/tarball/%{name}-%{version}-%{percona_rel}.tar.gz
# Source0-md5:	f530424ced878ee9e9c430e13ce3fe33
Source100:	http://www.sphinxsearch.com/files/sphinx-2.2.11-release.tar.gz
# Source100-md5:	5cac34f3d78a9d612ca4301abfcbd666
%if %{without system_boost}
Source101:      http://downloads.sourceforge.net/boost/boost_1_59_0.tar.bz2
# Source101-md5:	6aa9a5c6a4ca1016edd0ed1178e3cb87
%endif
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Source4:	mysqld.conf
Source5:	%{name}-clusters.conf
Source7:	%{name}-ndb.init
Source8:	%{name}-ndb.sysconfig
Source9:	%{name}-ndb-mgm.init
Source10:	%{name}-ndb-mgm.sysconfig
Source11:	%{name}-ndb-cpc.init
Source12:	%{name}-ndb-cpc.sysconfig
Source13:	%{name}-client.conf
Source14:	my.cnf
Patch100:	percona-server-git.patch
# Patch100-md5:	bd4d4d8f219788e9b186bd4f343b70d9
Patch0:		mysql-opt.patch
Patch1:		mysql-versioning.patch
Patch2:		mysql-protobuf.patch
Patch3:		build.patch
Patch4:		mysql-sphinx.patch
# https://github.com/sphinxsearch/sphinx/pull/32/
Patch5:		mysql-5.7-sphinx.patch
Patch6:		mysql-chain-certs.patch
# from fedora
Patch7:		mysql-dubious-exports.patch
Patch8:		mysql-cmake.patch
URL:		https://www.percona.com/software/mysql-database/percona-server
BuildRequires:	bison >= 1.875
BuildRequires:	cmake >= 2.8.2
BuildRequires:	curl-devel
BuildRequires:	readline-devel >= 6.2
BuildRequires:	libevent-devel
BuildRequires:	libstdc++-devel >= 5:4.0
BuildRequires:	automake
%{?with_system_boost:BuildRequires:	boost-devel = 1.59.0}
BuildRequires:	libhsclient-devel
%{?with_tcpd:BuildRequires:	libwrap-devel}
BuildRequires:	mecab-devel
BuildRequires:	ncurses-devel >= 4.2
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7d}
BuildRequires:	pam-devel
%{?with_autodeps:BuildRequires:	perl-DBI}
BuildRequires:	perl-devel >= 1:5.6.1
BuildRequires:	protobuf-devel
BuildRequires:	python-modules
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.597
BuildRequires:	sed >= 4.0
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-charsets = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	/usr/bin/setsid
Requires:	rc-scripts >= 0.2.0
Suggests:	percona-server-client
%{?with_tcpd:Suggests:	tcp_wrappers}
Suggests:	vim-syntax-mycnf
Provides:	MySQL-server
Provides:	group(mysql)
Provides:	msqlormysql
Provides:	user(mysql)
Obsoletes:	MySQL < 3.22.27
Obsoletes:	mysql-server
Conflicts:	logrotate < 3.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_sbindir}
%define		_localstatedir	/var/lib/mysql
%define		_perconahome	/home/services/%{name}

%description
Percona Server is a true multi-user, multi-threaded SQL (Structured
Query Language) database server. SQL is the most popular database
language in the world. Percona Server is a client/server
implementation that consists of a server daemon mysqld and many
different client programs/libraries.

The main goals of Percona Server are speed, robustness and easy to
use. Percona Server was originally developed because we at Tcx needed
a SQL server that could handle very big databases with magnitude
higher speed than what any database vendor could offer to us. We have
now been using Percona Server since 1996 in a environment with more
than 40 databases, 10,000 tables, of which more than 500 have more
than 7 million rows. This is about 50G of mission critical data.

The base upon which Percona Server is built is a set of routines that
have been used in a highly demanding production environment for many
years. While Percona Server is still in development, it already offers
a rich and highly useful function set.

%description -l fr.UTF-8
Percona Server est un serveur de bases de donnees SQL vraiment
multi-usagers et multi-taches. Le langage SQL est le langage de bases
de donnees le plus populaire au monde. Percona Server est une
implementation client/serveur qui consiste en un serveur (mysqld) et
differents programmes/bibliotheques clientes.

Les objectifs principaux de Percona Server sont: vitesse, robustesse
et facilite d'utilisation. Percona Server fut originalement developpe
parce que nous, chez Tcx, avions besoin d'un serveur SQL qui pouvait
gerer de tres grandes bases de donnees avec une vitesse d'un ordre de
magnitude superieur a ce que n'importe quel vendeur pouvait nous
offrir. Nous utilisons Percona Server depuis 1996 dans un
environnement avec plus de 40 bases de donnees, 10000 tables,
desquelles plus de 500 ont plus de 7 millions de lignes. Ceci
represente environ 50G de donnees critiques.

A la base de la conception de Percona Server, on retrouve une serie de
routines qui ont ete utilisees dans un environnement de production
pendant plusieurs annees. Meme si Percona Server est encore en
developpement, il offre deja une riche et utile serie de fonctions.

%description -l pl.UTF-8
Percona Server to prawdziwie wieloużytkownikowy, wielowątkowy serwer
baz danych SQL. SQL jest najpopularniejszym na świecie językiem
używanym do baz danych. Percona Server to implementacja klient/serwer
składająca się z demona mysqld i wielu różnych programów i bibliotek
klienckich.

Głównymi celami Percona Server-a są szybkość, potęga i łatwość
użytkowania. Percona Server oryginalnie był tworzony, ponieważ autorzy
w Tcx potrzebowali serwera SQL do obsługi bardzo dużych baz danych z
szybkością o wiele większą, niż mogli zaoferować inni producenci baz
danych. Używają go od 1996 roku w środowisku z ponad 40 bazami danych,
10 000 tabel, z których ponad 500 zawiera ponad 7 milionów rekordów -
w sumie około 50GB krytycznych danych.

Baza, na której oparty jest Percona Server, składa się ze zbioru
procedur, które były używane w bardzo wymagającym środowisku
produkcyjnym przez wiele lat. Pomimo, że Percona Server jest ciągle
rozwijany, już oferuje bogaty i użyteczny zbiór funkcji.

%description -l de.UTF-8
Percona Server ist eine SQL-Datenbank. Allerdings ist sie im Gegensatz
zu Oracle, DB2 oder PostgreSQL keine relationale Datenbank. Die Daten
werden zwar in zweidimensionalen Tabellen gespeichert und können mit
einem Primärschlüssel versehen werden. Es ist aber keine Definition
eines Fremdschlüssels möglich. Der Benutzer ist somit bei einer
Percona Server-Datenbank völlig allein für die (referenzielle)
Integrität der Daten verantwortlich. Allein durch die Nutzung externer
Tabellenformate, wie InnoDB bzw Berkeley DB wird eine Relationalität
ermöglicht. Diese Projekte sind aber getrennt von Percona Server zu
betrachten.

%description -l pt_BR.UTF-8
O Percona Server é um servidor de banco de dados SQL realmente
multiusuário e multi-tarefa. A linguagem SQL é a mais popular
linguagem para banco de dados no mundo. O Percona Server é uma
implementação cliente/servidor que consiste de um servidor chamado
mysqld e diversos programas/bibliotecas clientes. Os principais
objetivos do Percona Server são: velocidade, robustez e facilidade de
uso. O Percona Server foi originalmente desenvolvido porque nós na Tcx
precisávamos de um servidor SQL que pudesse lidar com grandes bases de
dados e com uma velocidade muito maior do que a que qualquer vendedor
podia nos oferecer. Estamos usando o Percona Server desde 1996 em um
ambiente com mais de 40 bases de dados com 10.000 tabelas, das quais
mais de 500 têm mais de 7 milhões de linhas. Isto é o equivalente a
aproximadamente 50G de dados críticos. A base da construção do Percona
Server é uma série de rotinas que foram usadas em um ambiente de
produção com alta demanda por muitos anos. Mesmo o Percona Server
estando ainda em desenvolvimento, ele já oferece um conjunto de
funções muito ricas e úteis. Veja a documentação para maiores
informações.

%description -l ru.UTF-8
Percona Server - это SQL (Structured Query Language) сервер базы
данных. Percona Server была написана Michael'ом (monty) Widenius'ом.
См. файл CREDITS в дистрибутиве на предмет других участников проекта и
прочей информации о Percona Server.

%description -l uk.UTF-8
Percona Server - це SQL (Structured Query Language) сервер бази даних.
Percona Server було написано Michael'ом (monty) Widenius'ом. Див. файл
CREDITS в дистрибутиві для інформації про інших учасників проекту та
іншої інформації.

%package charsets
Summary:	Percona Server - character sets definitions
Summary(pl.UTF-8):	Percona Server - definicje kodowań znaków
Group:		Applications/Databases

%description charsets
This package contains character sets definitions needed by both client
and server.

%description charsets -l pl.UTF-8
Ten pakiet zawiera definicje kodowań znaków potrzebne dla serwera i
klienta.

%package extras
Summary:	Percona Server additional utilities
Summary(pl.UTF-8):	Dodatkowe narzędzia do Percona Server
Group:		Applications/Databases
Requires:	%{name}-client = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}

%description extras
Percona Server additional utilities except Perl scripts (they may be
found in %{name}-extras-perl package).

%description extras -l pl.UTF-8
Dodatkowe narzędzia do Percona Server - z wyjątkiem skryptów Perla
(które są w pakiecie %{name}-extras-perl).

%package extras-perl
Summary:	Percona Server additional utilities written in Perl
Summary(pl.UTF-8):	Dodatkowe narzędzia do Percona Server napisane w Perlu
Group:		Applications/Databases
Requires:	%{name}-extras = %{version}-%{release}
Requires:	perl-DBD-mysql

%description extras-perl
Percona Server additional utilities written in Perl.

%description extras-perl -l pl.UTF-8
Dodatkowe narzędzia do Percona Server napisane w Perlu.

%package client
Summary:	Percona Server - Client
Summary(pl.UTF-8):	Percona Server - Klient
Summary(pt.UTF-8):	Percona Server - Cliente
Summary(ru.UTF-8):	Percona Server клиент
Summary(uk.UTF-8):	Percona Server клієнт
Group:		Applications/Databases
Requires:	%{name}-charsets = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	readline >= 6.2
Obsoletes:	MySQL-client < 3.22.27

%description client
This package contains the standard Percona Server clients.

%description client -l fr.UTF-8
Ce package contient les clients Percona Server standards.

%description client -l pl.UTF-8
Standardowe programy klienckie Percona Server.

%description client -l pt_BR.UTF-8
Este pacote contém os clientes padrão para o Percona Server.

%description client -l ru.UTF-8
Этот пакет содержит только клиент Percona Server.

%description client -l uk.UTF-8
Цей пакет містить тільки клієнта Percona Server.

%package libs
Summary:	Shared libraries for Percona Server
Summary(pl.UTF-8):	Biblioteki współdzielone Percona Server
Group:		Libraries
Obsoletes:	libmysql10 < 4
Obsoletes:	mysql-doc < 4.1.12

%description libs
Shared libraries for Percona Server.

%description libs -l pl.UTF-8
Biblioteki współdzielone Percona Server.

%package devel
Summary:	Percona Server - development header files and other files
Summary(pl.UTF-8):	Percona Server - Pliki nagłówkowe i inne dla programistów
Summary(pt.UTF-8):	Percona Server - Medições de desempenho
Summary(ru.UTF-8):	Percona Server - хедеры и библиотеки разработчика
Summary(uk.UTF-8):	Percona Server - хедери та бібліотеки програміста
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_ssl:Requires: openssl-devel}
Requires:	zlib-devel
Obsoletes:	MySQL-devel < 3.22.27
Obsoletes:	libmysql10-devel < 4
Obsoletes:	webscalesql-devel

%description devel
This package contains the development header files and other files
necessary to develop Percona Server client applications.

%description devel -l fr.UTF-8
Ce package contient les fichiers entetes et les librairies de
developpement necessaires pour developper des applications clientes
Percona Server.

%description devel -l pl.UTF-8
Pliki nagłówkowe i inne pliki konieczne do kompilacji aplikacji
klienckich Percona Server.

%description devel -l pt_BR.UTF-8
Este pacote contém os arquivos de cabeçalho (header files) e
bibliotecas necessárias para desenvolver aplicações clientes do
Percona Server.

%description devel -l ru.UTF-8
Этот пакет содержит хедеры и библиотеки разработчика, необходимые для
разработки клиентских приложений.

%description devel -l uk.UTF-8
Цей пакет містить хедери та бібліотеки програміста, необхідні для
розробки програм-клієнтів.

%package static
Summary:	Percona Server static libraries
Summary(pl.UTF-8):	Biblioteki statyczne Percona Server
Summary(ru.UTF-8):	Percona Server - статические библиотеки
Summary(uk.UTF-8):	Percona Server - статичні бібліотеки
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	MySQL-static < 3.22.27

%description static
Percona Server static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne Percona Server.

%description static -l ru.UTF-8
Этот пакет содержит статические библиотеки разработчика, необходимые
для разработки клиентских приложений.

%description static -l uk.UTF-8
Цей пакет містить статичні бібліотеки програміста, необхідні для
розробки програм-клієнтів.

%package bench
Summary:	Percona Server - Benchmarks
Summary(pl.UTF-8):	Percona Server - Programy testujące szybkość działania bazy
Summary(pt.UTF-8):	Percona Server - Medições de desempenho
Summary(ru.UTF-8):	Percona Server - бенчмарки
Summary(uk.UTF-8):	Percona Server - бенчмарки
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-client
Requires:	perl(DBD::mysql)
Obsoletes:	MySQL-bench < 3.22.27

%description bench
This package contains Percona Server benchmark scripts and data.

%description bench -l pl.UTF-8
Programy testujące szybkość serwera Percona Server.

%description bench -l pt_BR.UTF-8
Este pacote contém medições de desempenho de scripts e dados do
Percona Server.

%description bench -l ru.UTF-8
Этот пакет содержит скрипты и данные для оценки производительности
Percona Server.

%description bench -l uk.UTF-8
Цей пакет містить скрипти та дані для оцінки продуктивності Percona
Server.

%package ndb
Summary:	Percona Server - NDB Storage Engine Daemon
Summary(pl.UTF-8):	Percona Server - demon silnika przechowywania danych NDB
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb
This package contains the standard Percona Server NDB Storage Engine
Daemon.

%description ndb -l pl.UTF-8
Ten pakiet zawiera standardowego demona silnika przechowywania danych
NDB.

%package ndb-client
Summary:	Percona Server - NDB Clients
Summary(pl.UTF-8):	Percona Server - programy klienckie NDB
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb-client
This package contains the standard Percona Server NDB Clients.

%description ndb-client -l pl.UTF-8
Ten pakiet zawiera standardowe programy klienckie Percona Server NDB.

%package ndb-mgm
Summary:	Percona Server - NDB Management Daemon
Summary(pl.UTF-8):	Percona Server - demon zarządzający NDB
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb-mgm
This package contains the standard Percona Server NDB Management
Daemon.

%description ndb-mgm -l pl.UTF-8
Ten pakiet zawiera standardowego demona zarządzającego Percona Server
NDB.

%package ndb-cpc
Summary:	Percona Server - NDB CPC Daemon
Summary(pl.UTF-8):	Percona Server - demon NDB CPC
Group:		Applications/Databases
Requires:	%{name}-libs = %{version}-%{release}

%description ndb-cpc
This package contains the standard Percona Server NDB CPC Daemon.

%description ndb-cpc -l pl.UTF-8
Ten pakiet zawiera standardowego demona Percona Server NDB CPC.

%prep
%setup -q -n %{name}-%{version}-%{percona_rel} %{?with_sphinx:-a100} %{!?with_system_boost:-a101}
%patch -P100 -p1
%patch -P0 -p1
%if %{with sphinx}
# http://www.sphinxsearch.com/docs/manual-0.9.9.html#sphinxse-mysql51
%{__mv} sphinx-*/mysqlse storage/sphinx
%patch -P4 -p1
cd storage/sphinx
%patch -P5 -p2
cd ../..
%endif
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1

# to get these files rebuild
[ -f sql/sql_yacc.cc ] && %{__rm} sql/sql_yacc.cc
[ -f sql/sql_yacc.h ] && %{__rm} sql/sql_yacc.h

# map has more sane versioning that default "global everything" in ver.in
#cp -p libmysql/libmysql.map libmysql/libmysql.ver.in

%build
install -d build
cd build
# NOTE that /var/lib/mysql/mysql.sock is symlink to real sock file
# (it defaults to first cluster but user may change it to whatever
# cluster it wants)

%if "%{cc_version}" >= "7.0"
FALLTHROUGH_OPT="-Wimplicit-fallthrough=0"
%else
FALLTHROUGH_OPT=
%endif

CPPFLAGS="%{rpmcppflags}" \
%cmake .. \
	-DCMAKE_BUILD_TYPE=%{!?debug:RelWithDebInfo}%{?debug:Debug} \
	-DCMAKE_C_FLAGS_DEBUG="-fno-omit-frame-pointer -fno-strict-aliasing $FALLTHROUGH_OPT" \
	-DCMAKE_CXX_FLAGS_DEBUG="-fno-omit-frame-pointer -fno-strict-aliasing $FALLTHROUGH_OPT" \
	-DCMAKE_C_FLAGS_RELWITHDEBINFO="%{rpmcflags} -DNDEBUG -fno-omit-frame-pointer -fno-strict-aliasing $FALLTHROUGH_OPT -Wno-shadow" \
	-DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{rpmcxxflags} -DNDEBUG -fno-omit-frame-pointer -fno-strict-aliasing $FALLTHROUGH_OPT -Wno-shadow" \
	-DCOMPILATION_COMMENT="PLD/Linux Distribution Percona Server RPM" \
	-DCURSES_INCLUDE_PATH=/usr/include/ncurses \
	%{?with_systemtap:-DENABLE_DTRACE=ON} \
	-DALLOW_NO_SSE42=ON \
	-DFEATURE_SET="community" \
	-DINSTALL_LAYOUT=RPM \
	-DINSTALL_LIBDIR=%{_lib} \
	-DINSTALL_MYSQLTESTDIR_RPM="" \
	-DINSTALL_PLUGINDIR=%{_lib}/%{name}/plugin \
	-DINSTALL_SQLBENCHDIR=%{_datadir} \
	-DINSTALL_SUPPORTFILESDIR=share/%{name}-support \
	-DINSTALL_MYSQLSHAREDIR=share/%{name} \
	-DINSTALL_SECURE_FILE_PRIVDIR="" \
	-DMYSQL_UNIX_ADDR=/var/lib/mysql/mysql.sock \
	%{?debug:-DWITH_DEBUG=ON} \
	-DWITHOUT_EXAMPLE_STORAGE_ENGINE=1 \
	-DWITH_FAST_MUTEXES=ON \
	-DWITH_LIBWRAP=%{?with_tcpd:ON}%{!?with_tcpd:OFF} \
	-DWITH_PAM=ON \
	-DWITH_PERFSCHEMA_STORAGE_ENGINE=1 \
	-DWITH_PIC=ON \
	-DWITH_SCALABILITY_METRICS=ON \
	-DWITH_SSL=%{?with_ssl:system}%{!?with_ssl:no} \
	-DWITH_UNIT_TESTS=%{?with_tests:ON}%{!?with_tests:OFF} \
	-DWITH_COREDUMPER=%{?with_coredumper:ON}%{!?with_coredumper:OFF} \
	%{!?with_tokudb:-DWITHOUT_TOKUDB=ON} \
	%{!?with_rocksdb:-DWITHOUT_ROCKSDB=ON} \
%if %{without system_boost}
	%{!?with_system_boost:-DWITH_BOOST="$(pwd)/$(ls -1d ../boost_*)"} \
%endif
	-DWITH_LIBEVENT=system \
	-DWITH_LZ4=system \
	-DWITH_MECAB=system \
	-DWITH_PROTOBUF=system \
	-DWITH_READLINE=system \
	-DWITH_ZLIB=system \
	-DTMPDIR=/var/tmp

%{__make}

%if %{with tests}
%{__make} test

cd mysql-test

MTR_BINDIR=$(pwd)/../build/ \
%{__perl} ./mysql-test-run.pl \
	--force \
	--retry=0 \
	--ssl \
	--suite-timeout=720 \
	--testcase-timeout=30 \
	--mysqld=--binlog-format=mixed \
	--force-restart \
	--shutdown-timeout=60 \
	--max-test-fail=0 \
	--big-test \
	--skip-test-list=unstable-tests
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,sysconfig,%{name},skel} \
	   $RPM_BUILD_ROOT/var/{log/{archive,}/%{name},lib/mysql} \
	   $RPM_BUILD_ROOT%{_perconahome} \
	   $RPM_BUILD_ROOT%{_libdir}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -a %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
# This is template for configuration file which is created after 'service mysql init'
cp -a %{SOURCE4} mysqld.conf
cp -a %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/clusters.conf
touch $RPM_BUILD_ROOT/var/log/%{name}/{mysqld,query,slow}.log

# remove innodb directives from mysqld.conf if mysqld is configured without
%if %{without innodb}
	cp mysqld.conf mysqld.tmp
	awk 'BEGIN { RS="\n\n" } !/innodb/ { printf("%s\n\n", $0) }' < mysqld.tmp > mysqld.conf
%endif

# remove berkeley-db directives from mysqld.conf if mysqld is configured without
cp mysqld.conf mysqld.tmp
awk 'BEGIN { RS="\n\n" } !/bdb/ { printf("%s\n\n", $0) }' < mysqld.tmp > mysqld.conf

cp -a mysqld.conf $RPM_BUILD_ROOT%{_datadir}/%{name}/mysqld.conf
cp -a %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/mysql-client.conf
ln -s mysql-client.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/my.cnf
cp -a %{SOURCE14} $RPM_BUILD_ROOT/etc/skel/.my.cnf

# NDB
%if %{with ndb}
install -p %{SOURCE7} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-ndb
cp -a %{SOURCE8} $RPM_BUILD_ROOT/etc/sysconfig/%{name}-ndb
install -p %{SOURCE9} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-ndb-mgm
cp -a %{SOURCE10} $RPM_BUILD_ROOT/etc/sysconfig/%{name}-ndb-mgm
install -p %{SOURCE11} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-ndb-cpc
cp -a %{SOURCE12} $RPM_BUILD_ROOT/etc/sysconfig/%{name}-ndb-cpc
%endif

sed -i -e 's,/usr//usr,%{_prefix},g' $RPM_BUILD_ROOT%{_bindir}/mysql_config
sed -i -e '/libs/s/$ldflags//' $RPM_BUILD_ROOT%{_bindir}/mysql_config
sed -i -e '/libs/s/-lprobes_mysql//' $RPM_BUILD_ROOT%{_bindir}/mysql_config

# remove known unpackaged files
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}-support

# rename not to be so generic name
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{,mysql_}resolve_stack_dump
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man1/{,mysql_}resolve_stack_dump.1

# not useful without -debug build
%{!?debug:%{__rm} $RPM_BUILD_ROOT%{_bindir}/mysql_resolve_stack_dump}
%{!?debug:%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysql_resolve_stack_dump.1}
# generate symbols file, so one can generate backtrace using it
# mysql_resolve_stack_dump -s %{_datadir}/%{name}/mysqld.sym -n mysqld.stack.
# http://dev.mysql.com/doc/refman/5.0/en/using-stack-trace.html
%{?debug:nm -n $RPM_BUILD_ROOT%{_sbindir}/mysqld > $RPM_BUILD_ROOT%{_datadir}/%{name}/mysqld.sym}

# do not clobber users $PATH
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/mysql_plugin
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/mysql_upgrade
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/innochecksum
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/myisamchk
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/myisamlog
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/myisampack
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/my_print_defaults
sed -i -e 's#/usr/bin/my_print_defaults#%{_sbindir}/my_print_defaults#g' $RPM_BUILD_ROOT%{_bindir}/mysql_install_db
%{__mv} $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/mysqlcheck

# delete - functionality in initscript / rpm
# note: mysql_install_db (and thus resolveip) are needed by digikam
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mysqld_safe
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mysqld_multi
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysqld_{multi,safe}*
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/errmsg-utf8.txt
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysql.server*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mysqlman.1*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/comp_err.1*

# we don't package those (we have no -test or -testsuite pkg) and some of them just segfault
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mysql_client_test
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mysqlxtest
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/mysql-test
# libmysqld examples
%{__rm} $RPM_BUILD_ROOT%{_bindir}/mysql{_client_test_embedded,_embedded,test_embedded}
%if %{with coredumper}
# bundled coredumper library (with mistaken paths)
%{__rm} $RPM_BUILD_ROOT%{_prefix}/lib/libcoredumper.a
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/coredumper
%{__rm} $RPM_BUILD_ROOT%{_prefix}/cmake/coredumper*.cmake
%endif
%if %{with tokudb}
# some junk from tokudb
%{__rm} $RPM_BUILD_ROOT%{_prefix}/{COPYING.AGPLv3,COPYING.GPLv2,PATENTS,README.md}
%{__rm} $RPM_BUILD_ROOT%{_includedir}/backup.h
%endif

# not needed
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/libdaemon_example.*
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/daemon_example.ini
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/plugin/udf_example.so

# not an .info file
%{__rm} $RPM_BUILD_ROOT%{_infodir}/mysql.info

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 89 mysql
%useradd -u 89 -d %{_perconahome} -s /bin/false -g mysql -c "Percona Server" mysql

%post
/sbin/ldconfig
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%userremove mysql
	%groupremove mysql
fi

%post ndb
/sbin/chkconfig --add %{name}-ndb
%service %{name}-ndb restart "%{name} NDB engine"

%preun ndb
if [ "$1" = "0" ]; then
	%service %{name}-ndb stop
	/sbin/chkconfig --del %{name}-ndb
fi

%post ndb-mgm
/sbin/chkconfig --add %{name}-ndb-mgm
%service %{name}-ndb-mgm restart "%{name} NDB management node"

%preun ndb-mgm
if [ "$1" = "0" ]; then
	%service %{name}-ndb-mgm stop
	/sbin/chkconfig --del %{name}-ndb-mgm
fi

%post ndb-cpc
/sbin/chkconfig --add %{name}-ndb-cpc
%service %{name}-ndb-cpc restart "mysql NDB CPC"

%preun ndb-cpc
if [ "$1" = "0" ]; then
	%service %{name}-ndb-cpc stop
	/sbin/chkconfig --del %{name}-ndb-cpc
fi

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc build-ps/rpm/*.cnf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,mysql) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/clusters.conf
%attr(755,root,root) %{_bindir}/ps_mysqld_helper
%attr(755,root,root) %{_bindir}/ps_tokudb_admin
%attr(755,root,root) %{_bindir}/ps-admin
%attr(755,root,root) %{_sbindir}/innochecksum
%attr(755,root,root) %{_sbindir}/my_print_defaults
%attr(755,root,root) %{_sbindir}/myisamchk
%attr(755,root,root) %{_sbindir}/myisamlog
%attr(755,root,root) %{_sbindir}/myisampack
%attr(755,root,root) %{_sbindir}/mysql_plugin
%attr(755,root,root) %{_sbindir}/mysql_upgrade
%attr(755,root,root) %{_sbindir}/mysqlcheck
%attr(755,root,root) %{_sbindir}/mysqld
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugin
%attr(755,root,root) %{_libdir}/%{name}/plugin/adt_null.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/audit_log.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/auth_pam_compat.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/auth_pam.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/auth.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/auth_socket.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/auth_test_plugin.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/authentication_ldap_sasl_client.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/connection_control.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/data_masking.so
%{_libdir}/%{name}/plugin/data_masking.ini
%attr(755,root,root) %{_libdir}/%{name}/plugin/dialog.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/group_replication.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/keyring_file.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/keyring_udf.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/keyring_vault.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libpluginmecab.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libfnv1a_udf.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libfnv_udf.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libmurmur_udf.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_framework.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_services.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_services_threaded.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_session_detach.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_session_info.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_session_in_thd.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_sql_2_sessions.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_sql_all_col_types.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_sql_cmds_1.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_sql_commit.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_sql_complex.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_sql_errors.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_sql_lock.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_sql_processlist.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_sql_replication.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_sql_shutdown.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_sql_sqlmode.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_sql_stored_procedures_functions.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_sql_views_triggers.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_x_sessions_deinit.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/libtest_x_sessions_init.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/locking_service.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/mypluglib.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/mysql_no_login.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/mysqlx.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/qa_auth_client.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/qa_auth_interface.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/qa_auth_server.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/query_response_time.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/replication_observers_example_plugin.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/rewrite_example.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/rewriter.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/scalability_metrics.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/semisync_master.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/semisync_slave.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/test_security_context.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/test_udf_services.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/validate_password.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/version_token.so
%if %{with sphinx}
%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_sphinx.so
%endif
%if %{with tokudb}
%attr(755,root,root) %{_bindir}/tokuft_logprint
%attr(755,root,root) %{_bindir}/tokuftdump
%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_tokudb.so
%attr(755,root,root) %{_libdir}/%{name}/plugin/tokudb_backup.so
%attr(755,root,root) %{_libdir}/libHotBackup.so
%endif
%if %{with rocksdb}
%attr(755,root,root) %{_bindir}/ldb
%attr(755,root,root) %{_bindir}/mysql_ldb
%attr(755,root,root) %{_bindir}/sst_dump
%attr(755,root,root) %{_libdir}/%{name}/plugin/ha_rocksdb.so
%endif
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/my_print_defaults.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/mysql_plugin.1*
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man8/mysqld.8*

%if %{?debug:1}0
%attr(755,root,root) %{_bindir}/*resolve_stack_dump
%{_datadir}/%{name}/mysqld.sym
%{_mandir}/man1/*resolve_stack_dump.1*
%endif

%attr(700,mysql,mysql) %{_perconahome}
# root:root is proper here for mysql.rpm while mysql:mysql is potential security hole
%attr(751,root,root) /var/lib/mysql
%attr(750,mysql,mysql) %dir /var/log/%{name}
%attr(750,mysql,mysql) %dir /var/log/archive/%{name}
%attr(640,mysql,mysql) %ghost /var/log/%{name}/*

# This is template for configuration file which is created after 'service mysql init'
%{_datadir}/%{name}/mysqld.conf
%{_datadir}/%{name}/install_rewriter.sql
%{_datadir}/%{name}/mysql_security_commands.sql
%{_datadir}/%{name}/mysql_sys_schema.sql
%{_datadir}/%{name}/mysql_system_tables.sql
%{_datadir}/%{name}/mysql_system_tables_data.sql
%{_datadir}/%{name}/mysql_test_data_timezone.sql
%{_datadir}/%{name}/uninstall_rewriter.sql

%{_datadir}/%{name}/english
%{_datadir}/%{name}/dictionary.txt
%{_datadir}/%{name}/fill_help_tables.sql
%{_datadir}/%{name}/innodb_memcached_config.sql
# Don't mark these with %%lang. These are used depending
# on database client settings.
%{_datadir}/%{name}/bulgarian
%{_datadir}/%{name}/czech
%{_datadir}/%{name}/danish
%{_datadir}/%{name}/german
%{_datadir}/%{name}/greek
%{_datadir}/%{name}/spanish
%{_datadir}/%{name}/estonian
%{_datadir}/%{name}/french
%{_datadir}/%{name}/hungarian
%{_datadir}/%{name}/italian
%{_datadir}/%{name}/japanese
%{_datadir}/%{name}/korean
%{_datadir}/%{name}/dutch
%{_datadir}/%{name}/norwegian
%{_datadir}/%{name}/norwegian-ny
%{_datadir}/%{name}/polish
%{_datadir}/%{name}/portuguese
%{_datadir}/%{name}/romanian
%{_datadir}/%{name}/russian
%{_datadir}/%{name}/serbian
%{_datadir}/%{name}/slovak
%{_datadir}/%{name}/swedish
%{_datadir}/%{name}/ukrainian

%files charsets
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/charsets

%files extras
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/myisam_ftdump
%attr(755,root,root) %{_bindir}/mysql_install_db
%attr(755,root,root) %{_bindir}/mysql_secure_installation
%attr(755,root,root) %{_bindir}/mysql_tzinfo_to_sql
%attr(755,root,root) %{_bindir}/perror
%attr(755,root,root) %{_bindir}/replace
%attr(755,root,root) %{_bindir}/resolveip
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/mysql_install_db.1*
%{_mandir}/man1/mysql_secure_installation.1*
%{_mandir}/man1/mysql_tzinfo_to_sql.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/resolveip.1*

%files extras-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysqldumpslow
%{_mandir}/man1/mysqldumpslow.1*

%files client
%defattr(644,root,root,755)
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/skel/.my.cnf
%attr(755,root,root) %{_bindir}/lz4_decompress
%attr(755,root,root) %{_bindir}/mysql
%attr(755,root,root) %{_bindir}/mysql_config_editor
%attr(755,root,root) %{_bindir}/mysql_ssl_rsa_setup
%attr(755,root,root) %{_bindir}/mysqladmin
%attr(755,root,root) %{_bindir}/mysqlbinlog
%attr(755,root,root) %{_bindir}/mysqldump
%attr(755,root,root) %{_bindir}/mysqlimport
%attr(755,root,root) %{_bindir}/mysqlpump
%attr(755,root,root) %{_bindir}/mysqlshow
%attr(755,root,root) %{_bindir}/zlib_decompress
%{_mandir}/man1/lz4_decompress.1*
%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysql_config_editor.1*
%{_mandir}/man1/mysql_ssl_rsa_setup.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlpump.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/zlib_decompress.1*

%files libs
%defattr(644,root,root,755)
%attr(751,root,root) %dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/mysql-client.conf
%{_sysconfdir}/%{name}/my.cnf
%attr(755,root,root) %{_libdir}/libperconaserverclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libperconaserverclient.so.20
%if %{with ndb}
%attr(755,root,root) %{_libdir}/libndbclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndbclient.so.3
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql_config
%attr(755,root,root) %{_libdir}/libperconaserverclient.so
%{_pkgconfigdir}/perconaserverclient.pc
%if %{with ndb}
%attr(755,root,root) %{_libdir}/libndbclient.so
%endif
# static-only so far
%{_libdir}/libmysqld.a
%{_libdir}/libmysqlservices.a
%{_includedir}/mysql
%{_aclocaldir}/mysql.m4
%{_mandir}/man1/mysql_config.1*

%files static
%defattr(644,root,root,755)
%{_libdir}/libperconaserverclient.a
%if %{with ndb}
%{_libdir}/libndbclient.a
%endif

%files bench
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysqlslap
%attr(755,root,root) %{_bindir}/mysqltest
%{_mandir}/man1/mysqlslap.1*

%if %{with ndb}
%files ndb
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndbd
%attr(754,root,root) /etc/rc.d/init.d/%{name}-ndb
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}-ndb
%{_mandir}/man1/ndbd_redo_log_reader.1*
%{_mandir}/man8/ndbd.8*

%files ndb-client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ndb_config
%attr(755,root,root) %{_bindir}/ndb_delete_all
%attr(755,root,root) %{_bindir}/ndb_desc
%attr(755,root,root) %{_bindir}/ndb_drop_index
%attr(755,root,root) %{_bindir}/ndb_drop_table
%attr(755,root,root) %{_bindir}/ndb_error_reporter
%attr(755,root,root) %{_bindir}/ndb_mgm
%attr(755,root,root) %{_bindir}/ndb_print_backup_file
%attr(755,root,root) %{_bindir}/ndb_print_schema_file
%attr(755,root,root) %{_bindir}/ndb_print_sys_file
%attr(755,root,root) %{_bindir}/ndb_restore
%attr(755,root,root) %{_bindir}/ndb_select_all
%attr(755,root,root) %{_bindir}/ndb_select_count
%attr(755,root,root) %{_bindir}/ndb_show_tables
%attr(755,root,root) %{_bindir}/ndb_size.pl
%attr(755,root,root) %{_bindir}/ndb_test_platform
%attr(755,root,root) %{_bindir}/ndb_waiter
%{_mandir}/man1/ndb_config.1*
%{_mandir}/man1/ndb_delete_all.1*
%{_mandir}/man1/ndb_desc.1*
%{_mandir}/man1/ndb_drop_index.1*
%{_mandir}/man1/ndb_drop_table.1*
%{_mandir}/man1/ndb_error_reporter.1*
%{_mandir}/man1/ndb_mgm.1*
%{_mandir}/man1/ndb_print_backup_file.1*
%{_mandir}/man1/ndb_print_schema_file.1*
%{_mandir}/man1/ndb_print_sys_file.1*
%{_mandir}/man1/ndb_restore.1*
%{_mandir}/man1/ndb_select_all.1*
%{_mandir}/man1/ndb_select_count.1*
%{_mandir}/man1/ndb_show_tables.1*
%{_mandir}/man1/ndb_size.pl.1*
%{_mandir}/man1/ndb_waiter.1*

%files ndb-mgm
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndb_mgmd
%attr(754,root,root) /etc/rc.d/init.d/%{name}-ndb-mgm
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}-ndb-mgm
%{_mandir}/man8/ndb_mgmd.8*

%files ndb-cpc
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ndb_cpcd
%attr(754,root,root) /etc/rc.d/init.d/mysql-ndb-cpc
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}-ndb-cpc
%{_mandir}/man1/ndb_cpcd.1*
%endif
