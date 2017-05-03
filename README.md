# Recipe Ingredient Associations
### Applied Data Science Project, Spring 2017

This project scrapes slow cooker recipes from [Big Oven](https://www.bigoven.com/), processes the data down to a workable base table, and develops association rules and jaccard-distance hierarchical clustering using ingredient data.

The analytical base table for these models consists of recipe titles and ingredients. 

For R's arules library, the data had to be converted to a 'market basket' format where each row holds a list of ingredient names in contiguous cells with no organized system of columns. 

For hierarchical clustering, the recipes were one-hot encoded across 400 columns representing the 400 unique ingredients in the final recipe set. Each cell [i,j] contains a binary value to indicate the presence of ingredient j in recipe i. Jaccard distance is used to perform the clustering since it works well with sparse matrices of binary data and doesn't attend to co-absences.

A presentation with visualizations of these models is available at 

https://drive.google.com/open?id=12DSyk2jY8j-WYSiFrXqIJ1WJ5gEktOXUDXKX1ZzUGu8

and a more comprehensive report is available at

https://drive.google.com/open?id=1Bz0F-vRx5z42oi58eRohUDQZme9rnus_KrHfBzpZcig
