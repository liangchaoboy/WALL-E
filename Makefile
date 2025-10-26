build-env:
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
	export FASTGPT_API_KEY="get api key from liangchao or chentao or zhaojianfeng " && \
	cd WALL-E-SERVE && \
	go clean -cache && \
	go run main.go