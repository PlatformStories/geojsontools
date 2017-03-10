# Contains functions for manipulating jsons and geojsons.

import geojson
import numpy as np
import sys
import random
import subprocess
import os


def join(input_files, output_file):
    '''
    Join geojsons into one. The spatial reference system of the output file is the same
        as the one of the last file in the list.

    Args:
        input_files (list): List of file name strings.
        output_file (str): Output file name.
    '''

    # get feature collections
    final_features = []
    for file in input_files:
        with open(file) as f:
            feat_collection = geojson.load(f)
            final_features += feat_collection['features']

    feat_collection['features'] = final_features

    # write to output file
    with open(output_file, 'w') as f:
        geojson.dump(feat_collection, f)


def split(input_file, file_1, file_2, no_in_first_file):
    '''
    Split a geojson in two separate files.

    Args:
        input_file (str): Input filename.
        file_1 (str): Output file name 1.
        file_2 (str): Output file name 2.
        no_features (int): Number of features in input_file to go to file_1.
        output_file (str): Output file name.
    '''

    # get feature collection
    with open(input_file) as f:
        feat_collection = geojson.load(f)

    features = feat_collection['features']
    feat_collection_1 = geojson.FeatureCollection(features[0:no_in_first_file])
    feat_collection_2 = geojson.FeatureCollection(features[no_in_first_file:])

    with open(file_1, 'w') as f:
        geojson.dump(feat_collection_1, f)

    with open(file_2, 'w') as f:
        geojson.dump(feat_collection_2, f)


def get_from(input_file, property_names):
    '''
    Reads a geojson and returns a list of value tuples, each value corresponding to a
        property in property_names.

    Args:
        input_file (str): File name.
        property_names: List of strings; each string is a property name.

    Returns:
        List of value tuples.
    '''

    # get feature collections
    with open(input_file) as f:
        feature_collection = geojson.load(f)

    features = feature_collection['features']
    values = [tuple([feat['properties'].get(x)
                     for x in property_names]) for feat in features]

    return values


def write_properties_to(data, property_names, input_file, output_file, filter=None):
    '''
    Writes property data to polygon_file for all geometries indicated in the filter, and
        creates output file. The length of data must be equal to the number of geometries
        in the filter. Existing property values are overwritten.

    Args
        data (list): List of tuples. Each entry is a tuple of dimension equal to
            property_names.
        property_names (list): Property names.
        input_file (str): Input file name.
        output_file (str): Output file name.
        filter (dict): Filter format is {'property_name':[value1,value2,...]}.What this
            achieves is to write the first entry of data to the properties of the feature
            with 'property_name'=value1, and so on. This makes sense only if these values
            are unique. If Filter=None, then data is written to all geometries in the
            input file.
    '''

    with open(input_file) as f:
        feature_collection = geojson.load(f)

    features = feature_collection['features']

    if filter is None:
        for i, feature in enumerate(features):
            for j, property_value in enumerate(data[i]):
                feature['properties'][property_names[j]] = property_value
    else:
        filter_name = filter.keys()[0]
        filter_values = np.array(filter.values()[0])
        for feature in features:
            compare_value = feature['properties'][filter_name]
            ind = np.where(filter_values == compare_value)[0]
            if len(ind) > 0:
                for j, property_value in enumerate(data[ind]):
                    feature['properties'][property_names[j]] = property_value

    feature_collection['features'] = features

    with open(output_file, 'w') as f:
        geojson.dump(feature_collection, f)


def find_unique_values(input_file, property_name):
    '''
    Find unique values of a given property in a geojson file.

    Args
        input_file (str): File name.
        property_name (str): Property name.
    Returns
        List of distinct values of property. If property does not exist, it returns None.
    '''

    with open(input_file) as f:
        feature_collection = geojson.load(f)

    features = feature_collection['features']
    values = np.array([feat['properties'].get(property_name)
                       for feat in features])
    return np.unique(values)


