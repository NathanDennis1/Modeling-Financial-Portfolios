Points (Monday):

1. Missing Values:
   - Describe how many `NULL` in `INFOTABLE` and comment whether they are important or not like FIGI is not important
   - Similarly comment on the other missing variables.

2. Data Imbalance:
   - In `INFOTABLE`, `SSHPRNAMT` - We can plot a bar graph between these two variables and comment on it.
   - `PUT/CALL` - Graph is plotted, comment why NA is there and why we are not imputing/filling it up.
   - In `COVERPAGE`, `AMENDMENTYPE` - We can plot a bar graph between these two variables and comment on it.
  
3. Data scaling:
   - Divide it into 2 subtopics: Using Time series vs Not using Time Series
   - When using Time series Cross validation, we cannot use global scaling because then future data will impact past data causing optimistic results and biasness - so we need to implement standardization separately in each fold.
   - When not using Time series cross validation, we can use standardization
     
4. Additional Preprocessing:
   - Before January 2023, data is the `VALUE` column of `INFOTABLE` is reported is thousands of USD. After that, `VALUE` is reported rounded to the nearest USD. If we look at previous quarters, we must preprocess the data accordingly.
   - Mention how we can leverage database (like sql) to effectively handle large computational needs.

For the 'VALUE' column, we noted that there are many observations with 0's indicating 0 market value. We plan to investigate if these values hold any meaninful insights before we proceed. These observations could harm analysis, as these 0 values could distrupt continuity of time series analysis. However, these observations could provide some context as to the market value of certain stocks for companies and help identify trends for buying and selling behaviors.

We also note that there are several outliers for market value. Some observations have market values over 100 billion, major outliers compared to some of the rest of the companies. These are highly successful companies, such as Microsoft, Nvidia, Amazon, and Apple. We plan to use standardization to scale this variable to mitigate the influence of these larger companies and see how they compare with the rest of our data. This standardization process involves subtracting by the mean and dividing by the standard deviation, putting this variable on the same scale.

There is major data imbalance within some of the categorical variables in our dataset, some classes have far fewer samples than others. To mitigate this issue, we plan to experiment with different strategies, one which is stratified cross-validation to ensure each fold contains the same proportion of a class label across the dataset. This can mitigate the issue of data inbalance favoring the majority class.

(This is what I had for the data imbalance before the meeting, may not be as useful)

To mitigate this imbalance, we plan to test different strategies including resampling or utilizing different algorithms. We plan to experiement using resampling by oversampling the minority class to balance the distribution when conducting analysis.

