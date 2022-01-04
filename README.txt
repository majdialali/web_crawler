ACIT4420 - “Problem-solving with scripting” – Fall Semester 2021 
 
Final project submission and evaluation 
 
For  their  final  assessment  of  ACIT4420,  students  must  develop  a  project  and  submit  both  the  code  
base and a project report  on December 17th 2021 before 12.00 (noon), via Inspera. The submission 
must be anonymous and contain the candidate number as the only identifying information (no name 
or student number should be included). The project report must be submitted as a single pdf file. The 
code base should be submitted as a single zip file. All files necessary to run and test the project should 
be included in that zip file.   
Students  must  work  on  their  projects  individually.  They  must  choose  one  of  the  project  options  
presented in this document. The code for the project must be written in Python. Each project option 
contains a number of minimum features which must be implemented, but the students are expected 
to go beyond these minimum features and extend the project with their own ideas. 
The project report must be written in English and must be between 6000 and 12000 words long (not 
counting the code base, which is not part of the report). The report counts for 100% of the grade in 
this course. The report should contain: an introduction, an overview of available solutions, a simplified 
description of the design chosen by the student, detailed explanations of the implementation, analysis 
and testing of the project with examples, a final evaluation. The report will be graded according to: 
general  impression  (10%),  overview  and  alternatives  (10%),  design  (10%),  implementation  details  
(40%), testing and examples (10%), analysis (10%), format (10%).  


Project Option 1 - Website Crawler 
Create a Python project that is able to download websites and capture sensitive data from them. The 
program should accept the following inputs from the user: 
• The initial URL to start the crawling. 
• The depth of the crawling (how many links to subpages and to subpages of those to 
take into account). 
• User-defined regular expressions for sensitive data. 
Minimum features: 
• Download  the  website  from  the  provided  URL,  identify  links  inside  the  source  code  
and download all subpages linked there. Repeat until the crawling depth is reached. 
• Identify email addresses and phone numbers and create a list of the captured values. 
• Identify comments inside the source code and make a list of them, indicating the file 
names and line numbers where they appear. 
• Identify  special  data  using  the  regular  expressions  provided  by  the  user  and  create  
lists with them.  
• Create a list of the most common words used on the crawled websites. 