"""
Sample Dataset for Library Management Data Warehouse & Data Mining System
Contains realistic operational records for:
- Readers (Demographics, Departments, Memberships)
- Books (Academic & General with Rich Descriptions for Text Mining)
- Borrowing Transactions (Multi-month history, Co-borrowing patterns for Apriori)
"""

SAMPLE_READERS = [
    {"reader_id": "R101", "name": "Aarav Sharma", "age": 21, "gender": "Male", "department": "Computer Science", "membership_type": "Student", "registration_date": "2025-01-10"},
    {"reader_id": "R102", "name": "Diya Patel", "age": 22, "gender": "Female", "department": "Computer Science", "membership_type": "Student", "registration_date": "2025-01-12"},
    {"reader_id": "R103", "name": "Dr. Rajesh Verma", "age": 45, "gender": "Male", "department": "Computer Science", "membership_type": "Faculty", "registration_date": "2024-08-15"},
    {"reader_id": "R104", "name": "Sneha Kulkarni", "age": 24, "gender": "Female", "department": "Data Science", "membership_type": "Researcher", "registration_date": "2024-09-01"},
    {"reader_id": "R105", "name": "Rohan Gupta", "age": 20, "gender": "Male", "department": "Information Technology", "membership_type": "Student", "registration_date": "2025-01-15"},
    {"reader_id": "R106", "name": "Priya Nair", "age": 21, "gender": "Female", "department": "Data Science", "membership_type": "Student", "registration_date": "2025-01-18"},
    {"reader_id": "R107", "name": "Dr. Ananya Sen", "age": 39, "gender": "Female", "department": "Data Science", "membership_type": "Faculty", "registration_date": "2024-07-20"},
    {"reader_id": "R108", "name": "Vikram Singh", "age": 23, "gender": "Male", "department": "Electrical Engineering", "membership_type": "Student", "registration_date": "2025-01-20"},
    {"reader_id": "R109", "name": "Neha Joshi", "age": 22, "gender": "Female", "department": "Information Technology", "membership_type": "Student", "registration_date": "2025-01-22"},
    {"reader_id": "R110", "name": "Amitabh Roy", "age": 28, "gender": "Male", "department": "Business Administration", "membership_type": "Researcher", "registration_date": "2024-11-05"},
    {"reader_id": "R111", "name": "Kavita Reddy", "age": 21, "gender": "Female", "department": "Business Administration", "membership_type": "Student", "registration_date": "2025-01-25"},
    {"reader_id": "R112", "name": "Siddharth Rao", "age": 23, "gender": "Male", "department": "Mechanical Engineering", "membership_type": "Student", "registration_date": "2025-02-01"},
    {"reader_id": "R113", "name": "Dr. Suresh Menon", "age": 52, "gender": "Male", "department": "Mechanical Engineering", "membership_type": "Faculty", "registration_date": "2024-06-10"},
    {"reader_id": "R114", "name": "Pooja Hegde", "age": 20, "gender": "Female", "department": "Literature & Arts", "membership_type": "Student", "registration_date": "2025-02-05"},
    {"reader_id": "R115", "name": "Manish Choudhary", "age": 25, "gender": "Male", "department": "Literature & Arts", "membership_type": "Researcher", "registration_date": "2024-10-12"},
    {"reader_id": "R116", "name": "Shweta Deshmukh", "age": 22, "gender": "Female", "department": "Computer Science", "membership_type": "Student", "registration_date": "2025-02-10"},
    {"reader_id": "R117", "name": "Gaurav Malhotra", "age": 21, "gender": "Male", "department": "Information Technology", "membership_type": "Student", "registration_date": "2025-02-12"},
    {"reader_id": "R118", "name": "Tanvi Bhat", "age": 22, "gender": "Female", "department": "Data Science", "membership_type": "Student", "registration_date": "2025-02-15"},
    {"reader_id": "R119", "name": "Prof. Meera Iyer", "age": 48, "gender": "Female", "department": "Business Administration", "membership_type": "Faculty", "registration_date": "2024-05-18"},
    {"reader_id": "R120", "name": "Aditya Kapoor", "age": 23, "gender": "Male", "department": "Computer Science", "membership_type": "Student", "registration_date": "2025-02-20"},
    {"reader_id": "R121", "name": "Isha Saxena", "age": 21, "gender": "Female", "department": "Electrical Engineering", "membership_type": "Student", "registration_date": "2025-02-22"},
    {"reader_id": "R122", "name": "Karan Singhal", "age": 26, "gender": "Male", "department": "Computer Science", "membership_type": "Researcher", "registration_date": "2024-12-01"},
    {"reader_id": "R123", "name": "Ananya Mishra", "age": 20, "gender": "Female", "department": "Data Science", "membership_type": "Student", "registration_date": "2025-02-25"},
    {"reader_id": "R124", "name": "Dr. Vivek Chawla", "age": 43, "gender": "Male", "department": "Information Technology", "membership_type": "Faculty", "registration_date": "2024-07-15"},
    {"reader_id": "R125", "name": "Ritu Agarwal", "age": 22, "gender": "Female", "department": "Business Administration", "membership_type": "Student", "registration_date": "2025-03-01"},
    {"reader_id": "R126", "name": "Deepak Kumar", "age": 24, "gender": "Male", "department": "Mechanical Engineering", "membership_type": "Student", "registration_date": "2025-03-02"},
    {"reader_id": "R127", "name": "Harshita Jain", "age": 21, "gender": "Female", "department": "Computer Science", "membership_type": "Student", "registration_date": "2025-03-03"},
    {"reader_id": "R128", "name": "Nikhil Aggarwal", "age": 27, "gender": "Male", "department": "Data Science", "membership_type": "Researcher", "registration_date": "2024-11-20"},
    {"reader_id": "R129", "name": "Megha Pandey", "age": 23, "gender": "Female", "department": "Electrical Engineering", "membership_type": "Student", "registration_date": "2025-03-05"},
    {"reader_id": "R130", "name": "Varun Sethi", "age": 22, "gender": "Male", "department": "Information Technology", "membership_type": "Student", "registration_date": "2025-03-08"},
    {"reader_id": "R131", "name": "Anjali Tripathi", "age": 21, "gender": "Female", "department": "Literature & Arts", "membership_type": "Student", "registration_date": "2025-03-10"},
    {"reader_id": "R132", "name": "Dr. Harish Nambiar", "age": 50, "gender": "Male", "department": "Electrical Engineering", "membership_type": "Faculty", "registration_date": "2024-04-12"},
    {"reader_id": "R133", "name": "Simran Kaur", "age": 22, "gender": "Female", "department": "Business Administration", "membership_type": "Student", "registration_date": "2025-03-12"},
    {"reader_id": "R134", "name": "Abhinav Tiwari", "age": 24, "gender": "Male", "department": "Computer Science", "membership_type": "Student", "registration_date": "2025-03-15"},
    {"reader_id": "R135", "name": "Payal Dutta", "age": 25, "gender": "Female", "department": "Data Science", "membership_type": "Researcher", "registration_date": "2024-10-30"},
    {"reader_id": "R136", "name": "Kunal Ghosh", "age": 21, "gender": "Male", "department": "Mechanical Engineering", "membership_type": "Student", "registration_date": "2025-03-18"},
    {"reader_id": "R137", "name": "Tarun Bansal", "age": 23, "gender": "Male", "department": "Information Technology", "membership_type": "Student", "registration_date": "2025-03-20"},
    {"reader_id": "R138", "name": "Pallavi Shinde", "age": 22, "gender": "Female", "department": "Computer Science", "membership_type": "Student", "registration_date": "2025-03-22"},
    {"reader_id": "R139", "name": "Dr. Sanjay Bhattacharya", "age": 47, "gender": "Male", "department": "Literature & Arts", "membership_type": "Faculty", "registration_date": "2024-06-25"},
    {"reader_id": "R140", "name": "Bhavya Sharma", "age": 20, "gender": "Female", "department": "Data Science", "membership_type": "Student", "registration_date": "2025-03-25"},
    {"reader_id": "R141", "name": "Raghav Mathur", "age": 22, "gender": "Male", "department": "Business Administration", "membership_type": "Student", "registration_date": "2025-03-28"},
    {"reader_id": "R142", "name": "Alok Ranjan", "age": 29, "gender": "Male", "department": "Computer Science", "membership_type": "Researcher", "registration_date": "2024-09-15"},
    {"reader_id": "R143", "name": "Kritika Soni", "age": 21, "gender": "Female", "department": "Electrical Engineering", "membership_type": "Student", "registration_date": "2025-04-01"},
    {"reader_id": "R144", "name": "Kartik Varma", "age": 23, "gender": "Male", "department": "Information Technology", "membership_type": "Student", "registration_date": "2025-04-03"},
    {"reader_id": "R145", "name": "Shilpa Murthy", "age": 22, "gender": "Female", "department": "Literature & Arts", "membership_type": "Student", "registration_date": "2025-04-05"},
    {"reader_id": "R146", "name": "Prateek Saxena", "age": 21, "gender": "Male", "department": "Mechanical Engineering", "membership_type": "Student", "registration_date": "2025-04-08"},
    {"reader_id": "R147", "name": "Nandini Das", "age": 26, "gender": "Female", "department": "Business Administration", "membership_type": "Researcher", "registration_date": "2024-11-15"},
    {"reader_id": "R148", "name": "Ashwin Pillai", "age": 22, "gender": "Male", "department": "Data Science", "membership_type": "Student", "registration_date": "2025-04-10"},
    {"reader_id": "R149", "name": "Divya Swaminathan", "age": 23, "gender": "Female", "department": "Computer Science", "membership_type": "Student", "registration_date": "2025-04-12"},
    {"reader_id": "R150", "name": "Yashwant Patil", "age": 24, "gender": "Male", "department": "Information Technology", "membership_type": "Student", "registration_date": "2025-04-15"}
]

