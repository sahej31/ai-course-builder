start:
	docker compose up -d

stop:
	docker compose down

logs:
	docker compose logs -f backend

pull-model:
	docker exec -it ollama ollama pull llama3.1:8b
