%global debug_package %{nil}

Name: restic
Epoch: 100
Version: 0.12.1
Release: 1%{?dist}
Summary: Backup program with deduplication and encryption
License: BSD-2-Clause
URL: https://github.com/restic/restic/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.19
BuildRequires: glibc-static

%description
Restic is a backup program. It supports verification, encryption,
snapshots and deduplication.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
    export CGO_ENABLED=1 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w" \
        -o ./bin/restic ./cmd/restic

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_prefix}/share/bash-completion/completions
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/restic
./bin/restic generate --bash-completion %{buildroot}%{_prefix}/share/bash-completion/completions/restic

%files
%license LICENSE
%{_bindir}/*
%{_prefix}/share/bash-completion/completions/*

%changelog
