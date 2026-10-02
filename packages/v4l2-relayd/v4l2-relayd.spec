Name:           v4l2-relayd
Version:        0.2.0
Release:        1%{?dist}
Summary:        Play GStreamer sources into v4l2loopback devices
License:        GPL-2.0-or-later
URL:            https://gitlab.com/vicamo/v4l2-relayd
Source0:        https://gitlab.com/vicamo/v4l2-relayd/-/archive/upstream/%{version}/v4l2-relayd-upstream-%{version}.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64 aarch64
BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(systemd)
Requires:       glib2
Requires:       gstreamer1
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
# The daemon feeds loopback devices; the module itself is not in Fedora
# proper (RPM Fusion ships akmod-v4l2loopback), so this stays a weak
# dependency.
Recommends:     v4l2loopback

%description
v4l2-relayd plays GStreamer sources into v4l2loopback devices, with
systemd units and a generator for per-device instances.

%prep
%autosetup -n %{name}-upstream-%{version}
# The two fixes below are carried verbatim from the upstream Arch package
# (omarchy-pkgs). They are inlined because this recipe's source flow only
# fetches URL sources (see .copr/Makefile): there is no local patch file
# to reference.
patch -p0 <<'RELAYD_RESET_EOF'
--- src/v4l2-relayd.c.orig	2026-03-30 09:59:14.804751921 -0700
+++ src/v4l2-relayd.c	2026-03-30 09:59:14.827617699 -0700
@@ -58,6 +58,7 @@
 static GstElement *input_pipeline = NULL;
 static GstElement *output_pipeline = NULL;
 static GstElement *splash_pipeline = NULL;
+static GTimer *input_timer = NULL;

 static gboolean    backend_pipeline_bus_call (GstBus      *bus,
                                               GstMessage  *msg,
@@ -278,6 +279,10 @@
 {
   gst_element_set_state (splash_pipeline_get (), GST_STATE_NULL);
   gst_element_set_state (input_pipeline_get (), GST_STATE_PLAYING);
+  if (input_timer == NULL)
+    input_timer = g_timer_new ();
+  else
+    g_timer_start (input_timer);
 }

 static void
@@ -285,6 +290,15 @@
 {
   if (input_pipeline != NULL)
     gst_element_set_state (input_pipeline, GST_STATE_NULL);
+  /* After a real streaming session (>3s), reset the output pipeline
+   * to clear stale v4l2loopback state that causes format negotiation
+   * failures when switching between camera apps.  Brief probes from
+   * PipeWire/WirePlumber (<1s) are skipped. */
+  if (input_timer != NULL && g_timer_elapsed (input_timer, NULL) > 3.0
+      && output_pipeline != NULL) {
+    gst_element_set_state (output_pipeline, GST_STATE_READY);
+    gst_element_set_state (output_pipeline, GST_STATE_PLAYING);
+  }
   if (input_pipeline != NULL)
     gst_element_set_state (splash_pipeline, GST_STATE_PLAYING);
 }
RELAYD_RESET_EOF
patch -p0 <<'RELAYD_SPLASH_EOF'
--- data/systemd/v4l2-relayd@.service.orig	2026-06-15 12:00:00.000000000 -0500
+++ data/systemd/v4l2-relayd@.service	2026-06-15 12:00:00.000000000 -0500
@@ -14,7 +14,7 @@
 ExecCondition=/usr/bin/test -n "$HEIGHT"
 ExecCondition=/usr/bin/test -n "$FRAMERATE"
 ExecCondition=/usr/bin/test -n "${CARD_LABEL}"
-ExecStart=/bin/sh -c 'DEVICE=$(grep -l -m1 -E "^${CARD_LABEL}$" /sys/devices/virtual/video4linux/*/name | cut -d/ -f6); exec /usr/bin/v4l2-relayd -i "${VIDEOSRC}" $${SPLASHSRC:+-s "${SPLASHSRC}"} -o "appsrc name=appsrc caps=video/x-raw,format=${FORMAT},width=${WIDTH},height=${HEIGHT},framerate=${FRAMERATE} ! videoconvert ! v4l2sink name=v4l2sink device=/dev/$${DEVICE}" $EXTRA_OPTS'
+ExecStart=/bin/sh -c 'DEVICE=$(grep -l -m1 -E "^${CARD_LABEL}$" /sys/devices/virtual/video4linux/*/name | cut -d/ -f6); exec /usr/bin/v4l2-relayd -i "${VIDEOSRC}" $${SPLASHSRC:+-s "$${SPLASHSRC}"} -o "appsrc name=appsrc caps=video/x-raw,format=${FORMAT},width=${WIDTH},height=${HEIGHT},framerate=${FRAMERATE} ! videoconvert ! v4l2sink name=v4l2sink device=/dev/$${DEVICE}" $EXTRA_OPTS'
 Restart=always
 PrivateNetwork=yes
 PrivateTmp=yes
RELAYD_SPLASH_EOF

%build
NOCONFIGURE=1 ./autogen.sh
%configure --disable-maintainer-mode
%make_build

%check
make check

%install
%make_install
# The module supports configuring multiple loopback devices; since we do
# not know whether the user might be using some for other purposes, we
# should not override its options unilaterally (mirrors upstream).
rm %{buildroot}%{_sysconfdir}/modprobe.d/v4l2-relayd.conf
rmdir %{buildroot}%{_sysconfdir}/modprobe.d || :

%files
%license LICENSE
%doc README.md
%{_bindir}/v4l2-relayd
%config(noreplace) %{_sysconfdir}/default/v4l2-relayd
%{_sysconfdir}/modules-load.d/v4l2-relayd.conf
%{_sysconfdir}/v4l2-relayd.d/
%{_unitdir}/v4l2-relayd.service
%{_unitdir}/v4l2-relayd@.service
%{_libexecdir}/systemd/system-generators/v4l2-relayd-generator

%changelog
* Wed Sep 30 2026 kamm3r - 0.2.0-1
- Port the upstream Omarchy v4l2 loopback relay to Fedora.
