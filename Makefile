build-env:
	export FASTGPT_API_KEY="fastgpt-pAC7ttUNFMUNJIY7MoXkVvU5zhMcS6iidDPvFEvab1u3wvcr5ZtVEm7WInSymB7"
	cd  voice-assistant; rm -rf node_modules; npm install
# ------------------------------------------------------------------------

run-site:
	cd  voice-assistant; rm -rf .tmp
	cd  voice-assistant; npm run serve
# ------------------------------------------------------------------------

run-mcp:
	cd WALL-E-MCP; go run main.go
# ------------------------------------------------------------------------

run-serve:
	cd WALL-E-SERVE; go clean -cache; go run main.go