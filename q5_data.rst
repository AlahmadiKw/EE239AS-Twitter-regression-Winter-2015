===================
Question 5
===================

::

  python was used for data parsing and R Statistical language was used for data
  and regression analysis

To make predictions for the test data, we use the regression model that
corresponds to the correct time frame. We choose the regression model for the
specific hashtag that is most accurate in each period.

Since no information about which hashtag each test data is based on. based on our examination of the data, we made an assumption that the test data contains any hashtag related to the super bowl. Hence, we used the regression model that had the least total error and used it for the testing data.

The following R method was used to test the data: ::

	results = predict(fit3, dat, TRUE, interval = "prediction")

Results are shown below. For brevity, we only display the Standard Error for each
test data.


+------------------+---------+
|       file       |   SE    |
+==================+=========+
| sample1_period1  | 60.0256 |
+------------------+---------+
| sample2_period2  | 43.6    |
+------------------+---------+
| sample3_period3  | 65.82   |
+------------------+---------+
| sample4_period1  | 44.1750 |
+------------------+---------+
| sample5_period1  | 48.92   |
+------------------+---------+
| sample6_period2  | 44      |
+------------------+---------+
| sample7_period3  | 14.66   |
+------------------+---------+
| sample8_period1  | 15.95   |
+------------------+---------+
| sample9_period2  | 53.9    |
+------------------+---------+
| sample10_period3 | 14.68   |
+------------------+---------+
