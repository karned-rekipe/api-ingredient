# Starter

## Base de données
Installer un serveur MongoDB sur votre machine.
```shell
docker pull mongo
docker run -d -p 27017:27017 --name mongodb mongo
```

## API 
A la racine du projet se trouve un Dockerfile qui permet de lancer l'API en local.
```shell
docker build -t rekipe-api-ingredient .
docker run -d --name rekipe-api-ingredient -p 8001:8001 rekipe-api-ingredient
```