SAMPLE_BOOKS = [
    {
        "book_id": "B001",
        "title": "Python Programming and Data Science Foundations",
        "author": "Mark Lutz",
        "category": "Data Science",
        "publisher": "O'Reilly Media",
        "publication_year": 2022,
        "language": "English",
        "description": "Comprehensive guide covering Python programming language basics, data structures, object-oriented design, NumPy arrays, pandas DataFrames, and essential data manipulation techniques for data science practitioners."
    },
    {
        "book_id": "B002",
        "title": "Data Mining: Concepts and Techniques",
        "author": "Jiawei Han & Micheline Kamber",
        "category": "Data Science",
        "publisher": "Morgan Kaufmann",
        "publication_year": 2021,
        "language": "English",
        "description": "Fundamental textbook exploring data warehousing, OLAP cubes, data preprocessing, frequent itemset mining using Apriori and FP-Growth, classification models like Decision Trees, and cluster analysis algorithms."
    },
    {
        "book_id": "B003",
        "title": "Machine Learning with Scikit-Learn and PyTorch",
        "author": "Sebastian Raschka",
        "category": "Artificial Intelligence",
        "publisher": "Packt Publishing",
        "publication_year": 2023,
        "language": "English",
        "description": "Practical machine learning handbook detailing supervised learning, unsupervised clustering, neural networks, hyperparameter tuning, model evaluation, and predictive analytics using Python."
    },
    {
        "book_id": "B004",
        "title": "Database System Concepts and Design",
        "author": "Abraham Silberschatz & Henry Korth",
        "category": "Database Systems",
        "publisher": "McGraw-Hill",
        "publication_year": 2020,
        "language": "English",
        "description": "Core principles of relational databases, relational algebra, SQL querying, transaction management, ACID properties, indexing, concurrency control, and database normalization."
    },
    {
        "book_id": "B005",
        "title": "Mastering SQL and Relational Database Analytics",
        "author": "Alan Beaulieu",
        "category": "Database Systems",
        "publisher": "O'Reilly Media",
        "publication_year": 2022,
        "language": "English",
        "description": "In-depth guide to writing fast SQL queries, joins, subqueries, analytical window functions, data aggregation, database optimization, and schema design for business intelligence."
    },
    {
        "book_id": "B006",
        "title": "Data Warehouse Lifecycle Toolkit",
        "author": "Ralph Kimball & Margy Ross",
        "category": "Data Science",
        "publisher": "Wiley",
        "publication_year": 2020,
        "language": "English",
        "description": "The definitive methodology for designing dimensional data warehouses, star schemas, snowflake schemas, ETL pipeline architectures, fact tables, slowly changing dimensions, and business reporting."
    },
    {
        "book_id": "B007",
        "title": "Natural Language Processing with Python and NLTK",
        "author": "Steven Bird & Ewan Klein",
        "category": "Artificial Intelligence",
        "publisher": "O'Reilly Media",
        "publication_year": 2021,
        "language": "English",
        "description": "Hands-on text mining and computational linguistics tutorial covering tokenization, part-of-speech tagging, stop word removal, TF-IDF scoring, sentiment classification, and corpus analysis."
    },
    {
        "book_id": "B008",
        "title": "Artificial Intelligence: A Modern Approach",
        "author": "Stuart Russell & Peter Norvig",
        "category": "Artificial Intelligence",
        "publisher": "Pearson",
        "publication_year": 2022,
        "language": "English",
        "description": "Authoritative AI textbook presenting informed search algorithms, constraint satisfaction, probabilistic reasoning, knowledge representation, decision theory, and reinforcement learning."
    },
    {
        "book_id": "B009",
        "title": "Flask Web Development: Developing Web Applications with Python",
        "author": "Miguel Grinberg",
        "category": "Web Development",
        "publisher": "O'Reilly Media",
        "publication_year": 2022,
        "language": "English",
        "description": "Step-by-step guide to building scalable dynamic web applications with Flask, Jinja templates, routing, user authentication, RESTful APIs, database integration, and deployment."
    },
    {
        "book_id": "B010",
        "title": "Full Stack Web Development with HTML, CSS and JavaScript",
        "author": "Jon Duckett",
        "category": "Web Development",
        "publisher": "Wiley",
        "publication_year": 2021,
        "language": "English",
        "description": "Visual introduction to frontend programming, modern responsive UI design with Bootstrap, CSS grid layouts, JavaScript DOM manipulation, event handling, and interactive dashboards."
    },
    {
        "book_id": "B011",
        "title": "Cloud Computing Concepts, Technology and Architecture",
        "author": "Thomas Erl",
        "category": "Cloud Computing",
        "publisher": "Prentice Hall",
        "publication_year": 2021,
        "language": "English",
        "description": "Architectural breakdown of cloud services, virtualization, microservices, containerization, distributed storage, multi-tenancy, and cloud infrastructure scalability."
    },
    {
        "book_id": "B012",
        "title": "Cyber Security Fundamentals and Network Defense",
        "author": "William Stallings",
        "category": "Cyber Security",
        "publisher": "Pearson",
        "publication_year": 2023,
        "language": "English",
        "description": "Covers network defense strategies, encryption algorithms, hashing, firewalls, authentication protocols, penetration testing, vulnerability assessment, and risk management."
    },
    {
        "book_id": "B013",
        "title": "Strategic Business Analytics and Data-Driven Decision Making",
        "author": "Thomas Davenport",
        "category": "Business & Management",
        "publisher": "Harvard Business Press",
        "publication_year": 2022,
        "language": "English",
        "description": "How modern enterprises leverage big data analytics, KPI metrics, predictive modeling, data visualization, customer segmentation, and executive dashboards for market advantage."
    },
    {
        "book_id": "B014",
        "title": "Principles of Management and Organizational Behavior",
        "author": "Stephen Robbins",
        "category": "Business & Management",
        "publisher": "Pearson",
        "publication_year": 2020,
        "language": "English",
        "description": "Comprehensive textbook on organizational leadership, workplace motivation, team dynamics, strategic planning, human resource management, and corporate ethics."
    },
    {
        "book_id": "B015",
        "title": "Classic World Literature and Literary Analysis",
        "author": "Harold Bloom",
        "category": "Literature & Arts",
        "publisher": "Yale University Press",
        "publication_year": 2019,
        "language": "English",
        "description": "Scholarly exploration of canonical world literature, literary criticism, narrative structures, thematic motifs, symbolism, poetry analysis, and comparative storytelling."
    },
    {
        "book_id": "B016",
        "title": "Applied Statistics and Probability for Engineers",
        "author": "Douglas Montgomery",
        "category": "Mathematics & Statistics",
        "publisher": "Wiley",
        "publication_year": 2022,
        "language": "English",
        "description": "Mathematical foundations of probability distributions, hypothesis testing, linear regression, ANOVA, confidence intervals, experimental design, and statistical inference."
    },
    {
        "book_id": "B017",
        "title": "Advanced Data Structures and Algorithms in Python",
        "author": "Michael Goodrich & Roberto Tamassia",
        "category": "Computer Science",
        "publisher": "Wiley",
        "publication_year": 2021,
        "language": "English",
        "description": "In-depth treatment of balanced search trees, graph algorithms, dynamic programming, greedy algorithms, hashing mechanisms, asymptotic complexity, and computational optimization."
    },
    {
        "book_id": "B018",
        "title": "Deep Learning: Foundations and Architectures",
        "author": "Ian Goodfellow, Yoshua Bengio & Aaron Courville",
        "category": "Artificial Intelligence",
        "publisher": "MIT Press",
        "publication_year": 2021,
        "language": "English",
        "description": "Comprehensive reference covering convolutional networks, recurrent sequence models, backpropagation calculus, autoencoders, generative adversarial networks, and deep optimization."
    },
    {
        "book_id": "B019",
        "title": "Operating System Concepts and Architecture",
        "author": "Abraham Silberschatz & Peter Galvin",
        "category": "Computer Science",
        "publisher": "Wiley",
        "publication_year": 2020,
        "language": "English",
        "description": "Core principles of modern operating systems: process scheduling, multithreading, memory management, virtual memory paging, file systems, I/O systems, and kernel protection."
    },
    {
        "book_id": "B020",
        "title": "Computer Networks: A Systems Approach",
        "author": "Larry Peterson & Bruce Davie",
        "category": "Computer Science",
        "publisher": "Morgan Kaufmann",
        "publication_year": 2022,
        "language": "English",
        "description": "Layered networking architecture: TCP/IP protocols, packet routing algorithms, flow control, DNS infrastructure, wireless communication, congestion management, and network security."
    },
    {
        "book_id": "B021",
        "title": "Data Visualization with Python: Matplotlib and Seaborn",
        "author": "Colin Ware",
        "category": "Data Science",
        "publisher": "O'Reilly Media",
        "publication_year": 2022,
        "language": "English",
        "description": "Practical design principles for building interactive visualizations, heatmaps, scatter plots, time series dashboards, categorical distributions, and statistical graphics in Python."
    },
    {
        "book_id": "B022",
        "title": "Digital Marketing Strategy and Customer Analytics",
        "author": "Dave Chaffey",
        "category": "Business & Management",
        "publisher": "Kogan Page",
        "publication_year": 2021,
        "language": "English",
        "description": "Frameworks for search engine optimization, content marketing campaigns, social media analytics, customer conversion funnels, web traffic analysis, and brand management."
    },
    {
        "book_id": "B023",
        "title": "Modern Control Engineering and Robotics",
        "author": "Katsuhiko Ogata",
        "category": "Engineering",
        "publisher": "Pearson",
        "publication_year": 2021,
        "language": "English",
        "description": "State-space modeling, feedback control loops, PID tuning, frequency response, stability criteria, transfer functions, and electromechanical robotics applications."
    },
    {
        "book_id": "B024",
        "title": "Renewable Energy Systems and Electrical Power Grid",
        "author": "Gilbert Masters",
        "category": "Engineering",
        "publisher": "Wiley",
        "publication_year": 2022,
        "language": "English",
        "description": "Design of solar photovoltaic systems, wind turbine generation, energy storage battery technologies, smart grid integration, power electronics, and power distribution."
    },
    {
        "book_id": "B025",
        "title": "Shakespearean Drama and Renaissance Poetry",
        "author": "Stephen Greenblatt",
        "category": "Literature & Arts",
        "publisher": "Norton",
        "publication_year": 2020,
        "language": "English",
        "description": "Critical anthology analyzing Elizabethan drama, Shakespeare's tragedies, comedies, sonnets, linguistic rhetorical devices, historical context, and Renaissance stagecraft."
    }
]

