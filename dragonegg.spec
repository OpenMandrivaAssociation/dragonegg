%define _disable_ld_no_undefined 1

%define		gcc_version		%(%__cc -dumpversion)
%define		gcc_plugindir		%(%__cc -print-file-name=plugin)

Summary:	DragonEgg - Using LLVM as a GCC backend
Name:		dragonegg
Version:	3.3
Release:	2
License:	NCSA
Group:		Development/Other
Url:		https://dragonegg.llvm.org
Source0:	http://llvm.org/releases/%version/dragonegg-%version.src.tar.gz
Patch0:		dragonegg-3.3-arm-target.patch
BuildRequires:	gcc-plugin-devel
BuildRequires:	llvm-devel

%description
DragonEgg is a gcc plugin that replaces GCC's optimizers and code
generators with those from the LLVM project. It works with gcc-4.5,
gcc-4.6, and gcc-4.7, targets the x86-32 and x86-64 processor families,
and has been successfully used on the Darwin, FreeBSD, KFreeBSD, Linux
and OpenBSD platforms. It fully supports Ada, C, C++ and Fortran.
It has partial support for Go, Java, Obj-C and Obj-C++.

%files
%doc %{_docdir}/%{name}
%{_bindir}/%{name}
%{gcc_plugindir}/%{name}.so

#----------------------------------------------------------------------------
%prep
%setup -q -n %{name}-%{version}.src
%patch0 -p1 -b .arm~

%build
%setup_compile_flags
%make	\
	GCC=%__cc \
	LLVM_CONFIG=llvm-config \
	GCC_VERSION=%{gcc_version} \
	REVISION=`llvm-config --version` \
	VERBOSE=1

#-----------------------------------------------------------------------
%install
install -m755 -D %{name}.so %{buildroot}%{gcc_plugindir}/%{name}.so
install -d %{buildroot}%{_docdir}/%{name}
install -m644 README TODO %{buildroot}%{_docdir}/%{name}

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh

gcc-%{gcc_version} -fplugin=%{gcc_plugindir}/%{name}.so "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

