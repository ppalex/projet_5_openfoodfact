# Projet 5: OpenFoodFact

## Description

The goal of this project is to create an application which interacts with the Open Food Facts products database. It 

The application uses the API from Open Food Fact to download a bunch of products classified by categories.

Once the products are downloaded the application fills a Mysql database.

Then, a user can launch the program, choose product from categories and the program will compare and propose a substiute to the product.
The substitute is a product healthier than the selected product.

The user can also safe the substitte in the database.

## Language

* Python3

## Requirements

Use the following command in terminal to install requirements:

```
pip install -r requirements.txt

## Features

* Look up for products in Open Food Facts database;
* CLI application;
* The user interacts with the application in the console;
* 


## Prerequisite

First, it is necessary to create a MySql local database.
Once the databse is created, you can fill the connection information in the following file: Configuration\config.yml
