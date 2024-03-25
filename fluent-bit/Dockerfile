FROM fluent/fluent-bit:2.2.2-debug

COPY fluent-bit.conf /fluent-bit/etc/fluent-bit.conf
COPY delay-sigterm.sh /fluent-bit/delay-sigterm.sh
ENTRYPOINT ["/fluent-bit/delay-sigterm.sh"]
