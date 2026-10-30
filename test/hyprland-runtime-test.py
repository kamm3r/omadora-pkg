#!/usr/bin/env python3
"""Launch a disposable nested compositor; never use the real session's IPC socket."""
import argparse
import json
import os
from pathlib import Path
import select
import signal
import shlex
import socket
import subprocess
import tempfile
import time

parser = argparse.ArgumentParser()
parser.add_argument('--hyprland', type=Path, required=True)
parser.add_argument('--plugin', type=Path)
parser.add_argument('--rejected-plugin', type=Path)
args = parser.parse_args()
binary = args.hyprland.resolve()
parent_runtime = Path(os.environ['XDG_RUNTIME_DIR'])
parent_display = Path(os.environ['WAYLAND_DISPLAY'])
if not parent_display.is_absolute():
    parent_display = parent_runtime / parent_display
sandbox = Path(tempfile.mkdtemp(prefix='hc-'))
runtime = sandbox / 'r'
runtime.mkdir(mode=0o700)
for name in ['home', 'config', 'state', 'data']:
    (sandbox / name).mkdir()
config = sandbox / 'hyprland.lua'
config.write_text("hl.config({ xwayland = { enabled = false } })\nhl.monitor({ output = '', mode = '1280x720@60', position = 'auto', scale = '1' })\n")
env = os.environ.copy()
for name in ['HYPRLAND_INSTANCE_SIGNATURE', 'SWAYSOCK', 'DISPLAY', 'LD_PRELOAD']:
    env.pop(name, None)
env.update(HOME=str(sandbox/'home'), XDG_RUNTIME_DIR=str(runtime),
           XDG_CONFIG_HOME=str(sandbox/'config'), XDG_STATE_HOME=str(sandbox/'state'),
           XDG_DATA_HOME=str(sandbox/'data'), WAYLAND_DISPLAY=str(parent_display),
           HYPRLAND_NO_SD_VARS='1', HYPRLAND_NO_SD_TARGET='1', HYPRLAND_NO_SD_NOTIFY='1',
           HYPRLAND_NO_RT='1', HYPRLAND_NO_CRASHREPORTER='1',
           AQ_DRM_DEVICES='/dev/dri/omadora-test-no-kms-device',
           LIBSEAT_BACKEND='omadora-test-no-seat')
log = (sandbox/'compositor.log').open('w')
process = subprocess.Popen(['dbus-run-session', '--', str(binary), '--config', str(config)],
                           env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
ipc = None
client = None

def request(command):
    assert ipc is not None and ipc.is_relative_to(runtime), 'Refusing non-test IPC socket'
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(8)
        connection.connect(str(ipc))
        connection.sendall(command.encode())
        data = bytearray()
        while chunk := connection.recv(65536):
            data.extend(chunk)
        return data.decode()

def line():
    if not select.select([client.stdout], [], [], 8)[0]:
        raise AssertionError('Test Wayland client did not respond')
    return client.stdout.readline().strip()

try:
    deadline = time.monotonic() + 35
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise AssertionError('Nested compositor exited during startup')
        sockets = list(runtime.glob('hypr/*/.socket.sock'))
        if sockets:
            ipc = sockets[0]
            try:
                monitors = json.loads(request('j/monitors'))
                if monitors:
                    break
            except (OSError, ValueError):
                pass
        time.sleep(.1)
    else:
        raise AssertionError('Nested compositor did not create an output')
    assert request('/configerrors').strip() in ['', 'ok'], 'Config errors in test compositor'
    flags = shlex.split(subprocess.check_output(['pkg-config','--cflags','--libs','wayland-client'],text=True))
    client_binary = sandbox / 'late-bind'
    subprocess.run(['cc', str(Path(__file__).with_name('hyprland-late-bind.c')), '-o', str(client_binary), *flags], check=True)
    client_env = env.copy()
    display_sockets = [p for p in runtime.glob('wayland-*') if p.is_socket()]
    assert len(display_sockets) == 1, display_sockets
    client_env['WAYLAND_DISPLAY'] = str(display_sockets[0])
    client = subprocess.Popen([str(client_binary)], env=client_env, stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE, stderr=(sandbox/'client.log').open('w'), text=True, bufsize=1)
    first = line()
    assert first.startswith('READY '), first
    assert request('/output create headless OMADORA-LATE-BIND').strip() == 'ok'
    client.stdin.write('sync\n'); client.stdin.flush()
    added = line()
    assert added.startswith('READY ') and added != first, (first, added)
    global_id = int(added.split()[1])
    assert request('/output remove OMADORA-LATE-BIND').strip() == 'ok'
    deadline = time.monotonic() + 2
    while any(m['name']=='OMADORA-LATE-BIND' for m in json.loads(request('j/monitors'))):
        assert time.monotonic() < deadline, 'Test output removal did not complete'
        time.sleep(.02)
    # Allow the server to finish deferred retirement while this client does not dispatch.
    time.sleep(.15)
    # Reusing the name retires the previous global, reproducing a connector flap.
    assert request('/output create headless OMADORA-LATE-BIND').strip() == 'ok'
    client.stdin.write(f'bind {global_id}\n'); client.stdin.flush()
    result = line()
    assert result == 'BOUND', 'Late wl_output bind disconnected the client: ' + result
    assert line() == 'DRAINED'
    assert client.wait(timeout=5) == 0
    print('PASS: in-flight wl_output bind survives output removal and releases cleanly')
    if args.rejected_plugin:
        response = request('/plugin load ' + str(args.rejected_plugin.resolve()))
        assert response.strip() != 'ok' and ('mismatch' in response.lower() or 'version' in response.lower()), response
        print('PASS: plugin built for unpatched compositor rejected')
    if args.plugin:
        assert request('/plugin load ' + str(args.plugin.resolve())).strip() == 'ok'
        assert request('/plugin unload ' + str(args.plugin.resolve())).strip() == 'ok'
        print('PASS: matching titlebars loads and unloads in the nested session')
    response = request('/dispatch hl.dsp.exit()')
    assert response.strip() == 'ok', response
    assert process.wait(timeout=15) == 0
    print('PASS: compositor exits cleanly')
finally:
    if client and client.poll() is None:
        client.terminate()
        client.wait(timeout=5)
    if process.poll() is None:
        try:
            if ipc:
                request('/dispatch hl.dsp.exit()')
        except OSError:
            pass
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=5)
    log.close()
    print('Test logs:', sandbox)
