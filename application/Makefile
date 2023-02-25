server:
	python -m uvicorn api:api --port 8010 --host "0.0.0.0"

app:
	streamlit run app.py

build_image:
	sudo docker build -t mlops:latest .

run_server:
	sudo docker run -t --rm -p 8010:8010 mlops:latest