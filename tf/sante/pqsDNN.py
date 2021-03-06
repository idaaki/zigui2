from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np

# Data sets
IRIS_TRAINING = "iris_training.csv"
IRIS_TEST = "iris_test.csv"

# Load datasets.
training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
    filename=IRIS_TRAINING,
    target_dtype=np.int,
    features_dtype=np.float32)
test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
    filename=IRIS_TEST,
    target_dtype=np.int,
    features_dtype=np.float32)

# Specify that all features have real-value data
feature_columns = [tf.contrib.layers.real_valued_column("", dimension=81)]

# Build 3 layer DNN with 10, 20, 10 units respectively.
classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[10, 20, 10],
                                            n_classes=3,
                                            model_dir="/tmp/iris_model")

# Fit model.
classifier.fit(x=training_set.data,
               y=training_set.target,
               steps=2000)

# Evaluate accuracy.
accuracy_score = classifier.evaluate(x=test_set.data,
                                     y=test_set.target)["accuracy"]
print('Accuracy: {0:f}'.format(accuracy_score))

# Classify two new flower samples.
new_samples = np.array(
   [
[1408.1, 1421.3, 1429.8, 1436.4, 1447.5, 1456.8, 1469.8, 1483.6, 1495.7, 1491.4, 1491.6, 1495.1, 1501.2, 1503.8, 1514.3, 1517.5, 1515.1, 1511.4, 1509.7, 1503.2, 1505.6, 1513.6, 1517.3, 1517.3, 1516.9, 1513.9, 1507.8, 1503.9, 1506.5, 1515.1, 1518.6, 1514.1, 1492.4, 1477.6, 1461.4, 1442.3, 1442.6, 1458.8, 1465.1, 1476.8, 1504.0, 1513.1, 1510.6, 1515.4, 1516.2, 1501.7, 1491.7, 1488.0, 1472.3, 1429.9, 1418.3, 1401.0, 1384.3, 1369.5, 1343.6, 1312.9, 1294.8, 1292.6, 1296.6, 1306.5, 1330.9, 1353.3, 1371.1, 1384.6, 1395.0, 1401.9, 1410.5, 1415.3, 1415.2, 1413.8, 1416.8, 1420.6, 1427.3, 1438.5, 1458.9, 1469.5, 1470.7, 1470.3, 1466.6, 1448.7, 1422.2] ,
[1394.9, 1408.1, 1421.3, 1429.8, 1436.4, 1447.5, 1456.8, 1469.8, 1483.6, 1495.7, 1491.4, 1491.6, 1495.1, 1501.2, 1503.8, 1514.3, 1517.5, 1515.1, 1511.4, 1509.7, 1503.2, 1505.6, 1513.6, 1517.3, 1517.3, 1516.9, 1513.9, 1507.8, 1503.9, 1506.5, 1515.1, 1518.6, 1514.1, 1492.4, 1477.6, 1461.4, 1442.3, 1442.6, 1458.8, 1465.1, 1476.8, 1504.0, 1513.1, 1510.6, 1515.4, 1516.2, 1501.7, 1491.7, 1488.0, 1472.3, 1429.9, 1418.3, 1401.0, 1384.3, 1369.5, 1343.6, 1312.9, 1294.8, 1292.6, 1296.6, 1306.5, 1330.9, 1353.3, 1371.1, 1384.6, 1395.0, 1401.9, 1410.5, 1415.3, 1415.2, 1413.8, 1416.8, 1420.6, 1427.3, 1438.5, 1458.9, 1469.5, 1470.7, 1470.3, 1466.6, 1448.7] ,
[1381.0, 1394.9, 1408.1, 1421.3, 1429.8, 1436.4, 1447.5, 1456.8, 1469.8, 1483.6, 1495.7, 1491.4, 1491.6, 1495.1, 1501.2, 1503.8, 1514.3, 1517.5, 1515.1, 1511.4, 1509.7, 1503.2, 1505.6, 1513.6, 1517.3, 1517.3, 1516.9, 1513.9, 1507.8, 1503.9, 1506.5, 1515.1, 1518.6, 1514.1, 1492.4, 1477.6, 1461.4, 1442.3, 1442.6, 1458.8, 1465.1, 1476.8, 1504.0, 1513.1, 1510.6, 1515.4, 1516.2, 1501.7, 1491.7, 1488.0, 1472.3, 1429.9, 1418.3, 1401.0, 1384.3, 1369.5, 1343.6, 1312.9, 1294.8, 1292.6, 1296.6, 1306.5, 1330.9, 1353.3, 1371.1, 1384.6, 1395.0, 1401.9, 1410.5, 1415.3, 1415.2, 1413.8, 1416.8, 1420.6, 1427.3, 1438.5, 1458.9, 1469.5, 1470.7, 1470.3, 1466.6] 
   ],
   dtype=float)
#    [[6.4, 3.2, 4.5, 1.5], [5.8, 3.1, 5.0, 1.7]], dtype=float)
y = list(classifier.predict(new_samples, as_iterable=True))
print('Predictions: {}'.format(str(y)))

