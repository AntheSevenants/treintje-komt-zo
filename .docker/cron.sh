if ! test -f "trajectories.json"; then
    echo "No trajectories.json found in root directory. Exiting..."
    exit 1
fi

printenv > /etc/environment
cron -f