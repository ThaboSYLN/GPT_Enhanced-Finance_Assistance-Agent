# GPT-Enhanced Finance Assistance Agent

## Overview
This project is a Streamlit-based web application that serves as a GPT-enhanced finance assistant. It provides users with financial advice, stock analysis, and web-supplemented information using OpenAI's GPT models and real-time financial data.

## Features
- User authentication system
- Web supplementation for finance-related queries
- Private advisory based on user context
- Stock analysis with interactive charts
- Real-time financial news integration

## Installation

1. Clone the repository:
git clone https://github.com/ThaboSYLN/GPT_Enhanced-Finance_Assistance-Agent.git
cd GPT_Enhanced-Finance_Assistance-Agent

2. Install required packages:
pip install -r requirements.txt

3. Set up environment variables:

Create a file named `keyHolder.env` in the root directory and add your API keys:
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_news_api_key_here

## API Key Setup

### OpenAI API Key
1. Visit [OpenAI](https://openai.com/)
2. Sign up or log in to your account
3. Navigate to the API section to generate your API key
4. Note: OpenAI API usage may incur costs

### News API Key
1. Register at [News API](https://newsapi.ai/register)
2. After registration, you'll receive your free API key

## Usage

1. Run the Streamlit app:
streamlit run app.py

2. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`)

3. Register for an account or log in if you already have one

4. Explore the different tabs:
- Web Supplementation: Ask finance-related questions
- Private Advisory: Get personalized financial advice
- Stock Analysis: Analyze stock performance with interactive charts

## Project Demo
  please download the video:- https://drive.google.com/file/d/1UMNDcDrP7UGPH3Z4WYVS_z79H5n_WoBu/view?usp=drive_link

## Limitations and Future Improvements
- Currently limited to a predefined set of financial news sources
- Future plans include:
- Expanding the range of financial data sources
- Implementing more advanced stock analysis tools
- Enhancing the user interface for better accessibility

## Contributing
Contributions to improve the project are welcome. Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes and commit (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer
This application is for educational purposes only. It is not intended to provide professional financial advice. Always consult with a qualified financial advisor before making investment decisions.

## Author
Created by Thabo SYLN as part of a university project(UKZN COMP301-Software design).
