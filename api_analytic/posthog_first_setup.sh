set -e

export DEBIAN_FRONTEND=noninteractive
# Automatically restart without asking.
# this gets around needrestart command halting for user input
export RESTART_MODE=l
export POSTHOG_APP_TAG="${POSTHOG_APP_TAG:-latest}"
export SENTRY_DSN="${SENTRY_DSN:-'https://public@sentry.example.com/1'}"

POSTHOG_SECRET=$(head -c 28 /dev/urandom | sha224sum -b | head -c 56)
export POSTHOG_SECRET

# Talk to the user
echo "Welcome to the single instance PostHog installer 🦔"
echo ""
echo "⚠️  You really need 4gb or more of memory to run this stack ⚠️"
echo ""
echo "Power user or aspiring power user?"
echo "Check out our docs on deploying PostHog! https://posthog.com/docs/self-host/deploy/hobby"
echo ""

if ! [ -z "$1" ]
then
export POSTHOG_APP_TAG=$1
else
echo "What version of PostHog would you like to install? (We default to 'latest')"
echo "You can check out available versions here: https://hub.docker.com/r/posthog/posthog/tags"
read -r POSTHOG_APP_TAG_READ
if [ -z "$POSTHOG_APP_TAG_READ" ]
then
    echo "Using default and installing $POSTHOG_APP_TAG"
else
    export POSTHOG_APP_TAG=$POSTHOG_APP_TAG_READ
    echo "Using provided tag: $POSTHOG_APP_TAG"
fi
fi
echo ""
if ! [ -z "$2" ]
then
export DOMAIN=$2
else
echo "Let's get the exact domain PostHog will be installed on"
echo "Make sure that you have a Host A DNS record pointing to this instance!"
echo "This will be used for TLS 🔐"
echo "ie: test.posthog.net (NOT an IP address)"
read -r DOMAIN
export DOMAIN=$DOMAIN
fi
echo "Ok we'll set up certs for https://$DOMAIN"
echo ""
echo "We will need sudo access so the next question is for you to give us superuser access"
echo "Please enter your sudo password now:"
sudo echo ""
echo "Thanks! 🙏"
echo ""
echo "Ok! We'll take it from here 🚀"

echo "Making sure any stack that might exist is stopped"
sudo -E docker-compose -f docker-compose.yml stop &> /dev/null || true

# send log of this install for continued support!
curl -o /dev/null -L --header "Content-Type: application/json" -d "{
    \"api_key\": \"sTMFPsFhdP1Ssg\",
    \"distinct_id\": \"${DOMAIN}\",
    \"properties\": {\"domain\": \"${DOMAIN}\"},
    \"type\": \"capture\",
    \"event\": \"magic_curl_install_start\"
}" https://app.posthog.com/batch/ &> /dev/null

# update apt cache
echo "Grabbing latest apt caches"

# clone posthog
echo "Installing PostHog 🦔 from Github"
# try to clone - if folder is already there pull latest for that branch
git clone https://github.com/PostHog/posthog.git &> /dev/null || true
cd posthog

if [[ "$POSTHOG_APP_TAG" = "latest-release" ]]
then
    git fetch --tags
    latestReleaseTag=$(git describe --tags `git rev-list --tags --max-count=1`)
    echo "Checking out latest PostHog release: $latestReleaseTag"
    git checkout $latestReleaseTag
elif [[ "$POSTHOG_APP_TAG" = "latest" ]]
then
    echo "Pulling latest from current branch: $(git branch --show-current)"
    git pull
else
    releaseTag="${POSTHOG_APP_TAG/release-/""}"
    git fetch --tags
    echo "Checking out PostHog release: $releaseTag"
    git checkout $releaseTag
fi

cd ..

if [ -n "$3" ]
then
export TLS_BLOCK="acme_ca https://acme-staging-v02.api.letsencrypt.org/directory"
fi

# rewrite caddyfile
rm -f Caddyfile
envsubst > Caddyfile <<EOF
{
$TLS_BLOCK
}
$DOMAIN, :80, :443 {
reverse_proxy http://web:8000
}
EOF

# Write .env file
envsubst > .env <<EOF
POSTHOG_SECRET=$POSTHOG_SECRET
SENTRY_DSN=$SENTRY_DSN
DOMAIN=$DOMAIN
EOF

# write entrypoint
# NOTE: this is duplicated in bin/upgrade-hobby, so if you change it here,
# change it there too.
rm -rf compose
mkdir -p compose
cat > compose/start <<EOF
#!/bin/bash
/compose/wait
./bin/migrate
./bin/docker-server
EOF
chmod +x compose/start

cat > compose/temporal-django-worker <<EOF
#!/bin/bash
./bin/temporal-django-worker
EOF
chmod +x compose/temporal-django-worker

# write wait script
cat > compose/wait <<EOF
#!/usr/bin/env python3

import socket
import time

def loop():
    print("Waiting for ClickHouse and Postgres to be ready")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('clickhouse', 9000))
        print("Clickhouse is ready")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('db', 5432))
        print("Postgres is ready")
    except ConnectionRefusedError as e:
        time.sleep(5)
        loop()

loop()
EOF
chmod +x compose/wait

echo "Configuring Docker Compose...."
echo "Configuring Docker Compose...."
rm -f docker-compose.yml
cp posthog/docker-compose.base.yml docker-compose.base.yml
cp posthog/docker-compose.hobby.yml docker-compose.yml.tmpl
envsubst < docker-compose.yml.tmpl > docker-compose.yml
rm docker-compose.yml.tmpl
echo "Starting the stack!"
docker-compose -f docker-compose.yml up -d

echo "We will need to wait ~5-10 minutes for things to settle down, migrations to finish, and TLS certs to be issued"
echo ""
echo "⏳ Waiting for PostHog web to boot (this will take a few minutes)"
bash -c 'while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' localhost/_health)" != "200" ]]; do sleep 5; done'
echo "⌛️ PostHog looks up!"
echo ""
echo "🎉🎉🎉  Done! 🎉🎉🎉"
# send log of this install for continued support!
curl -o /dev/null -L --header "Content-Type: application/json" -d "{
    \"api_key\": \"sTMFPsFhdP1Ssg\",
    \"distinct_id\": \"${DOMAIN}\",
    \"properties\": {\"domain\": \"${DOMAIN}\"},
    \"type\": \"capture\",
    \"event\": \"magic_curl_install_complete\"
}" https://app.posthog.com/batch/ &> /dev/null
echo ""
echo "To stop the stack run 'docker-compose stop'"
echo "To start the stack again run 'docker-compose start'"
echo "If you have any issues at all delete everything in this directory and run the curl command again"
echo ""
echo 'To upgrade: run /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/posthog/posthog/HEAD/bin/upgrade-hobby)"'
echo ""
echo "PostHog will be up at the location you provided!"
echo "https://${DOMAIN}"
echo ""
echo "It's dangerous to go alone! Take this: 🦔"