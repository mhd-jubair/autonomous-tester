
MAKEFLAGS += --no-print-directory


run-real-webapp:
	@echo "Starting example web application without defect..."
	@uv run example/web_app/app_real.py & 

run-defected-webapp:
	@echo "Starting example web application with defect..."
	@uv run example/web_app/app_defect.py &

webapp-real:
	make run-real-webapp
	@echo "Running the autonomous tester for webapplication without defect..."
	@uv run src/autonomous_tester/main.py --type web_app --endpoint http://localhost:5000
	@fuser -k 5000/tcp

webapp-defected:
	make run-defected-webapp
	@echo "Running the autonomous tester for webapplication with defect..."
	@uv run src/autonomous_tester/main.py --type web_app --endpoint http://localhost:5001
	@fuser -k 5001/tcp

start-api-test:
	@uv run src/autonomous_tester/main.py --type api_app --endpoint http://localhost:8000

api-real:
	@echo "Starting example API without defect..."
	@uv run uvicorn example.api.auth_api_real:app --log-level critical --reload &
	make start-api-test
	@fuser -k 8000/tcp

api-defected:
	@echo "Starting example API with defect..."
	@uv run uvicorn example.api.auth_api_defect:app --log-level critical --reload &
	make start-api-test
	@fuser -k 8000/tcp