def filter_by_property(input_file, output_file, property_name, values):
    '''
    Create a file containing only features with specified property value(s) from
        input_file.

    Args
        input_file (str): File name.
        output_file (str): Output file name.
        property_name (str): Name of the feature property to filter by.
        values (list): Value(s) a feature may have for property_name if it is to be
            included in output_file.
    '''

    filtered_feats = []
    if not output_file.endswith('.geojson'):
        output_file += '.geojson'

    # Load feature list
    with open(input_file) as f:
        feature_collection = geojson.load(f)

    # Filter feats by property_name
    for feat in feature_collection['features']:
        if feat['properties'][property_name] in values:
            filtered_feats.append(feat)

    feature_collection['features'] = filtered_feats

    # Save filtered file
    with open(output_file, 'wb') as f:
        geojson.dump(f)


def create_train_test(input_file, output_file=None, test_size=0.2):
    '''
    Split a geojson file into train and test features. Saves features as geojsons in the
        working directory under the same file name with train and test prefixes to the
        original file name.

    Args
        input_file (str): File name
        output_file (str): Name to use after the train_ and test_ prefixes for the saved
            files. Defaults to None (files will be saves as train.geojson and
            test.geojson).
        test_size (float or int): Amount of features to set aside as test data. If less
            than one will be interpreted as a proportion of the total feature collection.
            Otherwise it is the amount of features to use as test data. Defaults to 0.2.
    '''

    with open(input_file) as f:
        data = geojson.load(f)
        features = data['features']
        np.random.shuffle(features)

    # Convert test size from proportion to number of polygons
    if test_size <= 1:
        test_size = int(test_size * len(features))

    # Name output files
    test_out, train_out = 'test.geojson', 'train.geojson'

    if output_file:
        if not output_file.endswtih('.geojson'):
            output_file += '.geojson'
        test_out, train_out='test_{}'.format(output_file), 'train_{}'.format(output_file)

    # Save train and test files
    data['features'] = features[:test_size]
    with open(test_out, 'wb') as test_file:
        geojson.dump(data, test_file)

    data['features'] = features[test_size:]
    with open(train_out, 'wb') as train_file:
        geojson.dump(data, train_file)


def create_balanced_geojson(input_file, classes, output_file='balanced.geojson',
                            samples_per_class=None):
    '''
    Create a geojson comprised of balanced classes from the class_name property in
        input_file. Randomly selects polygons from all classes.

    Args:
        input_file (str): File name
        classes (list[str]): Classes in input_file to include in the balanced output file.
            Must exactly match the 'class_name' property in the features of input_file.
        output_file (str): Name under which to save the balanced output file. Defualts to
            balanced.geojson.
        samples_per_class (int or None): Number of features to select per class in
            input_file. If None will use the smallest class size. Defaults to None.
    '''

    if not output_file.endswith('.geojson'):
        output_file += '.geojson'

    with open(input_file) as f:
        data = geojson.load(f)

    # Sort classes in separate lists
    sorted_classes = {clss : [] for clss in classes}

    for feat in data['features']:
        try:
            sorted_classes[feat['properties']['class_name']].append(feat)
        except (KeyError):
            continue

    # Determine sample size per class
    if not samples_per_class:
        smallest_class = min(sorted_classes, key=lambda clss: len(sorted_classes[clss]))
        samples_per_class = len(sorted_classes[smallest_class])

    # Randomly select features from each class
    try:
        samps = [random.sample(feats, samples_per_class) for feats in sorted_classes.values()]
        final = [feat for sample in samps for feat in sample]
    except (ValueError):
        raise Exception('Insufficient features in at least one class. Set ' \
                            'samples_per_class to None to use maximum amount of '\
                            'features.')

    # Shuffle and save balanced data
    np.random.shuffle(final)
    data['features'] = final

    with open(output_file, 'wb') as f:
        geojson.dump(data, f)
