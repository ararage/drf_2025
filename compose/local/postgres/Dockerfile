# Enable BuildKit syntax so we can mount and inspect the build context at build-time
# (required for the conditional check below)
# syntax=docker/dockerfile:1.4
FROM postgres:15.15-alpine
COPY ./compose/local/postgres/maintenance/restore.sh /usr/local/bin/maintenance/restore.sh

# Conditional copy: if `backup.bak` exists in the build context, copy it
# to the image and mark the restore script as executable; otherwise print
# a message. This uses a bind mount of the build context and requires
# BuildKit (hence the `syntax` line above).
RUN --mount=type=bind,source=.,target=/build_context \
	/bin/sh -lc 'if [ -f /build_context/backup.bak ]; then \
		cp /build_context/backup.bak /usr/local/bin/backup.bak && \
		chmod +x /usr/local/bin/maintenance/restore.sh && \
		echo "backup.bak exists: copied to /usr/local/bin/backup.bak"; \
	else \
		echo "backup.bak NOT FOUND — skipping copy"; \
	fi'

#RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
#    && rmdir /usr/local/bin/maintenance
# RUN /usr/local/bin/maintenance/restore.sh