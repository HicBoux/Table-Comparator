<h1>Table Comparator : a Flask app to compare two CSV of data in terms of statistics </h1>

Through this simple app, it becomes simpler to compare two tables of data (saved as .csv) in terms of meta statistics, 
descriptive statistics and distributions. Thus the app returns :<br/>
 -Number of rows, columns, duplicates, and NaN for each CSV file.<br/>
 -Name of the columns in the header and its datatypes for each CSV file.<br/>
 -Based on column names, a summary and comparison of them (in case of match) through basic indicators
like the mean, median, quantiles, maximum, minimum, standard deviation...<br/>
 -Double line graphs with D3.js visualisations to compare 2 columns with the same name.<br/>
 -Single line graphs with D3.js visualisations when a column is only in one csv.<br/>

<h2>Requirements</h2>
Python 3 <br/>
Python following libraries : Pandas, Numpy, Flask <br/>
An internet connection in order to load the D3.js library<br/>
(It can possibly on older versions, but not tested yet.)

<h2>How to set it :</h2>

1) Install your Python environment with all the necessary packages. Be sure Flask is well configured.
2) Download from this Github repository the folder of the app named "Table_Comparator".
3) Start a terminal/shell window and move to current directory of the app : ```cd /path_to_the_app/Table_comparator/```
4) Start the app by executing the Python script "csv_uploader.py" : ``python csv_uploader.py```
5) Open your web browser to your Flask configured URL or by default at "localhost:5000". The app would appear with a title in blue !
6) Below the section "Upload the two CSV to compare :", click on the "Choose file" left button and upload your first CSV.
Then click on the right one and upload your second CSV file. Once done, let's launch the algorithm by clicking on "Compare" !
7) Depending on the size of your data, it will take more or less time to display the calculated summaries. Graphs can take
longer to be drawn, but you will be able to first read the summaries during the load of the graphs.
8) Enjoy !


<h2>References</h2>

-[D3.js framework](https://d3js.org/) <br/>
-[Plunker Online D3.js simulator](http://embed.plnkr.co/) <br/>
-[D3.js examples](https://bl.ocks.org/) <br/>
-[Flask tutorial](http://sdz.tdct.org/sdz/creez-vos-applications-web-avec-flask.html) (in french) <br/>

<h2>Credits</h2>

Copyright (c) 2019, HicBoux. Work released under MIT License. 

(Please contact me if you wish to use my work in specific conditions not allowed automatically by the MIT License.)

