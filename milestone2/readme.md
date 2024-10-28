Points (Monday):

1. Missing Values:
   - Describe how many NULL in INFOTABLE and comment whether they are important or not like FIGI is not important
   - Similarly comment on the other missing variables.

2. Data Imbalance:
   - In INFOTABLE, SSHPRNAMT - We can plot a bar graph between these two variables and comment on it.
   - PUT/CALL - Graph is plotted, comment why NA is there and why we are not imputing/filling it up.
   - In COVERPAGE, AMENDMENTYPE - We can plot a bar graph between these two variables and comment on it.
  
3. Data scaling:
   - Divide it into 2 subtopics: Using Time series vs Not using Time Series
   - When using Time series Cross validation, we cannot use global scaling because then future data will impact past data causing optimistic results and biasness
   - When not using Time series cross validation, we can use standardization
