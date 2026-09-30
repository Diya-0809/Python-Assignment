# Assignment 1 Solutions — Programming with Python (202044504)

Python version: 3.10+

Files:
Q1_Campus_Merit_Analyzer.py
Q2_Optimized_Password_Audit.py
Q3_Recursive_Expression_Engine.py
Q4_Exception_Safe_CSV_Transaction_Splitter.py
Q5_OOP_Bank_Settlement_System.py
Q6_Python_Module_Dependency_Resolver.py
Q7_Interactive_Formula_Validator.py
Q8_Compressed_Log_Index.py
Q9_Threaded_Job_Scheduler.py
Q10_Tkinter_Assignment_Tracker.py

Run a console question with:
    python Q1_Campus_Merit_Analyzer.py

Q4:
Enter the input CSV path when prompted. credit.csv, debit.csv and error.csv
are created in the current working directory.

Q8 BUILD:
The program asks for:
    folder_path zip_name
It creates a pickle index temporarily and stores it with the source logs
inside the requested ZIP archive.

Q8 SEARCH:
The program asks for:
    pickle_path q token1 token2 ...

Q10:
Run the Tkinter file directly. Data is persisted in assignment_tracker.json.
The GUI supports adding students/submissions, updating marks, filtering and CSV export.

Q9 assumption:
The assignment specifies a per-job resource count but gives no worker resource
capacity. The solution therefore models each worker as one-job-at-a-time and
does not use resource count as a scheduling capacity constraint. This assumption
should be changed if your faculty has specified a different resource model.

Testing:
Use the sample inputs from the assignment plus boundary, invalid-input and
additional self-created tests as required by the assignment instructions.
