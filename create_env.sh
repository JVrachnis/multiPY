# Create .env file from .env.example if it doesn't exist
if [ ! -f /workspaces/multiPY/.env ]; then
    cp /workspaces/multiPY/.env.example /workspaces/multiPY/.env
    echo "📋 Created .env file from .env.example"
fi