# Generate transactions: realistic multi-borrowings to facilitate Apriori co-occurrence rules
SAMPLE_TRANSACTIONS = [
    # Computer Science & Data Science Co-borrowing group (Python + Data Mining + Machine Learning)
    {"transaction_id": "T1001", "reader_id": "R101", "book_id": "B001", "borrow_date": "2025-01-15", "due_date": "2025-01-29", "return_date": "2025-01-28", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1002", "reader_id": "R101", "book_id": "B002", "borrow_date": "2025-01-15", "due_date": "2025-01-29", "return_date": "2025-01-28", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1003", "reader_id": "R101", "book_id": "B003", "borrow_date": "2025-02-05", "due_date": "2025-02-19", "return_date": "2025-02-18", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1004", "reader_id": "R101", "book_id": "B006", "borrow_date": "2025-02-05", "due_date": "2025-02-19", "return_date": "2025-02-22", "fine": 3.0, "status": "Returned"},
    {"transaction_id": "T1005", "reader_id": "R101", "book_id": "B017", "borrow_date": "2025-03-01", "due_date": "2025-03-15", "return_date": "2025-03-14", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1006", "reader_id": "R101", "book_id": "B018", "borrow_date": "2025-03-20", "due_date": "2025-04-03", "return_date": "2025-04-01", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1007", "reader_id": "R101", "book_id": "B021", "borrow_date": "2025-04-05", "due_date": "2025-04-19", "return_date": None, "fine": 0.0, "status": "Borrowed"},
    {"transaction_id": "T1008", "reader_id": "R101", "book_id": "B007", "borrow_date": "2025-04-05", "due_date": "2025-04-19", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    # Reader R102 (High borrower in CS/Web)
    {"transaction_id": "T1009", "reader_id": "R102", "book_id": "B001", "borrow_date": "2025-01-16", "due_date": "2025-01-30", "return_date": "2025-01-29", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1010", "reader_id": "R102", "book_id": "B002", "borrow_date": "2025-01-16", "due_date": "2025-01-30", "return_date": "2025-01-29", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1011", "reader_id": "R102", "book_id": "B009", "borrow_date": "2025-02-10", "due_date": "2025-02-24", "return_date": "2025-02-23", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1012", "reader_id": "R102", "book_id": "B010", "borrow_date": "2025-02-10", "due_date": "2025-02-24", "return_date": "2025-02-23", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1013", "reader_id": "R102", "book_id": "B004", "borrow_date": "2025-03-05", "due_date": "2025-03-19", "return_date": "2025-03-18", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1014", "reader_id": "R102", "book_id": "B005", "borrow_date": "2025-03-05", "due_date": "2025-03-19", "return_date": "2025-03-18", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1015", "reader_id": "R102", "book_id": "B019", "borrow_date": "2025-04-01", "due_date": "2025-04-15", "return_date": None, "fine": 0.0, "status": "Borrowed"},
    {"transaction_id": "T1016", "reader_id": "R102", "book_id": "B020", "borrow_date": "2025-04-01", "due_date": "2025-04-15", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    # Reader R103 (Faculty - High borrower)
    {"transaction_id": "T1017", "reader_id": "R103", "book_id": "B002", "borrow_date": "2025-01-05", "due_date": "2025-02-05", "return_date": "2025-02-04", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1018", "reader_id": "R103", "book_id": "B003", "borrow_date": "2025-01-05", "due_date": "2025-02-05", "return_date": "2025-02-04", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1019", "reader_id": "R103", "book_id": "B006", "borrow_date": "2025-02-12", "due_date": "2025-03-12", "return_date": "2025-03-10", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1020", "reader_id": "R103", "book_id": "B008", "borrow_date": "2025-02-12", "due_date": "2025-03-12", "return_date": "2025-03-10", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1021", "reader_id": "R103", "book_id": "B018", "borrow_date": "2025-03-15", "due_date": "2025-04-15", "return_date": "2025-04-12", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1022", "reader_id": "R103", "book_id": "B007", "borrow_date": "2025-03-15", "due_date": "2025-04-15", "return_date": "2025-04-12", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1023", "reader_id": "R103", "book_id": "B001", "borrow_date": "2025-04-16", "due_date": "2025-05-16", "return_date": None, "fine": 0.0, "status": "Borrowed"},
    {"transaction_id": "T1024", "reader_id": "R103", "book_id": "B016", "borrow_date": "2025-04-16", "due_date": "2025-05-16", "return_date": None, "fine": 0.0, "status": "Borrowed"},
    {"transaction_id": "T1025", "reader_id": "R103", "book_id": "B017", "borrow_date": "2025-04-16", "due_date": "2025-05-16", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    # Reader R104 (Researcher - High borrower)
    {"transaction_id": "T1026", "reader_id": "R104", "book_id": "B001", "borrow_date": "2025-01-20", "due_date": "2025-02-10", "return_date": "2025-02-09", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1027", "reader_id": "R104", "book_id": "B002", "borrow_date": "2025-01-20", "due_date": "2025-02-10", "return_date": "2025-02-09", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1028", "reader_id": "R104", "book_id": "B003", "borrow_date": "2025-01-20", "due_date": "2025-02-10", "return_date": "2025-02-09", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1029", "reader_id": "R104", "book_id": "B007", "borrow_date": "2025-02-15", "due_date": "2025-03-05", "return_date": "2025-03-04", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1030", "reader_id": "R104", "book_id": "B008", "borrow_date": "2025-02-15", "due_date": "2025-03-05", "return_date": "2025-03-04", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1031", "reader_id": "R104", "book_id": "B018", "borrow_date": "2025-03-10", "due_date": "2025-03-30", "return_date": "2025-03-29", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1032", "reader_id": "R104", "book_id": "B021", "borrow_date": "2025-03-10", "due_date": "2025-03-30", "return_date": "2025-03-29", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1033", "reader_id": "R104", "book_id": "B016", "borrow_date": "2025-04-05", "due_date": "2025-04-25", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    # Reader R105 (IT Student - Medium borrower)
    {"transaction_id": "T1034", "reader_id": "R105", "book_id": "B004", "borrow_date": "2025-01-22", "due_date": "2025-02-05", "return_date": "2025-02-04", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1035", "reader_id": "R105", "book_id": "B005", "borrow_date": "2025-01-22", "due_date": "2025-02-05", "return_date": "2025-02-04", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1036", "reader_id": "R105", "book_id": "B009", "borrow_date": "2025-02-18", "due_date": "2025-03-04", "return_date": "2025-03-07", "fine": 3.0, "status": "Returned"},
    {"transaction_id": "T1037", "reader_id": "R105", "book_id": "B010", "borrow_date": "2025-02-18", "due_date": "2025-03-04", "return_date": "2025-03-07", "fine": 3.0, "status": "Returned"},
    {"transaction_id": "T1038", "reader_id": "R105", "book_id": "B012", "borrow_date": "2025-03-15", "due_date": "2025-03-29", "return_date": "2025-03-28", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1039", "reader_id": "R105", "book_id": "B011", "borrow_date": "2025-04-02", "due_date": "2025-04-16", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    # Reader R106 (Data Science - Medium borrower)
    {"transaction_id": "T1040", "reader_id": "R106", "book_id": "B001", "borrow_date": "2025-01-25", "due_date": "2025-02-08", "return_date": "2025-02-07", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1041", "reader_id": "R106", "book_id": "B002", "borrow_date": "2025-01-25", "due_date": "2025-02-08", "return_date": "2025-02-07", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1042", "reader_id": "R106", "book_id": "B003", "borrow_date": "2025-02-20", "due_date": "2025-03-06", "return_date": "2025-03-05", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1043", "reader_id": "R106", "book_id": "B021", "borrow_date": "2025-03-12", "due_date": "2025-03-26", "return_date": "2025-03-25", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1044", "reader_id": "R106", "book_id": "B007", "borrow_date": "2025-04-05", "due_date": "2025-04-19", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    # Reader R107 (Faculty Data Science - High borrower)
    {"transaction_id": "T1045", "reader_id": "R107", "book_id": "B001", "borrow_date": "2025-01-10", "due_date": "2025-02-10", "return_date": "2025-02-08", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1046", "reader_id": "R107", "book_id": "B002", "borrow_date": "2025-01-10", "due_date": "2025-02-10", "return_date": "2025-02-08", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1047", "reader_id": "R107", "book_id": "B003", "borrow_date": "2025-01-10", "due_date": "2025-02-10", "return_date": "2025-02-08", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1048", "reader_id": "R107", "book_id": "B006", "borrow_date": "2025-02-15", "due_date": "2025-03-15", "return_date": "2025-03-14", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1049", "reader_id": "R107", "book_id": "B007", "borrow_date": "2025-02-15", "due_date": "2025-03-15", "return_date": "2025-03-14", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1050", "reader_id": "R107", "book_id": "B016", "borrow_date": "2025-03-20", "due_date": "2025-04-20", "return_date": "2025-04-18", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1051", "reader_id": "R107", "book_id": "B018", "borrow_date": "2025-03-20", "due_date": "2025-04-20", "return_date": "2025-04-18", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1052", "reader_id": "R107", "book_id": "B021", "borrow_date": "2025-04-22", "due_date": "2025-05-22", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    # Reader R108 (Electrical - Low borrower)
    {"transaction_id": "T1053", "reader_id": "R108", "book_id": "B024", "borrow_date": "2025-02-01", "due_date": "2025-02-15", "return_date": "2025-02-14", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1054", "reader_id": "R108", "book_id": "B023", "borrow_date": "2025-03-01", "due_date": "2025-03-15", "return_date": "2025-03-14", "fine": 0.0, "status": "Returned"},

    # Reader R109 (IT Student - Medium borrower)
    {"transaction_id": "T1055", "reader_id": "R109", "book_id": "B004", "borrow_date": "2025-01-28", "due_date": "2025-02-11", "return_date": "2025-02-10", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1056", "reader_id": "R109", "book_id": "B005", "borrow_date": "2025-01-28", "due_date": "2025-02-11", "return_date": "2025-02-10", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1057", "reader_id": "R109", "book_id": "B009", "borrow_date": "2025-02-25", "due_date": "2025-03-11", "return_date": "2025-03-10", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1058", "reader_id": "R109", "book_id": "B011", "borrow_date": "2025-03-18", "due_date": "2025-04-01", "return_date": "2025-03-31", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1059", "reader_id": "R109", "book_id": "B012", "borrow_date": "2025-04-10", "due_date": "2025-04-24", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    # Reader R110 (Business Researcher - Medium borrower)
    {"transaction_id": "T1060", "reader_id": "R110", "book_id": "B013", "borrow_date": "2025-01-15", "due_date": "2025-02-05", "return_date": "2025-02-03", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1061", "reader_id": "R110", "book_id": "B014", "borrow_date": "2025-01-15", "due_date": "2025-02-05", "return_date": "2025-02-03", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1062", "reader_id": "R110", "book_id": "B022", "borrow_date": "2025-02-20", "due_date": "2025-03-10", "return_date": "2025-03-08", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1063", "reader_id": "R110", "book_id": "B016", "borrow_date": "2025-03-15", "due_date": "2025-04-05", "return_date": "2025-04-04", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1064", "reader_id": "R110", "book_id": "B001", "borrow_date": "2025-04-10", "due_date": "2025-04-30", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    # Reader R111 (Business Student - Low borrower)
    {"transaction_id": "T1065", "reader_id": "R111", "book_id": "B013", "borrow_date": "2025-02-01", "due_date": "2025-02-15", "return_date": "2025-02-14", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1066", "reader_id": "R111", "book_id": "B014", "borrow_date": "2025-02-01", "due_date": "2025-02-15", "return_date": "2025-02-14", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1067", "reader_id": "R111", "book_id": "B022", "borrow_date": "2025-03-10", "due_date": "2025-03-24", "return_date": "2025-03-28", "fine": 4.0, "status": "Returned"},

    # Reader R112 (Mechanical - Low borrower)
    {"transaction_id": "T1068", "reader_id": "R112", "book_id": "B023", "borrow_date": "2025-02-10", "due_date": "2025-02-24", "return_date": "2025-02-23", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1069", "reader_id": "R112", "book_id": "B016", "borrow_date": "2025-03-15", "due_date": "2025-03-29", "return_date": "2025-03-28", "fine": 0.0, "status": "Returned"},

    # Reader R113 (Mechanical Faculty - Medium borrower)
    {"transaction_id": "T1070", "reader_id": "R113", "book_id": "B023", "borrow_date": "2025-01-10", "due_date": "2025-02-10", "return_date": "2025-02-09", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1071", "reader_id": "R113", "book_id": "B024", "borrow_date": "2025-01-10", "due_date": "2025-02-10", "return_date": "2025-02-09", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1072", "reader_id": "R113", "book_id": "B016", "borrow_date": "2025-02-20", "due_date": "2025-03-20", "return_date": "2025-03-19", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1073", "reader_id": "R113", "book_id": "B001", "borrow_date": "2025-03-25", "due_date": "2025-04-25", "return_date": "2025-04-24", "fine": 0.0, "status": "Returned"},

    # Reader R114 (Literature - Low borrower)
    {"transaction_id": "T1074", "reader_id": "R114", "book_id": "B015", "borrow_date": "2025-02-15", "due_date": "2025-03-01", "return_date": "2025-02-28", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1075", "reader_id": "R114", "book_id": "B025", "borrow_date": "2025-03-05", "due_date": "2025-03-19", "return_date": "2025-03-18", "fine": 0.0, "status": "Returned"},

    # Reader R115 (Literature Researcher - Medium borrower)
    {"transaction_id": "T1076", "reader_id": "R115", "book_id": "B015", "borrow_date": "2025-01-20", "due_date": "2025-02-10", "return_date": "2025-02-09", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1077", "reader_id": "R115", "book_id": "B025", "borrow_date": "2025-01-20", "due_date": "2025-02-10", "return_date": "2025-02-09", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1078", "reader_id": "R115", "book_id": "B007", "borrow_date": "2025-03-01", "due_date": "2025-03-20", "return_date": "2025-03-19", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1079", "reader_id": "R115", "book_id": "B001", "borrow_date": "2025-04-02", "due_date": "2025-04-22", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    # Additional co-borrowing sessions across active readers:
    {"transaction_id": "T1080", "reader_id": "R116", "book_id": "B001", "borrow_date": "2025-02-18", "due_date": "2025-03-04", "return_date": "2025-03-03", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1081", "reader_id": "R116", "book_id": "B002", "borrow_date": "2025-02-18", "due_date": "2025-03-04", "return_date": "2025-03-03", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1082", "reader_id": "R116", "book_id": "B003", "borrow_date": "2025-03-12", "due_date": "2025-03-26", "return_date": "2025-03-25", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1083", "reader_id": "R116", "book_id": "B004", "borrow_date": "2025-03-12", "due_date": "2025-03-26", "return_date": "2025-03-25", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1084", "reader_id": "R116", "book_id": "B005", "borrow_date": "2025-04-05", "due_date": "2025-04-19", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    {"transaction_id": "T1085", "reader_id": "R117", "book_id": "B009", "borrow_date": "2025-02-20", "due_date": "2025-03-06", "return_date": "2025-03-05", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1086", "reader_id": "R117", "book_id": "B010", "borrow_date": "2025-02-20", "due_date": "2025-03-06", "return_date": "2025-03-05", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1087", "reader_id": "R117", "book_id": "B011", "borrow_date": "2025-03-15", "due_date": "2025-03-29", "return_date": "2025-04-02", "fine": 4.0, "status": "Returned"},

    {"transaction_id": "T1088", "reader_id": "R118", "book_id": "B001", "borrow_date": "2025-02-22", "due_date": "2025-03-08", "return_date": "2025-03-07", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1089", "reader_id": "R118", "book_id": "B002", "borrow_date": "2025-02-22", "due_date": "2025-03-08", "return_date": "2025-03-07", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1090", "reader_id": "R118", "book_id": "B003", "borrow_date": "2025-03-18", "due_date": "2025-04-01", "return_date": "2025-03-31", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1091", "reader_id": "R118", "book_id": "B021", "borrow_date": "2025-04-08", "due_date": "2025-04-22", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    {"transaction_id": "T1092", "reader_id": "R119", "book_id": "B013", "borrow_date": "2025-01-20", "due_date": "2025-02-20", "return_date": "2025-02-18", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1093", "reader_id": "R119", "book_id": "B014", "borrow_date": "2025-01-20", "due_date": "2025-02-20", "return_date": "2025-02-18", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1094", "reader_id": "R119", "book_id": "B022", "borrow_date": "2025-02-25", "due_date": "2025-03-25", "return_date": "2025-03-24", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1095", "reader_id": "R119", "book_id": "B016", "borrow_date": "2025-04-01", "due_date": "2025-05-01", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    {"transaction_id": "T1096", "reader_id": "R120", "book_id": "B017", "borrow_date": "2025-02-25", "due_date": "2025-03-11", "return_date": "2025-03-10", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1097", "reader_id": "R120", "book_id": "B018", "borrow_date": "2025-02-25", "due_date": "2025-03-11", "return_date": "2025-03-10", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1098", "reader_id": "R120", "book_id": "B019", "borrow_date": "2025-03-20", "due_date": "2025-04-03", "return_date": "2025-04-02", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1099", "reader_id": "R120", "book_id": "B020", "borrow_date": "2025-03-20", "due_date": "2025-04-03", "return_date": "2025-04-02", "fine": 0.0, "status": "Returned"},

    {"transaction_id": "T1100", "reader_id": "R122", "book_id": "B001", "borrow_date": "2025-01-25", "due_date": "2025-02-15", "return_date": "2025-02-14", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1101", "reader_id": "R122", "book_id": "B002", "borrow_date": "2025-01-25", "due_date": "2025-02-15", "return_date": "2025-02-14", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1102", "reader_id": "R122", "book_id": "B003", "borrow_date": "2025-02-20", "due_date": "2025-03-12", "return_date": "2025-03-11", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1103", "reader_id": "R122", "book_id": "B006", "borrow_date": "2025-02-20", "due_date": "2025-03-12", "return_date": "2025-03-11", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1104", "reader_id": "R122", "book_id": "B007", "borrow_date": "2025-03-18", "due_date": "2025-04-08", "return_date": "2025-04-07", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1105", "reader_id": "R122", "book_id": "B008", "borrow_date": "2025-03-18", "due_date": "2025-04-08", "return_date": "2025-04-07", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1106", "reader_id": "R122", "book_id": "B018", "borrow_date": "2025-04-12", "due_date": "2025-05-02", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    # Reader R123 (Data Science - Medium borrower)
    {"transaction_id": "T1107", "reader_id": "R123", "book_id": "B001", "borrow_date": "2025-03-01", "due_date": "2025-03-15", "return_date": "2025-03-14", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1108", "reader_id": "R123", "book_id": "B002", "borrow_date": "2025-03-01", "due_date": "2025-03-15", "return_date": "2025-03-14", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1109", "reader_id": "R123", "book_id": "B003", "borrow_date": "2025-03-25", "due_date": "2025-04-08", "return_date": "2025-04-07", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1110", "reader_id": "R123", "book_id": "B007", "borrow_date": "2025-04-12", "due_date": "2025-04-26", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    # Reader R124 (Faculty IT - High borrower)
    {"transaction_id": "T1111", "reader_id": "R124", "book_id": "B004", "borrow_date": "2025-01-15", "due_date": "2025-02-15", "return_date": "2025-02-14", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1112", "reader_id": "R124", "book_id": "B005", "borrow_date": "2025-01-15", "due_date": "2025-02-15", "return_date": "2025-02-14", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1113", "reader_id": "R124", "book_id": "B009", "borrow_date": "2025-02-20", "due_date": "2025-03-20", "return_date": "2025-03-19", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1114", "reader_id": "R124", "book_id": "B010", "borrow_date": "2025-02-20", "due_date": "2025-03-20", "return_date": "2025-03-19", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1115", "reader_id": "R124", "book_id": "B011", "borrow_date": "2025-03-25", "due_date": "2025-04-25", "return_date": "2025-04-24", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1116", "reader_id": "R124", "book_id": "B012", "borrow_date": "2025-03-25", "due_date": "2025-04-25", "return_date": "2025-04-24", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1117", "reader_id": "R124", "book_id": "B019", "borrow_date": "2025-04-28", "due_date": "2025-05-28", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    # Reader R125 (Business Student - Low borrower)
    {"transaction_id": "T1118", "reader_id": "R125", "book_id": "B013", "borrow_date": "2025-03-05", "due_date": "2025-03-19", "return_date": "2025-03-18", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1119", "reader_id": "R125", "book_id": "B014", "borrow_date": "2025-03-05", "due_date": "2025-03-19", "return_date": "2025-03-18", "fine": 0.0, "status": "Returned"},

    # Reader R127 (CS Student - Low borrower)
    {"transaction_id": "T1120", "reader_id": "R127", "book_id": "B001", "borrow_date": "2025-03-10", "due_date": "2025-03-24", "return_date": "2025-03-23", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1121", "reader_id": "R127", "book_id": "B002", "borrow_date": "2025-03-10", "due_date": "2025-03-24", "return_date": "2025-03-23", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1122", "reader_id": "R127", "book_id": "B017", "borrow_date": "2025-04-02", "due_date": "2025-04-16", "return_date": None, "fine": 0.0, "status": "Borrowed"},

    # Reader R128 (Data Science Researcher - High borrower)
    {"transaction_id": "T1123", "reader_id": "R128", "book_id": "B001", "borrow_date": "2025-01-10", "due_date": "2025-01-31", "return_date": "2025-01-30", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1124", "reader_id": "R128", "book_id": "B002", "borrow_date": "2025-01-10", "due_date": "2025-01-31", "return_date": "2025-01-30", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1125", "reader_id": "R128", "book_id": "B003", "borrow_date": "2025-01-10", "due_date": "2025-01-31", "return_date": "2025-01-30", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1126", "reader_id": "R128", "book_id": "B006", "borrow_date": "2025-02-14", "due_date": "2025-03-07", "return_date": "2025-03-06", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1127", "reader_id": "R128", "book_id": "B007", "borrow_date": "2025-02-14", "due_date": "2025-03-07", "return_date": "2025-03-06", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1128", "reader_id": "R128", "book_id": "B018", "borrow_date": "2025-03-12", "due_date": "2025-04-02", "return_date": "2025-04-01", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1129", "reader_id": "R128", "book_id": "B021", "borrow_date": "2025-03-12", "due_date": "2025-04-02", "return_date": "2025-04-01", "fine": 0.0, "status": "Returned"},
    {"transaction_id": "T1130", "reader_id": "R128", "book_id": "B016", "borrow_date": "2025-04-15", "due_date": "2025-05-06", "return_date": None, "fine": 0.0, "status": "Borrowed"}
]
