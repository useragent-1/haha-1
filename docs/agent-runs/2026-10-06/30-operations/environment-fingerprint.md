# ENV_FINGERPRINT

> 用途：每次开工先比对本文件与当前环境；不一致时执行 `bash /home/user/ha-ha/scripts/setup.sh`，再更新本文件。依赖目录可能不进入平台快照，因此“上轮安装成功”不能替代本轮 import 自检。

## 指纹元数据

| 项 | 值 |
|---|---|
| 生成时间 UTC | 2026-10-06T03:14:07.803382+00:00 |
| Host | e2b.local |
| Kernel | 6.1.158+ |
| Platform | Linux-6.1.158+-x86_64-with-glibc2.41 |
| Python | `Python 3.13.14` |
| pip | `pip 26.1.2 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)` |
| pip 包数量 | 182 |
| pip 列表 SHA-256 | `956309ecfe9a0bdac7d525d8edde6b638da4483a88362ee35f59a47589b59a29` |
| apt 包数量 | 650 |
| apt 列表 SHA-256 | `1de972d3b480a850c08eb79dc43cc8080a2a459974a6089610bca2fbefcfed0c` |

## 开工比对动作

```bash
python --version
python -m pip --version
python -m pip list --format=freeze | sort | sha256sum
dpkg-query -W -f='${binary:Package}=${Version}\n' | sort | sha256sum
python - <<'PY2'
for m in ['capstone','unicorn']:
    try:
        x=__import__(m); print(m, 'OK', getattr(x, '__version__', ''))
    except Exception as e:
        print(m, 'ERROR', repr(e))
PY2
```

若 Python 版本、包列表 hash、关键 import 或工具路径不一致：

```bash
bash /home/user/ha-ha/scripts/setup.sh
```

## pip 摘要

关键包：

```text
capstone==5.0.9
pip==26.1.2
setuptools==83.0.0
unicorn==2.1.4
```

完整列表：`case/environment-fingerprint/pip-freeze.txt`

## 已安装 apt 包

完整列表 SHA-256：`1de972d3b480a850c08eb79dc43cc8080a2a459974a6089610bca2fbefcfed0c`。为保证指纹可独立审计，以下记录全部已安装包：

<details>
<summary>apt package list (650 packages)</summary>

