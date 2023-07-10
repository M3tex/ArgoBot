#!/bin/bash

# Script de gestion du bot (lancement, arrêt, etc.)

day=$(date +"%F")
timestamp=$(date +"%H_%M_%S")



start_bot() {
    # Création du dossier du jour s'il n'existe pas encore
    # (jour du lancement du bot)
    mkdir -p logs/$day

    echo "Lancement du bot..."
    nohup python3 -u argobot/main.py &> "logs/$day/nohup_$timestamp.out" &
    echo $! > pid

    # Pour accéder facilement au log courant
    rm logs/current.log > /tmp/trash
    ln -s $day/nohup_$timestamp.out logs/current.log
}


stop_bot() {
    kill -s 10 $(cat pid)
    echo "Bot hors ligne"
    sleep 0.1

    while ps | grep $(cat pid);
    do 
        kill $(cat pid)
    done
}


if [ "$#" -lt "1" ]; then
    echo "Utilisation: $0 [start|stop|restart]"
    exit 1;
fi


if [ $1 = "start" ]; then
    start_bot
fi


if [ $1 = "stop" ]; then
    stop_bot
fi


if [ $1 = "restart" ]; then
    stop_bot
    sleep 0.25
    start_bot
fi


if [[ $1 =~ ^log.* ]]; then
    cat logs/current.log
fi