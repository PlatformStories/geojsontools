# Using geojson_tools to manipulate a training dataset

In this example we begin with a geojson of AOIs that we would like to use to train a classifier. To prepare for training we must classify each AOI, separate the ground truth into train and test data, and potentially create a balanced set to train on if our model is sensitive to class imbalance.

Here we use geojson_tools to accomplish these tasks. In this walkthrough you will start with the following files, which can be found in the sample-dataset folder:  

1. <b>[features.geojson](https://github.com/PlatformStories/geojson_tools/blob/master/examples/create-dataset/features.geojson)</b> - A collection of AOIs that contain the geometries and feature ids of our training data.  
2. <b>classes.pkl</b> - A pickled list of class names ('Buildings' or 'No Buildings') associated with each AOI.

We will combine the above two files to create our ground truth dataset and then further manipulate that geojson to create train, test, and balanced datasets.

1. Begin by importing geojson_tools and loading the list of class names from classes.pkl.

    ```python
    import numpy, pickle
    import geojson_tools as gt

    # Load the list of ground truth classes
    with open('classes.pkl', 'r') as f:
        classes = pickle.load(f)
    ```

2. Next we use ```write_properties_to``` to combine the class labels with features.geojson to create ground_truth.geojson:

    ```python
    # Combine classes with features to create ground_truth.geojson
    gt.write_properties_to(classes, property_names=['class_name'],
                           input_file='features.geojson',
                           output_file='ground_truth.geojson')
    ```

3. Now split ground_truth.geojson into train and test data as follows:

    ```python
    # Create train.geojson and test.geojson from ground_truth.geojson
    gt.create_train_test('ground_truth.geojson', test_size=0.15)
    ```

4. Finally, create a balanced training dataset from train.geojson:

    ```python
    # Create a balanced version of train.geojson
    gt.create_balanced_geojson('train.geojson', classes=['No Buildings', 'Buildings'],
                           output_file='train_balanced.geojson')
    ```


You should now have the following additional files in your working directory:

1. <b>ground_truth.geojson</b>: Classified version of features.geojson
2. <b>test.geojson</b>: Testing data for our model
3. <b>train.geojson</b>: Imbalanced training data for our classifier
4. <b>train_balanced.geojson</b>: Balanced training data for our classifier