```text
adduser=3.152
apt-transport-https=3.0.3
apt=3.0.3
autoconf=2.72-3.1
automake=1:1.17-4
autotools-dev=20240727.1
base-files=13.8+deb13u6
base-passwd=[REDACTED:last4=.6.7]
bash=5.2.37-2+b9
binutils-common:amd64=2.44-3
binutils-x86-64-linux-gnu=2.44-3
binutils=2.44-3
bsdutils=1:2.41-5
build-essential=12.12
bzip2=1.0.8-6
ca-certificates=20250419
chrony=4.6.1-3+deb13u2
comerr-dev:amd64=2.1-1.47.2-3+b11
coreutils=9.7-3
cpp-14-x86-64-linux-gnu=14.2.0-19
cpp-14=14.2.0-19
cpp-x86-64-linux-gnu=4:14.2.0-1
cpp=4:14.2.0-1
curl=8.14.1-2+deb13u4
dash=0.5.12-12
dbus-bin=1.16.2-2
dbus-daemon=1.16.2-2
dbus-session-bus-common=1.16.2-2
dbus-system-bus-common=1.16.2-2
dbus=1.16.2-2
debconf=1.5.91
debian-archive-keyring=2025.1
debianutils=5.23.2
default-libmysqlclient-dev:amd64=1.1.1
diffutils=1:3.10-4
dirmngr=2.4.7-21+deb13u1+b4
dmsetup=2:1.02.205-2
dpkg-dev=1.22.22
dpkg=1.22.22
file=1:5.46-5
findutils=4.10.0-3
fontconfig-config=2.15.0-2.3
fontconfig=2.15.0-2.3
fonts-dejavu-core=2.37-8
fonts-dejavu-mono=2.37-8
fonts-noto-cjk=1:20240730+repack1-1
fuse3=3.17.2-3
g++-14-x86-64-linux-gnu=14.2.0-19
g++-14=14.2.0-19
g++-x86-64-linux-gnu=4:14.2.0-1
g++=4:14.2.0-1
gcc-14-base:amd64=14.2.0-19
gcc-14-x86-64-linux-gnu=14.2.0-19
gcc-14=14.2.0-19
gcc-x86-64-linux-gnu=4:14.2.0-1
gcc=4:14.2.0-1
gfortran-14-x86-64-linux-gnu=14.2.0-19
gfortran-14=14.2.0-19
gfortran-x86-64-linux-gnu=4:14.2.0-1
gfortran=4:14.2.0-1
gir1.2-freedesktop-dev:amd64=1.84.0-1
gir1.2-freedesktop:amd64=1.84.0-1
gir1.2-gdkpixbuf-2.0:amd64=2.42.12+dfsg-4+deb13u1
gir1.2-glib-2.0-dev:amd64=2.84.4-3~deb13u3
gir1.2-glib-2.0:amd64=2.84.4-3~deb13u3
gir1.2-harfbuzz-0.0:amd64=10.2.0-1+deb13u1
gir1.2-pango-1.0:amd64=1.56.3-1
gir1.2-rsvg-2.0:amd64=2.60.0+dfsg-1
girepository-tools:amd64=2.84.4-3~deb13u3
git-man=1:2.47.3-0+deb13u1
git=1:2.47.3-0+deb13u1
gnupg-l10n=2.4.7-21+deb13u1
gnupg=2.4.7-21+deb13u1
gpg-agent=2.4.7-21+deb13u1+b4
gpg=2.4.7-21+deb13u1+b4
gpgconf=2.4.7-21+deb13u1+b4
gpgsm=2.4.7-21+deb13u1+b4
grep=3.11-4
gzip=1.13-1
hicolor-icon-theme=0.18-2
hostname=3.25
icu-devtools=76.1-4
imagemagick-7-common=8:7.1.1.43+dfsg1-1+deb13u11
imagemagick-7.q16=8:7.1.1.43+dfsg1-1+deb13u11
imagemagick=8:7.1.1.43+dfsg1-1+deb13u11
init-system-helpers=1.69~deb13u1
iproute2=6.15.0-1
iptables=1.8.11-2
iputils-ping=3:20240905-3
jq=1.7.1-6+deb13u2
keyutils=1.6.3-6
krb5-multidev:amd64=1.21.3-5+deb13u1
less=668-1
libacl1:amd64=2.3.2-2+b1
libapparmor1:amd64=4.1.0-1
libapr1t64:amd64=1.7.5-1
libaprutil1t64:amd64=1.6.3-3+b1
libapt-pkg7.0:amd64=3.0.3
libasan8:amd64=14.2.0-19
libassuan9:amd64=3.0.2-2
libatomic1:amd64=14.2.0-19
libattr1:amd64=1:2.5.2-3
libaudit-common=1:4.0.2-2
libaudit1:amd64=1:4.0.2-2+b2
libauthen-sasl-perl=2.1700-1
libbinutils:amd64=2.44-3
libblas-dev:amd64=3.12.1-6
libblas3:amd64=3.12.1-6
libblkid-dev:amd64=2.41-5
libblkid1:amd64=2.41-5
libbluetooth-dev:amd64=5.82-1.1
libbluetooth3:amd64=5.82-1.1
libbpf1:amd64=1:1.5.0-3
libbrotli-dev:amd64=1.1.0-2+b7
libbrotli1:amd64=1.1.0-2+b7
libbsd0:amd64=0.12.2-2
libbz2-1.0:amd64=1.0.8-6
libbz2-dev:amd64=1.0.8-6
libc-bin=2.41-12+deb13u3
libc-dev-bin=2.41-12+deb13u3
libc6-dev:amd64=2.41-12+deb13u3
libc6:amd64=2.41-12+deb13u3
libcairo-gobject2:amd64=1.18.4-1+b1
libcairo-script-interpreter2:amd64=1.18.4-1+b1
libcairo2-dev:amd64=1.18.4-1+b1
libcairo2:amd64=1.18.4-1+b1
libcap-ng0:amd64=0.8.5-4+b1
libcap2-bin=1:2.75-10+deb13u1+b1
libcap2:amd64=1:2.75-10+deb13u1+b1
libcbor0.10:amd64=0.10.2-2
libcc1-0:amd64=14.2.0-19
libclone-perl:amd64=0.47-1+b1
libcom-err2:amd64=1.47.2-3+b11
libcrypt-dev:amd64=1:4.4.38-1
libcrypt1:amd64=1:4.4.38-1
libctf-nobfd0:amd64=2.44-3
libctf0:amd64=2.44-3
libcurl3t64-gnutls:amd64=8.14.1-2+deb13u4
libcurl4-openssl-dev:amd64=8.14.1-2+deb13u4
libcurl4t64:amd64=8.14.1-2+deb13u4
libdata-dump-perl=1.25-1
libdatrie-dev:amd64=0.2.13-3+b1
libdatrie1:amd64=0.2.13-3+b1
libdav1d-dev:amd64=1.5.1-1
libdav1d7:amd64=1.5.1-1
libdb-dev:amd64=5.3.4
libdb5.3-dev=5.3.28+dfsg2-9
libdb5.3t64:amd64=5.3.28+dfsg2-9
libdbus-1-3:amd64=1.16.2-2
libde265-0:amd64=1.0.15-1+b3
libdebconfclient0:amd64=0.280
libdeflate-dev:amd64=1.23-2
libdeflate0:amd64=1.23-2
libdevmapper1.02.1:amd64=2:1.02.205-2
libdjvulibre-dev:amd64=3.5.28-2.2
libdjvulibre-text=3.5.28-2.2
libdjvulibre21:amd64=3.5.28-2.2
libdpkg-perl=1.22.22
libdrm-amdgpu1:amd64=2.4.124-2
libdrm-common=2.4.124-2
libdrm-intel1:amd64=2.4.124-2
libdrm2:amd64=2.4.124-2
libedit2:amd64=3.1-20250104-1
libegl-mesa0:amd64=25.0.7-2+deb13u1
libegl1:amd64=1.7.0-1+b2
libelf1t64:amd64=0.192-4
libencode-locale-perl=1.05-3
liberror-perl=0.17030-1
libevent-2.1-7t64:amd64=2.1.12-stable-10+b1
libevent-core-2.1-7t64:amd64=2.1.12-stable-10+b1
libevent-dev=2.1.12-stable-10+b1
libevent-extra-2.1-7t64:amd64=2.1.12-stable-10+b1
libevent-openssl-2.1-7t64:amd64=2.1.12-stable-10+b1
libevent-pthreads-2.1-7t64:amd64=2.1.12-stable-10+b1
libexif-dev:amd64=0.6.25-1+deb13u1
libexif12:amd64=0.6.25-1+deb13u1
libexpat1-dev:amd64=2.7.1-2
libexpat1:amd64=2.7.1-2
libffi-dev:amd64=3.4.8-2
libffi8:amd64=3.4.8-2
libfftw3-bin=3.3.10-2+b1
libfftw3-dev:amd64=3.3.10-2+b1
libfftw3-double3:amd64=3.3.10-2+b1
libfftw3-long3:amd64=3.3.10-2+b1
libfftw3-quad3:amd64=3.3.10-2+b1
libfftw3-single3:amd64=3.3.10-2+b1
libfido2-1:amd64=1.15.0-1+b1
libfile-basedir-perl=0.09-2
libfile-desktopentry-perl=0.22-3
libfile-listing-perl=6.16-1
libfile-mimeinfo-perl=0.35-1
libfont-afm-perl=1.20-4
libfontconfig-dev:amd64=2.15.0-2.3
libfontconfig1:amd64=2.15.0-2.3
libfreetype-dev:amd64=2.13.3+dfsg-1+deb13u1
libfreetype6:amd64=2.13.3+dfsg-1+deb13u1
libfribidi-dev:amd64=1.0.16-1
libfribidi0:amd64=1.0.16-1
libfuse3-4:amd64=3.17.2-3
libgbm1:amd64=25.0.7-2+deb13u1
libgcc-14-dev:amd64=14.2.0-19
libgcc-s1:amd64=14.2.0-19
libgcrypt20:amd64=1.11.0-7+deb13u1
libgdbm-compat4t64:amd64=1.24-2
libgdbm-dev:amd64=1.24-2
libgdbm6t64:amd64=1.24-2
libgdk-pixbuf-2.0-0:amd64=2.42.12+dfsg-4+deb13u1
libgdk-pixbuf-2.0-dev:amd64=2.42.12+dfsg-4+deb13u1
libgdk-pixbuf2.0-bin=2.42.12+dfsg-4+deb13u1
libgdk-pixbuf2.0-common=2.42.12+dfsg-4+deb13u1
libgfortran-14-dev:amd64=14.2.0-19
libgfortran5:amd64=14.2.0-19
libgio-2.0-dev-bin=2.84.4-3~deb13u3
libgio-2.0-dev:amd64=2.84.4-3~deb13u3
libgirepository-2.0-0:amd64=2.84.4-3~deb13u3
libgl1-mesa-dri:amd64=25.0.7-2+deb13u1
libgl1:amd64=1.7.0-1+b2
libgles2:amd64=1.7.0-1+b2
libglib2.0-0t64:amd64=2.84.4-3~deb13u3
libglib2.0-bin=2.84.4-3~deb13u3
libglib2.0-data=2.84.4-3~deb13u3
libglib2.0-dev-bin=2.84.4-3~deb13u3
libglib2.0-dev:amd64=2.84.4-3~deb13u3
libglvnd0:amd64=1.7.0-1+b2
libglx-mesa0:amd64=25.0.7-2+deb13u1
libglx0:amd64=1.7.0-1+b2
libgmp-dev:amd64=2:6.3.0+dfsg-3
libgmp10:amd64=2:6.3.0+dfsg-3
libgmpxx4ldbl:amd64=2:6.3.0+dfsg-3
libgnutls-dane0t64:amd64=3.8.9-3+deb13u4
libgnutls-openssl27t64:amd64=3.8.9-3+deb13u4
libgnutls28-dev:amd64=3.8.9-3+deb13u4
libgnutls30t64:amd64=3.8.9-3+deb13u4
libgomp1:amd64=14.2.0-19
libgpg-error0:amd64=1.51-4
libgprofng0:amd64=2.44-3
libgraphite2-3:amd64=1.3.14-2+deb13u1
libgraphite2-dev:amd64=1.3.14-2+deb13u1
libgssapi-krb5-2:amd64=1.21.3-5+deb13u1
libgssrpc4t64:amd64=1.21.3-5+deb13u1
libharfbuzz-cairo0:amd64=10.2.0-1+deb13u1
libharfbuzz-dev:amd64=10.2.0-1+deb13u1
libharfbuzz-gobject0:amd64=10.2.0-1+deb13u1
libharfbuzz-icu0:amd64=10.2.0-1+deb13u1
libharfbuzz-subset0:amd64=10.2.0-1+deb13u1
libharfbuzz0b:amd64=10.2.0-1+deb13u1
libheif-plugin-dav1d:amd64=1.19.8-1
libheif-plugin-libde265:amd64=1.19.8-1
libheif1:amd64=1.19.8-1
libhogweed6t64:amd64=3.10.1-1
libhtml-form-perl=6.12-1
libhtml-format-perl=2.16-2
libhtml-parser-perl:amd64=3.83-2~deb13u1
libhtml-tagset-perl=3.24-1
libhtml-tree-perl=5.07-3
libhttp-cookies-perl=[REDACTED:last4=11-1]
libhttp-daemon-perl=6.16-1+deb13u1
libhttp-date-perl=6.06-1
libhttp-message-perl=7.00-2
libhttp-negotiate-perl=6.01-2
libhwasan0:amd64=14.2.0-19
libice-dev:amd64=2:1.1.1-1
libice6:amd64=2:1.1.1-1
libicu-dev:amd64=76.1-4
libicu76:amd64=76.1-4
libidn2-0:amd64=2.3.8-2
libidn2-dev:amd64=2.3.8-2
libimath-3-1-29t64:amd64=3.1.12-1+b3
libimath-dev:amd64=3.1.12-1+b3
libio-compress-brotli-perl=0.004001-2+b3
libio-html-perl=1.004-3
libio-socket-ssl-perl=2.089-1
libio-stringy-perl=2.113-2
libip4tc2:amd64=1.8.11-2
libip6tc2:amd64=1.8.11-2
libipc-system-simple-perl=1.30-2
libisl23:amd64=0.27-1
libitm1:amd64=14.2.0-19
libjansson4:amd64=2.14-2+b3
libjbig-dev:amd64=2.1-6.1+b2
libjbig0:amd64=2.1-6.1+b2
libjpeg-dev:amd64=1:2.1.5-4
libjpeg62-turbo-dev:amd64=1:2.1.5-4
libjpeg62-turbo:amd64=1:2.1.5-4
libjq1:amd64=1.7.1-6+deb13u2
libk5crypto3:amd64=1.21.3-5+deb13u1
libkadm5clnt-mit12:amd64=1.21.3-5+deb13u1
libkadm5srv-mit12:amd64=1.21.3-5+deb13u1
libkdb5-10t64:amd64=1.21.3-5+deb13u1
libkeyutils1:amd64=1.6.3-6
libkrb5-3:amd64=1.21.3-5+deb13u1
libkrb5-dev:amd64=1.21.3-5+deb13u1
libkrb5support0:amd64=1.21.3-5+deb13u1
libksba8:amd64=1.6.7-2+b1
liblapack-dev:amd64=3.12.1-6
liblapack3:amd64=3.12.1-6
liblastlog2-2:amd64=2.41-5
liblcms2-2:amd64=2.16-2+deb13u2
liblcms2-dev:amd64=2.16-2+deb13u2
libldap-dev:amd64=2.6.10+dfsg-1
libldap2:amd64=2.6.10+dfsg-1
liblerc-dev:amd64=4.0.0+ds-5
liblerc4:amd64=4.0.0+ds-5
libllvm19:amd64=1:19.1.7-3+b1
liblqr-1-0-dev:amd64=0.4.2-2.1+b2
liblqr-1-0:amd64=0.4.2-2.1+b2
liblsan0:amd64=14.2.0-19
libltdl-dev:amd64=2.5.4-4
libltdl7:amd64=2.5.4-4
liblwp-mediatypes-perl=6.04-2
liblwp-protocol-https-perl=6.14-1
liblz4-1:amd64=1.10.0-4
liblzma-dev:amd64=5.8.1-1+deb13u1
liblzma5:amd64=5.8.1-1+deb13u1
liblzo2-2:amd64=2.10-3+b1
libmagic-mgc=1:5.46-5
libmagic1t64:amd64=1:5.46-5
libmagickcore-7-arch-config:amd64=8:7.1.1.43+dfsg1-1+deb13u11
libmagickcore-7-headers=8:7.1.1.43+dfsg1-1+deb13u11
libmagickcore-7.q16-10-extra:amd64=8:7.1.1.43+dfsg1-1+deb13u11
libmagickcore-7.q16-10:amd64=8:7.1.1.43+dfsg1-1+deb13u11
libmagickcore-7.q16-dev:amd64=8:7.1.1.43+dfsg1-1+deb13u11
libmagickcore-dev=8:7.1.1.43+dfsg1-1+deb13u11
libmagickwand-7-headers=8:7.1.1.43+dfsg1-1+deb13u11
libmagickwand-7.q16-10:amd64=8:7.1.1.43+dfsg1-1+deb13u11
libmagickwand-7.q16-dev:amd64=8:7.1.1.43+dfsg1-1+deb13u11
libmagickwand-dev=8:7.1.1.43+dfsg1-1+deb13u11
libmailtools-perl=2.22-1
libmariadb-dev-compat=1:11.8.6-0+deb13u1
libmariadb-dev=1:11.8.6-0+deb13u1
libmariadb3:amd64=1:11.8.6-0+deb13u1
libmaxminddb-dev:amd64=1.12.2-1
libmaxminddb0:amd64=1.12.2-1
libmd0:amd64=1.1.0-2+b1
libmnl0:amd64=1.0.5-3
libmount-dev:amd64=2.41-5
libmount1:amd64=2.41-5
libmpc3:amd64=1.3.1-1+b3
libmpfr6:amd64=4.2.2-1
libncurses-dev:amd64=6.5+20250216-2
libncurses6:amd64=6.5+20250216-2
libncursesw6:amd64=6.5+20250216-2
libnet-dbus-perl=1.2.0-2+b3
libnet-http-perl=6.23-1
libnet-smtp-ssl-perl=1.04-2
libnet-ssleay-perl:amd64=1.94-3
libnetfilter-conntrack3:amd64=1.1.0-1
libnettle8t64:amd64=3.10.1-1
libnfnetlink0:amd64=1.0.2-3
libnfsidmap1:amd64=1:2.8.3-1
libnftables1:amd64=1.1.3-1
libnftnl11:amd64=1.2.9-1
libnghttp2-14:amd64=1.64.0-1.1+deb13u1
libnghttp2-dev:amd64=1.64.0-1.1+deb13u1
libnghttp3-9:amd64=1.8.0-1
libnghttp3-dev:amd64=1.8.0-1
libngtcp2-16:amd64=1.11.0-1+deb13u1
libngtcp2-crypto-gnutls8:amd64=1.11.0-1+deb13u1
libnpth0t64:amd64=1.8-3
libonig5:amd64=6.9.9-1+b1
libopenexr-3-1-30:amd64=3.1.13-2
libopenexr-dev=3.1.13-2
libopenjp2-7-dev:amd64=2.5.3-2.1~deb13u2
libopenjp2-7:amd64=2.5.3-2.1~deb13u2
libp11-kit-dev:amd64=0.25.5-3
libp11-kit0:amd64=0.25.5-3
libpam-modules-bin=1.7.0-5
libpam-modules:amd64=1.7.0-5
libpam-runtime=1.7.0-5
libpam0g:amd64=1.7.0-5
libpango-1.0-0:amd64=1.56.3-1
libpango1.0-dev:amd64=1.56.3-1
libpangocairo-1.0-0:amd64=1.56.3-1
libpangoft2-1.0-0:amd64=1.56.3-1
libpangoxft-1.0-0:amd64=1.56.3-1
libpaper-utils=2.2.5-0.3+b2
libpaper2:amd64=2.2.5-0.3+b2
libpciaccess0:amd64=0.17-3+b3
libpcre2-16-0:amd64=10.46-1~deb13u1
libpcre2-32-0:amd64=10.46-1~deb13u1
libpcre2-8-0:amd64=10.46-1~deb13u1
libpcre2-dev:amd64=10.46-1~deb13u1
libpcre2-posix3:amd64=10.46-1~deb13u1
libperl5.40:amd64=5.40.1-6
libpixman-1-0:amd64=0.44.0-3
libpixman-1-dev:amd64=0.44.0-3
libpkgconf3:amd64=1.8.1-4
libpng-dev:amd64=1.6.48-1+deb13u5
libpng16-16t64:amd64=1.6.48-1+deb13u5
libpq-dev=17.10-0+deb13u1
libpq5:amd64=17.10-0+deb13u1
libproc2-0:amd64=2:4.0.4-9
libpsl-dev:amd64=0.21.2-1.1+b1
libpsl5t64:amd64=0.21.2-1.1+b1
libpython3-stdlib:amd64=3.13.5-1
libpython3.13-minimal:amd64=3.13.5-2+deb13u3
libpython3.13-stdlib:amd64=3.13.5-2+deb13u3
libquadmath0:amd64=14.2.0-19
libraw23t64:amd64=0.21.4-2
libreadline-dev:amd64=8.2-6
libreadline8t64:amd64=8.2-6
librsvg2-2:amd64=2.60.0+dfsg-1
librsvg2-common:amd64=2.60.0+dfsg-1
librsvg2-dev:amd64=2.60.0+dfsg-1
librtmp-dev:amd64=2.4+20151223.gitfa8646d.1-2+b5
librtmp1:amd64=2.4+20151223.gitfa8646d.1-2+b5
libsasl2-2:amd64=2.1.28+dfsg1-9
libsasl2-modules-db:amd64=2.1.28+dfsg1-9
libseccomp2:amd64=2.6.0-2
libselinux1-dev:amd64=3.8.1-1
libselinux1:amd64=3.8.1-1
libsemanage-common=3.8.1-1
libsemanage2:amd64=3.8.1-1
libsensors-config=1:3.6.2-2
libsensors5:amd64=1:3.6.2-2
libsepol-dev:amd64=3.8.1-1
libsepol2:amd64=3.8.1-1
libserf-1-1:amd64=1.3.10-3+b1
libsframe1:amd64=2.44-3
libsharpyuv-dev:amd64=1.5.0-0.1
libsharpyuv0:amd64=1.5.0-0.1
libsm-dev:amd64=2:1.2.6-1
libsm6:amd64=2:1.2.6-1
libsmartcols1:amd64=2.41-5
libsqlite3-0:amd64=3.46.1-7+deb13u1
libsqlite3-dev:amd64=3.46.1-7+deb13u1
libssh2-1-dev:amd64=1.11.1-1+deb13u1
libssh2-1t64:amd64=1.11.1-1+deb13u1
libssl-dev:amd64=3.5.6-1~deb13u2
libssl3t64:amd64=3.5.6-1~deb13u2
libstdc++-14-dev:amd64=14.2.0-19
libstdc++6:amd64=14.2.0-19
libsvn1:amd64=1.14.5-3
libsysprof-capture-4-dev:amd64=48.0-2
libsystemd-shared:amd64=257.13-1~deb13u1
libsystemd0:amd64=257.13-1~deb13u1
libtasn1-6-dev:amd64=4.20.0-2+deb13u1
libtasn1-6:amd64=4.20.0-2+deb13u1
libtcl8.6:amd64=8.6.16+dfsg-1
libtext-charwidth-perl:amd64=0.04-11+b4
libtext-iconv-perl:amd64=1.7-8+b4
libtext-wrapi18n-perl=0.06-10
libthai-data=0.1.29-2
libthai-dev:amd64=0.1.29-2+b1
libthai0:amd64=0.1.29-2+b1
libtie-ixhash-perl=1.23-4
libtiff-dev:amd64=4.7.0-3+deb13u2
libtiff6:amd64=4.7.0-3+deb13u2
libtiffxx6:amd64=4.7.0-3+deb13u2
libtimedate-perl=2.3300-2
libtinfo6:amd64=6.5+20250216-2
libtirpc-common=1.3.6+ds-1
libtirpc-dev:amd64=1.3.6+ds-1
libtirpc3t64:amd64=1.3.6+ds-1
libtk8.6:amd64=8.6.16-1
libtool=2.5.4-4
libtry-tiny-perl=0.32-1
libtsan2:amd64=14.2.0-19
libubsan1:amd64=14.2.0-19
libudev1:amd64=257.13-1~deb13u1
libunbound8:amd64=1.22.0-2+deb13u3
libunistring5:amd64=1.3-2
liburi-perl=5.30-1
libutf8proc3:amd64=2.9.0-1+b2
libuuid1:amd64=2.41-5
libvulkan1:amd64=1.4.309.0-1
libwayland-client0:amd64=1.23.1-3
libwayland-server0:amd64=1.23.1-3
libwebp-dev:amd64=1.5.0-0.1
libwebp7:amd64=1.5.0-0.1
libwebpdecoder3:amd64=1.5.0-0.1
libwebpdemux2:amd64=1.5.0-0.1
libwebpmux3:amd64=1.5.0-0.1
libwmf-0.2-7:amd64=0.2.13-1.1+b3
libwmf-dev=0.2.13-1.1+b3
libwmflite-0.2-7:amd64=0.2.13-1.1+b3
libwrap0:amd64=7.6.q-36
libwtmpdb0:amd64=0.73.0-3+deb13u1
libwww-perl=6.78-1
libwww-robotrules-perl=6.02-1
libx11-6:amd64=2:1.8.12-1
libx11-data=2:1.8.12-1
libx11-dev:amd64=2:1.8.12-1
libx11-protocol-perl=0.56-9
libx11-xcb1:amd64=2:1.8.12-1
libxau-dev:amd64=1:1.0.11-1
libxau6:amd64=1:1.0.11-1
libxaw7:amd64=2:1.0.16-1
libxcb-dri3-0:amd64=1.17.0-2+b1
libxcb-glx0:amd64=1.17.0-2+b1
libxcb-present0:amd64=1.17.0-2+b1
libxcb-randr0:amd64=1.17.0-2+b1
libxcb-render0-dev:amd64=1.17.0-2+b1
libxcb-render0:amd64=1.17.0-2+b1
libxcb-shape0:amd64=1.17.0-2+b1
libxcb-shm0-dev:amd64=1.17.0-2+b1
libxcb-shm0:amd64=1.17.0-2+b1
libxcb-sync1:amd64=1.17.0-2+b1
libxcb-xfixes0:amd64=1.17.0-2+b1
libxcb1-dev:amd64=1.17.0-2+b1
libxcb1:amd64=1.17.0-2+b1
libxcomposite1:amd64=1:0.4.6-1
libxcursor1:amd64=1:1.2.3-1
libxdmcp-dev:amd64=1:1.1.5-1
libxdmcp6:amd64=1:1.1.5-1
libxext-dev:amd64=2:1.3.4-1+b3
libxext6:amd64=2:1.3.4-1+b3
libxfixes3:amd64=1:6.0.0-2+b4
libxft-dev:amd64=2.3.6-1+b4
libxft2:amd64=2.3.6-1+b4
libxi6:amd64=2:1.8.2-1
libxinerama1:amd64=2:1.1.4-3+b4
libxkbfile1:amd64=1:1.1.0-1+b4
libxml-parser-perl=2.47-2~deb13u1
libxml-twig-perl=1:3.52-3
libxml-xpathengine-perl=0.14-2
libxml2-dev:amd64=2.12.7+dfsg+really2.9.14-2.1+deb13u3
libxml2:amd64=2.12.7+dfsg+really2.9.14-2.1+deb13u3
libxmu6:amd64=2:1.1.3-3+b4
libxmuu1:amd64=2:1.1.3-3+b4
libxpm4:amd64=1:3.5.17-1+deb13u1
libxrandr2:amd64=2:1.5.4-1+b3
libxrender-dev:amd64=1:0.9.12-1
libxrender1:amd64=1:0.9.12-1
libxshmfence1:amd64=1.3.3-1
libxslt1-dev:amd64=1.1.35-1.2+deb13u3
libxslt1.1:amd64=1.1.35-1.2+deb13u3
libxss-dev:amd64=1:1.2.3-1+b3
libxss1:amd64=1:1.2.3-1+b3
libxt-dev:amd64=1:1.2.1-1.2+b2
libxt6t64:amd64=1:1.2.1-1.2+b2
libxtables12:amd64=1.8.11-2
libxtst6:amd64=2:1.2.5-1
libxv1:amd64=2:1.0.11-1.1+b3
libxxf86dga1:amd64=2:1.1.5-1+b3
libxxf86vm1:amd64=1:1.1.4-1+b4
libxxhash0:amd64=0.8.3-2
libyaml-0-2:amd64=0.2.5-2
libyaml-dev:amd64=0.2.5-2
libz3-4:amd64=4.13.3-1
libzstd-dev:amd64=1.5.7+dfsg-1
libzstd1:amd64=1.5.7+dfsg-1
linux-libc-dev=6.12.95-1
login.defs=1:4.17.4-2
login=1:4.16.0-2+really2.41-5
luit=2.0.20240910-1
m4=1.4.19-8
make=4.4.1-2
mariadb-common=1:11.8.6-0+deb13u1
mawk=1.3.4.20250131-1
media-types=13.0.0
mercurial-common=7.0.1-2
mercurial=7.0.1-2
mesa-libgallium:amd64=25.0.7-2+deb13u1
mesa-vulkan-drivers:amd64=25.0.7-2+deb13u1
mount=2.41-5
mysql-common=5.8+1.1.1
native-architecture=0.2.6
ncurses-base=6.5+20250216-2
ncurses-bin=6.5+20250216-2
netbase=6.5
nettle-dev:amd64=3.10.1-1
nfs-common=1:2.8.3-1
nftables=1.1.3-1
nodejs=20.20.2-1nodesource1
openssh-client=1:10.0p1-7+deb13u4
openssh-server=1:10.0p1-7+deb13u4
openssh-sftp-server=1:10.0p1-7+deb13u4
openssl-provider-legacy=3.5.6-1~deb13u2
openssl=3.5.6-1~deb13u2
pango1.0-tools=1.56.3-1
passwd=1:4.17.4-2
patch=2.8-2
perl-base=5.40.1-6
perl-modules-5.40=5.40.1-6
perl-openssl-defaults:amd64=7+b2
perl=5.40.1-6
pinentry-curses=1.3.1-2
pkgconf-bin=1.8.1-4
pkgconf:amd64=1.8.1-4
procps=2:4.0.4-9
python3-minimal=3.13.5-1
python3-packaging=25.0-1
python3.13-minimal=3.13.5-2+deb13u3
python3.13=3.13.5-2+deb13u3
python3=3.13.5-1
r-base-core=4.5.0-3
r-base-dev=4.5.0-3
r-base-html=4.5.0-3
r-base=4.5.0-3
r-cran-boot=1.3-31-1
r-cran-class=7.3-23-1
r-cran-cluster=2.1.8.1-1
r-cran-codetools=0.2-20-1
r-cran-foreign=0.8.90-1
r-cran-kernsmooth=2.23-26-1
r-cran-lattice=0.22-7-1
r-cran-mass=7.3-65-1
r-cran-matrix=1.7-3-1
r-cran-mgcv=1.9-3-1
r-cran-nlme=3.1.168-1
r-cran-nnet=7.3-20-1
r-cran-rpart=4.1.24-1
r-cran-spatial=7.3-18-1
r-cran-survival=3.8-3-1
r-doc-html=4.5.0-3
r-recommended=4.5.0-3
readline-common=8.2-6
rpcbind=1.2.7-1
rpcsvc-proto=1.4.3-1
runit-helper=2.16.4
sed=4.9-2+deb13u1
sensible-utils=0.0.25
shared-mime-info=2.4-5+b2
socat=1.8.0.3-1
sq=1.3.1-2+b2
sqv=1.3.0-3+b2
subversion=1.14.5-3
sudo=1.9.16p2-3+deb13u2
systemd-sysv=257.13-1~deb13u1
systemd=257.13-1~deb13u1
sysvinit-utils=3.14-4
tar=1.35+dfsg-3.1
tcl-dev:amd64=8.6.16
tcl8.6-dev:amd64=8.6.16+dfsg-1
tcl8.6=8.6.16+dfsg-1
tcl=8.6.16
tk-dev:amd64=8.6.16
tk8.6-dev:amd64=8.6.16-1
tk8.6=8.6.16-1
tk=8.6.16
tzdata=2026b-0+deb13u1
ucf=3.0052
unzip=6.0-29
util-linux=2.41-5
uuid-dev:amd64=2.41-5
wget=1.25.0-2
x11-common=1:7.7+24+deb13u1
x11-utils=7.7+7
x11-xserver-utils=7.7+11
x11proto-dev=2024.1-1
xauth=1:1.1.2-1.1
xdg-utils=1.2.1-2
xorg-sgml-doctools=1:1.11-1.1
xtrans-dev=1.4.0-1
xz-utils=5.8.1-1+deb13u1
zip=3.0-15
zlib1g-dev:amd64=1:1.3.dfsg+really1.3.1-1+b1
zlib1g:amd64=1:1.3.dfsg+really1.3.1-1+b1
zutty=0.16.2.20241020+dfsg1-1
```
</details>

## 工具路径

```text
python	/usr/local/bin/python
pip	/usr/local/bin/pip
git	/usr/bin/git
file	/usr/bin/file
readelf	/usr/bin/readelf
objdump	/usr/bin/objdump
strings	/usr/bin/strings
nm	/usr/bin/nm
curl	/usr/bin/curl
jq	/usr/bin/jq
rg	NOT_INSTALLED
xxd	NOT_INSTALLED
7z	NOT_INSTALLED
strace	NOT_INSTALLED
binwalk	NOT_INSTALLED
rustfilt	NOT_INSTALLED
ghidra	NOT_INSTALLED
r2	NOT_INSTALLED
yara	NOT_INSTALLED
```

## setup.sh 三项自检

```text
triage_artifact: OK
find_crypto: OK
auto_analyze: OK
```

完整 setup 输出：`case/environment-fingerprint/setup_raw.txt`

注意：setup 输出出现 Git 无 upstream 警告，但脚本最终 `setup_exit=0`，三项自检和 capstone/unicorn import 均成功。
