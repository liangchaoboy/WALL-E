build-env:
	export FASTGPT_API_KEY="get api key from chentao or liangcha"
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