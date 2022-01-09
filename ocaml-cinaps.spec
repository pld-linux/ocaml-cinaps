#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	cinaps
Summary:	Trivial Metaprogramming tool using the OCaml toplevel
Summary(pl.UTF-8):	Trywialne narzędzie do metaprogramowania wykorzystujące toplevel w OCamlu
Name:		ocaml-cinaps
Version:	0.15.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/ocaml-ppx/cinaps/releases
Source0:	https://github.com/ocaml-ppx/cinaps/archive/v%{version}/cinaps-%{version}.tar.gz
# Source0-md5:	fe76665415e691e0c3c0d761ff95edfb
URL:		https://github.com/ocaml-ppx/cinaps
BuildRequires:	help2man
BuildRequires:	ocaml >= 1:4.04
BuildRequires:	ocaml-dune-devel >= 2.0.0
BuildRequires:	ocaml-re-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{without ocaml_opt}
%define		no_install_post_strip	1
# no opt means no native binary, stripping bytecode breaks such programs
%define		_enable_debug_packages	0
%endif

%description
This package contains files needed to run bytecode executables using
cinaps library.

%description -l pl.UTF-8
Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających biblioteki cinaps.

%package devel
Summary:	Trivial Metaprogramming tool using the OCaml toplevel - development part
Summary(pl.UTF-8):	Trywialne narzędzie do metaprogramowania wykorzystujące toplevel w OCamlu - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ocaml-re-devel
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
cinaps library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
biblioteki cinaps.

%prep
%setup -q -n cinaps-%{version}

%build
dune build --verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/man1
help2man -N --version-string=%{version} $RPM_BUILD_ROOT%{_bindir}/cinaps >$RPM_BUILD_ROOT%{_mandir}/man1/cinaps.1

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/cinaps/runtime/*.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/cinaps

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.md README.org
%attr(755,root,root) %{_bindir}/cinaps
%dir %{_libdir}/ocaml/cinaps
%{_libdir}/ocaml/cinaps/META
%dir %{_libdir}/ocaml/cinaps/runtime
%{_libdir}/ocaml/cinaps/runtime/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/cinaps/runtime/*.cmxs
%endif
%{_mandir}/man1/cinaps.1*

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/cinaps/runtime/*.cmi
%{_libdir}/ocaml/cinaps/runtime/*.cmt
%{_libdir}/ocaml/cinaps/runtime/*.cmti
%{_libdir}/ocaml/cinaps/runtime/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/cinaps/runtime/*.a
%{_libdir}/ocaml/cinaps/runtime/*.cmx
%{_libdir}/ocaml/cinaps/runtime/*.cmxa
%endif
%{_libdir}/ocaml/cinaps/dune-package
%{_libdir}/ocaml/cinaps/opam
