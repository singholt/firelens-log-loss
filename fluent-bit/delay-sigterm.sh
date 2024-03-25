#!/bin/sh

# The selected code is a shell script that handles the SIGTERM signal.
# When the script receives a SIGTERM signal, it prints a message,
# waits for 20 seconds, then kills a child process and waits for it
# to terminate. The script then starts the Fluent Bit service with a
# specific configuration file and assigns its process ID to the
# variable `child`. The script will then wait for the `child`
# process to terminate.
#
# The purpose of this script is to give Fluent Bit time to finish
# before receiving a SIGTERM signal, to ensure the inputs remain open
# for a while after the signal is received, therefore after the process
# generates the logs terminates.
_term() {
  echo "Caught SIGTERM signal!"
  sleep 20
  echo "Killing child process!"
  kill -TERM "$child"
  wait "$child"
}

trap _term TERM

/fluent-bit/bin/fluent-bit -c /fluent-bit/etc/fluent-bit.conf &
# Switch to netcat to discard Fluent Bit as the source of the issue.
#nc -lkU /var/run/fluent.sock &

child=$!
wait "$child"
