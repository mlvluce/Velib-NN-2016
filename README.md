# Predicting full and empty stations for the operations of bike-sharing systems

This term project was completed during the 2016 Spring semester for the class *15.077 - Statistical Learning and Data Mining* at MIT. It focuses on a key issue of bike-sharing systems around the world to ensure the reliability of the system: predicting the availability of bikes and docking points at any station of the network. The summary below exposes the objective of the project and briefly presents the modeling work. The final report is available in `report.pdf` with detailed explanations, supporting graphs and illustrations.

## Motivations

Users of public bicycle schemes expect to find an available bicyle close to their origin and to be able to drop it near their destination. For the operators, it means that they should avoid as much as possible the situations where stations are completely empty or completely full, forcing users to walk to another station to find bikes or docking points.

## Methodology

The size of its network and the availability of public data accessible through an API makes Paris' bike-sharing system Vélib a good case study for the project. The familiarity of the author with the city also helps drive the analysis in meaningful directions.

Since the public API from JC Decaux, Vélib's operator, only provides real-time data, the first step of the study consists in automating the collection of historical data which are necessary to train the predition model. In `api.py`, data are fetched every minute from the API endpoint, and written in a *.csv* file. To limit the number of rows and the size of the database, the row of a station is only saved in the event that at least one bike was either picked up or dropped off since the last recorded datapoint.

The data are then pre-processed in `preprocessing.py`. The occupancy rate, defined by the ratio of the number of available bikes divided by the total number of bike stands, is calculated every five minutes for each station. Two datasets are created: one is the occupancy profile through the day of stations; the second is obtained by adding a variable that denotes if the station is observed to become empty, full or neither during the next sixty minutes, given an hour of the day and the occupancy rate at that time. This variable takes three values: *-1* for empty, *1* for full and *0* for neither.

In a `clustering.py`, 1,229 stations are clustered into four groups using a k-means algorithm based on their occupancy rate daily profiles available in the first dataset. Plotting the location of the stations belonging to each group on a map of Paris helps validate the results by adding some geographic and economic context. In `cluster_map.py`, a *.kml* file is generated to facilitate the visualization by importing the data in Google Maps. After this step, the number of degrees of freedom is greatly reduced and over a thousand station identifiers are replaced with just 4 group numbers.

Eventually, a neural network is built and trained on the second dataset to predict if a station will empty or fill itself within the next hour. As shown in `neuralnet.py`, the learning rate and the number of neurons in the hidden layer were fine-tuned over a wide range of possible value, preserving the ones with the lowest training errors.

## Conclusions

Although many parameters were not considered and can be used to refine the model, the simple model exposed above yields already satisfactory results, with a prediction score of about 88%. To go further, network effects with the influence of nearby stations could be accounted for, the impact of weather should be studied and modeling the time series nature of the data can be explored.