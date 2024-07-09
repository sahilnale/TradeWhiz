# TradeWhiz

TradeWhiz is a sophisticated web application designed to allow users to simulate stock trading in a risk-free environment. This project aims to provide a realistic trading experience, enabling users to practice their strategies, analyze market trends, and make informed trading decisions without the risk of financial loss.

## Features

### Real-Time Stock Data
TradeWhiz utilizes APIs to fetch live stock data, ensuring that users have access to the most current market information. This feature helps in making accurate and timely trading decisions.

### Market Sentiment Analysis
By leveraging Natural Language Processing (NLP) techniques, TradeWhiz analyzes market sentiment from various news sources. This analysis helps users understand the market mood and predict potential stock movements.

### Interactive and User-Friendly Interface
Built with React, TradeWhiz offers a seamless and intuitive user experience. The interface is designed to be interactive, making it easy for users to navigate through different features and functionalities.

### Secure and Scalable Backend
The backend is developed using Flask, ensuring a robust and secure environment for handling user data. TradeWhiz is deployed on AWS EC2, providing scalability and reliability.


## Technologies Used
- **Frontend:** React
- **Backend:** Flask
- **Database:** MongoDB
- **Web Scraping:** BeautifulSoup
- **NLP:** NLTK
- **Hosting:** AWS EC2

## Getting Started

### Prerequisites
To run TradeWhiz locally, you need to have the following installed:
- Node.js
- Python
- MongoDB


### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sahilnale/TradeWhiz.git
   cd TradeWhiz
   ```

2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. Start MongoDB:
   ```bash
   mongod
   ```

5. Run the backend server:
   ```bash
   python app.py
   ```

6. Run the frontend server:
   ```bash
   cd frontend
   npm start
   ```

## Usage
1. Open your browser and navigate to `http://localhost:3000`.
2. Register or log in to start using TradeWhiz.
3. Explore real-time stock data, practice trading, and analyze market sentiment.

## Contributing
We welcome contributions to TradeWhiz. Please fork the repository and submit a pull request for any features, enhancements, or bug fixes.

## License
This project is licensed under the MIT License.

## Contact
For any queries or support, please contact:
- Sahil Nale
- Email: [sahilnale@ucla.edu](mailto:sahilnale@ucla.edu)
- GitHub: [sahilnale](https://github.com/sahilnale)

---

TradeWhiz is designed to provide a comprehensive and immersive experience for those looking to enhance their trading skills and knowledge. Happy trading!
