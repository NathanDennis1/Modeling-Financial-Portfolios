# COMPSCI 1090A Project Timeline

[Project Timeline Link](https://edstem.org/us/courses/59912/lessons/113457/slides/622103)

The details below outline each stage of the CS 1090A project journey:

### 🚀✨ Milestone Overview

- **Pitch Projects & Evaluations**  
  - *Guidelines Coming Soon!*  
  - **Project Proposals Due:** 9/25  
  - Students submit proposals over two weeks, followed by peer evaluation over one week. The course staff will then finalize and release a list of approved project options.

- **MS1: Finalize Groups and Choose Projects**  
  - **Due Date:** 10/18  
  - **Grade Weight:** 5%  
  - Groups may switch members based on project preference until the due date. Each group will select their top 4 project choices from the approved list.

- **Groups and Projects Assigned**  
  - **Date:** 10/21  
  - Project assignments are released to groups by course staff.

- **MS2: Data Acquisition and Preprocessing**  
  - **Due Date:** 10/30  
  - **Grade Weight:** 10%  
  - Students acquire and preprocess data, addressing issues such as missing values, imbalance, scaling, and potential errors.

- **MS3: EDA, Project Plan Adjustments, and Goal Setting**  
  - **Due Date:** 11/13  
  - **Grade Weight:** 15%  
  - After data cleaning, students conduct an Exploratory Data Analysis (EDA) to refine project goals and adjust their project plans.

- **MS4: Baseline Model and Pipeline Development**  
  - **Due Date:** 12/2  
  - **Grade Weight:** 25%  
  - Students create a baseline model and establish a pipeline for training/testing an advanced model.

- **MS5: Final Project Submission and Deliverables**  
  - **Due Date:** 12/16  
  - **Grade Weight:** 45%  
  - Final deliverables include a comprehensive report and a 6-minute video presentation.

*Note: Detailed guidelines for each milestone will be provided as deadlines approach.*

---

## Project: Large Financial Managers – Understanding Portfolio Compositions via SEC Form 13F Data

### Group Members
- **David Bombara** - [davidbombara@g.harvard.edu](mailto:davidbombara@g.harvard.edu)
- **Aditya Saxena** - [adityasaxena@g.harvard.edu](mailto:adityasaxena@g.harvard.edu)
- **Nathan Dennis** - [nathandennis@g.harvard.edu](mailto:nathandennis@g.harvard.edu)

### Background and Motivation
The SEC Form 13F, filed quarterly by institutional investors, increases public visibility of their equity holdings. This project aims to analyze these filings from Q2 2013 to Q3 2024 to gain insights into the holdings and strategies of large institutional investors like hedge funds, which typically operate with limited transparency. Examining these quarterly holdings may reveal cross-sectional and time-series trends at both firm and market levels.

### Data
The project will use the Form 13F data, available through the SEC's EDGAR system. This dataset includes filing details such as submission types, filing dates, issuer names, CUSIP numbers, and market values. Despite its relevance in capturing large-scale investment activities, the dataset may contain errors or inconsistencies due to self-reported data. These challenges will be addressed during the EDA phase, with a focus on handling missing or incorrect entries.

- **Data Source:** [SEC Form 13F Data Sets](https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets)

### Scope
The project will begin with exploratory data analysis to uncover trends in institutional holdings. This includes cross-sectional analysis comparing portfolio compositions across institutions each quarter and time-series analysis to observe changes over time. Planned methods include linear regression to model relationships and clustering to group similar strategies. This project offers hands-on experience with data cleaning, analysis, and modeling, enhancing our understanding of institutional investment behaviors.
