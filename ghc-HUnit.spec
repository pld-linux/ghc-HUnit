#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	HUnit
Summary:	A unit testing framework for Haskell
Summary(pl.UTF-8):	Szkielet testów jednostkowych dla Haskella
Name:		ghc-%{pkgname}
Version:	1.2.5.2
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/HUnit
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	1ba79aaeb57361a8593e864694539025
URL:		http://hunit.sourceforge.net/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-deepseq
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-deepseq-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 3
Requires:	ghc-base < 5
Requires:	ghc-deepseq
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
HUnit is a unit testing framework for Haskell, inspired by the JUnit
tool for Java, see: <http://www.junit.org/>.

%description -l pl.UTF-8
HUnit to szkielet testów jednostkowych dla Haskella, zainspirowany
narzędziem JUnit dla Javy, p. <http://www.junit.org/>.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 3
Requires:	ghc-base-prof < 5
Requires:	ghc-deepseq-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE README
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSHUnit-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSHUnit-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Test
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Test/HUnit.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Test/HUnit
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Test/HUnit/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSHUnit-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Test/HUnit.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Test/HUnit/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
