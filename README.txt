README

CS598-PSL Project 4: Movie Recommender

- Tim Crosling (tgc3@illinois.edu) - App Dev and System 2 Implementation<br>
- Kin Yik Lam (kinyikl2@illinois.edu) - System 2 Refinement and Review, System 1 review<br>
- Chua Swee Kwang (skchua2@illinois.edu) - System 1 Implementation, quality review

Code Reference:
(1) index.html - frontend webpage for the app.  Hosted on AWS Amplify at https://main.d3cgn4rz35jqti.amplifyapp.com/
(2) AWS_Lambda_Script.py - Backend server implementing systems 1 & 2.  Hosted on AWS Lambda "GetMovies" function

Note: to operate the solution you also need to configure an AWS API Gateway "GetMovies" to connect the frontend to backend.  The solution also relies on two S3 files: 
- Top_30_Similarity_Matrix saved by System 3 (https://cs598-psl.s3.us-east-2.amazonaws.com/top_30_similarity_matrix(1).csv)
- Columns.csv providing a shortcut column headings for the S matrix for use in the lambda script (https://cs598-psl.s3.us-east-2.amazonaws.com/columns.csv)