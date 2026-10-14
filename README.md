# Programming with Python — Assignment 2

Individual Python solutions for all ten questions in the B.Tech IT Semester V assignment.

## Requirements
- Python 3.10+
- Q1, Q2, Q4, Q6, Q7, Q8, Q9: standard library
- Q3 and Q5: `pip install mysql-connector-python`
- Q10: `pip install matplotlib`

## Files and run instructions
- Q1 Email extractor: `python Q1_Email_Intelligence_Extractor.py emails.txt`
- Q2 HTML ranker: `python Q2_HTML_Product_Ranker.py < input.txt` (input contains `p k` and HTML paths)
- Q3 MySQL analytics: `python Q3_MySQL_Student_Course_Analytics.py`
- Q4 SQL builder: `python Q4_SQL_Join_Query_Builder.py < query.json`
- Q5 Contact GUI: `python Q5_Tkinter_MySQL_Contact_Manager.py`
- Q6 Log anomaly detector: `python Q6_Log_Anomaly_Detector.py < logs.txt`
- Q7 JSONL ETL: `python Q7_Generator_JSON_ETL.py readings.jsonl`
- Q8 Matrix path optimizer: `python Q8_Matrix_Path_Optimizer.py < matrix.txt`
- Q9 Inventory merger: `python Q9_OOP_Inventory_Merger.py inventoryA.json inventoryB.json [merged.json]`
- Q10 Visualization dashboard: `python Q10_Data_Visualization_Dashboard.py marks.csv output_folder`

## Important setup notes
- Q3 requires an existing MySQL database and CSV headers as documented in the source.
- Q4 builds safe parameterized SQL but does not connect to a database or execute the query.
- Q5 requires a MySQL database to be created first, then run the program using credentials for that database.
- Q9 uses JSON inventory files; see its usage message for the expected schema.
- Q10 saves cleaned data, summary data, and three chart images in the selected output folder.

Review each program, run the assignment samples, and add at least three additional test cases before submitting.
