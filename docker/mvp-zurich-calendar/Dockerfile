# syntax=docker/dockerfile:1
#
# The calendar connector with the mvp-zurich datasets: the waste-collection
# calendars of the City of Zurich (organic waste, paper, cardboard, household
# waste, the hazardous-waste van) from Open Data Zürich, served behind the
# pack's waste concepts. The base image (docker/calendar-connector of the
# code repository) plus the pack's dataset bundles. The build context is the
# pack's datasets directory, a checkout's datasets/mvp-zurich. Published as
# ghcr.io/<owner>/swiss-tip-calendar:mvp-zurich by the workflow
# container-images.yml; compose.yaml of the code repository starts it beside
# the server behind the profile "calendar".
#
#   docker build -f docker/mvp-zurich-calendar/Dockerfile -t swiss-tip-calendar:mvp-zurich datasets/mvp-zurich
#   SWISSTIP_PACK=mvp-zurich SWISSTIP_CONNECTORS=http://127.0.0.1:8100 docker compose -f ../swiss-tip/compose.yaml --profile calendar up -d --wait
#
# The build fails when a bundle does not validate: the base image's --health
# exits 2 unless every bundle it finds is served.

ARG BASE_IMAGE=swiss-tip-calendar-connector:0.3.2
FROM ${BASE_IMAGE}
ARG DATASET_VERSIONS=""
ARG REVISION=""
LABEL org.opencontainers.image.title="Swiss TIP calendar connector with the mvp-zurich datasets" \
      org.opencontainers.image.description="The waste-collection calendars of the City of Zurich (Open Data Zürich, CC0) served to the Swiss TIP MCP server behind the mvp-zurich waste concepts: organic waste, paper, cardboard, household waste and the hazardous-waste van, by postal code. HTTP on port 8100: /manifest, /lookup, /health. Not reached by callers directly; the server registers it with --connector." \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.version="${DATASET_VERSIONS}" \
      org.opencontainers.image.revision="${REVISION}" \
      swiss-tip.datasets.versions="${DATASET_VERSIONS}"

COPY --chown=10001:10001 . /srv/swiss-tip/datasets/

RUN swisstip-calendar-connector --datasets-dir /srv/swiss-tip/datasets --health > /dev/null
