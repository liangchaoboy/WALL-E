run-site:
	cd  voice-assistant; rm -rf .tmp
	cd  voice-assistant; npm run serve
# ------------------------------------------------------------------------

run-mcp:
	cd WALL-E-MCP; go run main.go
# ------------------------------------------------------------------------

run-serve:
	cd WALL-E-SERVE; 
	go clean -cache;
	go run main.go