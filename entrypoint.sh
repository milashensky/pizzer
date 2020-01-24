#!/bin/sh
while [ ! -f /shared/.migration.done ]; do
	echo "waiting for migration"
	sleep 5
done
exec "$@"
