/* Exercise an in-flight wl_registry.bind after output removal on a test server. */
#include <wayland-client.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static unsigned latest_output;
static void global(void *data, struct wl_registry *registry, unsigned name,
                   const char *interface, unsigned version) {
    (void)data; (void)registry; (void)version;
    if (!strcmp(interface, "wl_output")) latest_output = name;
}
static void removed(void *data, struct wl_registry *registry, unsigned name) {
    (void)data; (void)registry; (void)name;
}
int main(void) {
    struct wl_display *display = wl_display_connect(NULL);
    if (!display) return 2;
    struct wl_registry *registry = wl_display_get_registry(display);
    const struct wl_registry_listener listener = {global, removed};
    wl_registry_add_listener(registry, &listener, NULL);
    setvbuf(stdout, NULL, _IOLBF, 0);
    if (wl_display_roundtrip(display) < 0) return 3;
    printf("READY %u\n", latest_output);
    char command[80];
    while (fgets(command, sizeof(command), stdin)) {
        if (!strncmp(command, "sync", 4)) {
            if (wl_display_roundtrip(display) < 0) return 4;
            printf("READY %u\n", latest_output);
        } else {
            unsigned name;
            if (sscanf(command, "bind %u", &name) != 1) return 5;
            /* Deliberately do not dispatch the queued global_remove first. */
            struct wl_output *output = wl_registry_bind(registry, name, &wl_output_interface, 3);
            if (!output || wl_display_roundtrip(display) < 0) {
                printf("ERROR %d\n", wl_display_get_error(display));
                return 1;
            }
            puts("BOUND");
            wl_output_release(output);
            if (wl_display_roundtrip(display) < 0) return 6;
            puts("DRAINED");
            break;
        }
    }
    wl_registry_destroy(registry);
    wl_display_disconnect(display);
    return 0;
}
