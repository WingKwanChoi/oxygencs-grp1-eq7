### 1.Générer le fichier requirements.txt
Exécutez cette commande dans votre terminal pour créer un fichier requirements.txt à partir de votre Pipfile.lock :
```bash
pipenv lock -r > requirements.txt
```

### 2.Construire l'image Docker :
Exécutez la commande suivante pour construire l'image Docker :
```bash
docker build -t oxygencs-app .
```

### 3.Exécuter le conteneur Docker :
Utilisez la commande suivante pour exécuter le conteneur Docker :
```bash
docker run -d --name oxygencs-container -e HOST=http://159.203.50.162 -e TOKEN=999109532408abf795f3 -e T_MAX=25 -e T_MIN=18 -e PG_USER=user01eq7 -e PG_HOST=157.230.69.113 -e PG_DATABASE=db01eq7 -e PG_PASSWORD=nJCxUQQGEzAYKnWw -e PG_PORT=5432 oxygencs-app
```
Remplacez your_host, your_token, your_tmax, your_tmin, et your_database_url par les valeurs appropriées.
*Éléments déja remplacer pour l'équipe 7 du groupe 01


### 4.Configurer un dépôt DockerHub :
- Créez un compte sur DockerHub si ce n'est pas déjà fait.
- Connectez-vous depuis votre terminal avec la commande :
```bash
docker login
```

- Taggez votre image Docker et poussez-la sur DockerHub :
```bash
docker tag oxygencs-app your_dockerhub_username/oxygencs-app
docker push your_dockerhub_username/oxygencs-app
```
Remplacez your_dockerhub_username par la valeur appropriée.