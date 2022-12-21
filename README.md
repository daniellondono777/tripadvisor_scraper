<h1 align="left">Trip Advisor Scraper</h1>

  <p align="left">
    This system scraps relevant information from tripadvisor.com and converts it into a string with CSV format. It uses Flask in order to provide API functionality.
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

- Designed for Iceberg Data
- Author: Daniel Londoño B. 



### Built With

* 🌶️ Flask
* 🥣 BeautifulSoup
* 🐼 Pandas




<!-- GETTING STARTED -->
## Getting Started

In order to run the project, it is advised to follow the following steps. 

### Prerequisites

This project was developed using Python3.10.4. You can download it from here: https://www.python.org/downloads/

* Once you cloned the repository, on the project's root folder, run in order to activate the local environment:
  ```sh
  source env/bin/activate
  ```

* Followed by
  ```sh
  pip3 install -r requirements.txt
  ```

* To start the server, run:
  ```sh
  python3 backend.py
  ```

<!-- USAGE EXAMPLES -->
## Usage

Once the server is running, with Postman (or any other request system) create a GET request to localhost:5000/scrap . This request must contain a JSON Body as follows.
  ```sh
  {"ciudad" : your_desired_colombian_city}
  ```

<!-- CONTACT -->
## Contact

Daniel Londoño - [@LinkedIn](https://www.linkedin.com/in/daniel-londo%C3%B1o-60189a132/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
