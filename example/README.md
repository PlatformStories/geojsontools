# Create training and test data sets

In this example, we use geosjontools to create training and test data sets which can be used for machine learning.
There are two files in this folder: [features.geojson](https://github.com/PlatformStories/geojsontools/blob/master/examples/create-dataset/features.geojson), which contains a number of geometries, each indexed by a feature id, and classes.pkl, a pickled list of class names corresponding to the geometries in features.geojson.

1. Import geojsontools and load the list of class names from classes.pkl.

    ```python
    import numpy, pickle
    import geojsontools as gt

    # Load the list of ground truth classes
    with open('classes.pkl', 'r') as f:
        classes = pickle.load(f)
    ```

2. Combine the class labels with features.geojson to create ground_truth.geojson:

    ```python
    # Combine classes with features to create ground_truth.geojson
    gt.write_properties_to(classes, property_names=['class_name'],
                           input_file='features.geojson',
                           output_file='ground_truth.geojson')
    ```

3. Split ground_truth.geojson into train and test data as follows:

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

You can upload these files for viewing to [geojson.io](geojson.io).
