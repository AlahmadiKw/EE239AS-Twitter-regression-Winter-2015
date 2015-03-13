===================
Problem Formulation
===================

Question 2
**********

::

  python was used for data parsing and R Statistical language was used for data and regression analysis

1. Problem Formulation
----------------------

* Predicting the number of tweets in the next hour based on
  previous hours data. (the letters between brackerts will be used as shorthands)

  - **Output**:

    * [n_twt] Expected number of tweets

  - **Input**:

    * [hr] Desired hour of expectation
    * [n_rt]Total number of retweets at that hour
    * [n_flr] Total number of follows of all users who used the hashtag
    * [m_flr] n_ The sum of the maximum number of followers that occured within that
      hour

2. Data Collection
------------------

* The python ``get_stats`` in ``project3.py`` method parses the data such
  that it sums up the tweets data for every hour as follows:

  - Total number of tweets
  - Total number of retweets
  - Total number of followers for all tweets withing an hour
  - Maximum number of tweets within an hour
  - The hour in which the above data were collected at

3. Initial Data Analysis
------------------------

* Before forming our regression model, we first did some exploration
  of the data in order to find the best way to prepare the data for
  the model.
* After some data exploration, we saw that the best data formulation
  for the regression model is as follows:

  - Since we want to predict the number of tweets in a specific hour
    of the day regardelss of the date, we first sort the data
    chronologically in hour bins regardless of the date as shown below.
  - For each time bin, we average all data such that for each hour bin
    (24 bins), we have averages of the total number of tweets, total
    number of retweets, total number of followers, and total maximums
    of followers that occured within that hour.

4. Data Exploration
-------------------

* This step aims to identify outliers and irregularities in the data.
* We first plot the number of tweets across each of the four input
  variables in `1. Problem Formulation`_ as shown below:

|img5| |img6|

|img7| |img8|

.. |img5| image:: img/twt_cnt_max_hour_outlier.png
   :height: 300
.. |img6| image:: img/twt_cnt_ret_cnt_outlier.png
   :height: 300
.. |img7| image:: img/twt_cnt_num_flwrs_outlier.png
   :height: 300
.. |img8| image:: img/twt_cnt_max_flwrs_outlier.png
   :height: 300

* From the figure above, it is clear that the exists one significant
  outlier that does not mesh well with the rest of the data. Therefore,
  we eliminitate this particular data. replotting the data we get a
  better sparsed plots as shown below

|img1| |img2|

|img3| |img4|

.. |img1| image:: img/twt_cnt_over_hours.png
   :height: 300
.. |img2| image:: img/twt_cnt_over_ret_count.png
   :height: 300
.. |img3| image:: img/twt_cnt_over_flwr_cnt.png
   :height: 300
.. |img4| image:: img/twt_cnt_over_max_flwrs.png
   :height: 300

4. Regression Model
-------------------

* We implement a simple linear regression model with one dependant (the output)
  and four independant variables (the inputs). Our regression model is as follows:

.. math::

  [n_twt] = beta*[hr] + beta'*[n_rt] + beta''*[n_flr] + beta'''*[m_flr]

* where beta, beta', beta'', and beta''' are the regression coefficients


5. Analyzing the Regression Model
---------------------------------

* First, we assume that there is a significant relationship between the inputs
  and the output. The t-values and p-values should give us clues on wether our
  assumptoins are valid or not. analysing and interpreting the t-value and p-value
  are as folows:

  * The p-value for each feature tests the null hypothesis that the regression
    coefficient is equal to zero (i.e has no effect) [1]_. Hence, a low p-value (< 0.05)
    indicates that there is indeed a significant relationship between the input and the output.

  * The t statistic is the coefficient divided by the by the stantard error.
    It can be thought of as a measure of the precision with which the regression
    coefficient is measured [2]_. Hence, the larger the t-value the more significant
    our feature is.

* Using the ``summary(fit)`` function in R (fit is the regression model name),
  we get:

::

  lm(formula = twt_count ~ hours + flwr_cnt + ret_cnt + max_flwrs,
    data = dat)

  Residuals:
       Min       1Q   Median       3Q      Max
  -157.260   -8.063    8.602   22.963   73.506

  Coefficients:
                Estimate Std. Error t value Pr(>|t|)
  (Intercept)  7.819e+01  2.727e+01   2.868  0.00985 **
  hours        6.627e-01  1.476e+00   0.449  0.65858
  flwr_cnt     5.460e-05  2.607e-05   2.095  0.04985 *
  ret_cnt      5.061e-01  4.604e-02  10.994 1.12e-09 ***
  max_flwrs   -5.815e-05  5.118e-05  -1.136  0.26995
  ---
  Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

  Residual standard error: 47.42 on 19 degrees of freedom
  Multiple R-squared:  0.996, Adjusted R-squared:  0.9952
  F-statistic:  1188 on 4 and 19 DF,  p-value: < 2.2e-16

* **hours**:
  The t value is considered very small and the p value is very large (>> .05).
  It is clear that a 1st order regression line is not a good fit and hence


.. [1] `How to Interpret Regression Analysis Results: P-values and Coefficients`_
.. [2] `Interpreting Regression Output`_

.. _`How to Interpret Regression Analysis Results: P-values and Coefficients`: http://blog.minitab.com/blog/adventures-in-statistics/how-to-interpret-regression-analysis-results-p-values-and-coefficients

.. _`Interpreting Regression Output`: http://dss.princeton.edu/online_help/analysis/interpreting_regression.htm#ptse



.. +------------------+--------------------+---------------------+-----------------------------+------+
.. | number of tweets | number of retweets | number of followers | maximum number of followers | hour |
.. +==================+====================+=====================+=============================+======+
.. | 432              | 23                 | 234089dddddddddddddd| 11100234                    | 1    |
.. |  sf              | dd                 | dd                  | dd                          | dd   |
.. | 432              | 23                 | 234089              | 11100234                    | 1    |
.. +------------------+--------------------+---------------------+-----------------------------+------+
.. | 432              | 23                 | 234089              | 11100234                    | 1    |
.. +------------------+--------------------+---------------------+-----------------------------+------+
.. | 8                | 5                  | 2323                | 7677                        | 2    |
.. +------------------+--------------------+---------------------+-----------------------------+------+
.. | 67               | 8                  | 236                 | 454                         | 2    |
.. +------------------+--------------------+---------------------+-----------------------------+------+
.. | 9                | 7                  | 97                  | 676                         | 2    |
.. +------------------+--------------------+---------------------+-----------------------------+------+
.. | ...              | ...                | ...                 | ...                         | ...  |
.. +------------------+--------------------+---------------------+-----------------------------+------+
.. | 76               | 234                | 12                  | 11100234                    | 23   |
.. +------------------+--------------------+---------------------+-----------------------------+------+
.. | 566              | 76                 | 123                 | 12312                       | 23   |
.. +------------------+--------------------+---------------------+-----------------------------+------+
.. | 56               | 5                  | 12312               | 346345                      | 23   |
.. +------------------+--------------------+---------------------+-----------------------------+------+



