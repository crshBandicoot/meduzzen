Start app by executing:
    uvicorn src.main:app --reload
Docker:
    sudo docker build . -t fastapiapp
    sudo docker run --mount type=bind,source="$(pwd)"/src,target=/app --name fastapiApp -p 80:80 -d fastapiapp