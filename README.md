# Classifier

## Background

They say that with Machine Learning you can make predictions without 
explicitly programming it to perform the task. For me, it seems that I 
still need to explicitly build it for the specific task. For example, when I 
made a [collaborative filtering](https://github.com/korjusk/MovieRec) project I
had to:
* collect the data
* clean the data
* analyze the data
* visualize the data
* split the data
* define goal and success
* make baseline predictions
* build a test
* figure out possible complications
* choose frameworks and libraries
* rent a server with Nvidia GPUs
* install and set up everything
* build or find a neural network
* tune hyperparameters
* train it for 10h
* make a prediction with the trained model  

I want to automate all of that.

<br>

## Goal

* Learn to deploy a machine learning project
* Learn how to configure the server and related software
* Build a simple classification model that could predict without being 
explicitly programmed to perform

<br>

## Result

I have a picture of a cat and I want to know if it's a cat or a dog.

<br>

#### Let's go to classifier website [172.83.8.197](http://172.83.8.197/)

![](images/home.png) 

<br>

#### Enter info and click classify

![](images/result.png) 

<br>

#### The model was trained with ~80 Googled pictures like that

![](images/cat.png) 

<br>

The same model can be used with multiple classes and multiple target URLs.
And of course, instead of a cat and a dog you could enter whatever you wish. 
For example 'gun', 'knife' and 'hotdog' or 
'professional linkedin profile' and 'linkedin profile'.

<br>

## Files

* Server setup notes: [setup.md](https://github.com/korjusk/Classifier/blob/master/setup.md)
* Gunicorn config: [gunicorn_config.py](https://github.com/korjusk/Classifier/blob/master/gunicorn/gunicorn_config.py)
* Python code: [flaskproject.py](https://github.com/korjusk/Classifier/blob/master/flaskproject.py) and [wsgi.py](https://github.com/korjusk/Classifier/blob/master/wsgi.py)
* Html code: [index.html](https://github.com/korjusk/Classifier/blob/master/index.html) and [success.html](https://github.com/korjusk/Classifier/blob/master/success.html)
* Bash script: [restarter.sh](https://github.com/korjusk/Classifier/blob/master/restarter.sh)

<br><br>

If the website is not accessible then I probably turned it off.
Let me know if you want to use it.
