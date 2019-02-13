#!/bin/bash
sudo systemctl restart nginx
sudo systemctl stop flaskproject
sudo systemctl start flaskproject
sudo systemctl enable flaskproject
