# Loan Request Verification



**Solution Overview:**

This Git repository hosts a comprehensive solution designed to streamline the loan request verification process. Working solution is available under this [link](https://loanapplicationverification.azurewebsites.net/).

**Caution:** Since this solution is a demo it heavily relies on free-tier resources. If the quota is exceeded, there may be a temporary service interruption until the limits are reset.





**Solution Architecture:**


![LoanApplicationVerification_arch_diagram drawio](https://github.com/KatarzynaSzmydki/Loan_Request_Verification/assets/104822281/62a2f785-a921-4cc4-ae96-1824694d5fce)


**Key Characteristics:**

_Machine Learning Integration_: The solution seamlessly integrates classification model to assess and verify loan requests, providing a layer of decision-making based on predictive analytics.

_Flask Web Application_: The code incorporates a Flask web application, offering an intuitive and user-friendly interface for interacting with the loan request verification system. Bootstrap is utilized to enhance the application's aesthetic appeal and responsiveness.

_Dynamic Badge Visualization_: The application dynamically visualizes verification outcomes through badges, employing Bootstrap styling to intuitively communicate results to end-users.

_Data Analysis and Visualization_: Utilizing Power BI report available as part of Flask application, the solution presents processed loan request data in an organized and visually appealing manner, enhancing user understanding and facilitating efficient decision-making. It focuses on loan characteristict correlation with loan acceptance.

_Responsive Design_: The web application features a responsive design, ensuring optimal user experience across various devices and screen sizes.


**Purpose:**

The primary purpose of this solution is to showcase a fully functioning platform for verifying loan requests through the integration of machine learning models within web application. By combining Flask, Bootstrap, and machine learning capabilities, the repository aims to offer a sophisticated yet accessible tool for efficient loan request decision-making.

**Technology Used:**

- Azure Web Services
- Azure SQL Database
- Azure Data Factory to copy data to Azure SQL database in scheduled intervals and re-train classification model (Databricks)
- Power BI report
- Flask framework


**See short preview of the solution**


https://github.com/KatarzynaSzmydki/Loan_Request_Verification/assets/104822281/003f4bf3-3b73-41d9-8eeb-cb2bf160a72a










