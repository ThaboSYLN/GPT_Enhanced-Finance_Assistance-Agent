import streamlit as st
from openai import OpenAI
import os
import requests
import yfinance as yf
import plotly.graph_objects as go
from dotenv import load_dotenv
from auth import auth_required, login_page, register_page, logout

# Load environment variables
load_dotenv('keyHolder.env')

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_financial_news():
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/top-headlines?category=business&apiKey={api_key}"
    response = requests.get(url)
    articles = response.json()['articles']
    return "\n".join([f"{article['title']}: {article['description']}" for article in articles[:5]])

def web_supplementation(query):
    news = get_financial_news()
    
    full_prompt = f"""You are an AI assistant that provides factual, concise, and direct answers similar to a web search engine or browser. 
    Based on the following recent financial news and the user's query, provide a clear and informative response:

    Recent financial news:
    {news}

    User query: {query}
    
    
    Respond in a way that directly answers the query, incorporating relevant information from the news if applicable. 
    If the query can't be answered based on the given information, provide a general, factual response related to the topic."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a web search assistant providing clear, factual,detailed information and analysis."},
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=1500,
        n=1,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def private_advisory(query, context=""):
    full_prompt = f"{context}\n\nAs a personal finance assistant and market analyst, please provide advice on the following: {query}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a personal finance assistant and market analyst."},
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=300,
        n=1,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()


def get_stock_data(ticker, period='1y'):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)


def plot_stock_data(data, ticker):
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
    fig.update_layout(title=f"{ticker} Stock Price", xaxis_title="Date", yaxis_title="Price")
    return fig


st.set_page_config(page_title="Finance Assistant💲💹", page_icon="💲")
st.title("GPT-enhanced Finance Assistant")


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    

if not st.session_state.logged_in:
    auth_option = st.sidebar.radio("Choose an option", ["Login", "Register"])
    if auth_option == "Login":
        login_page()
    else:
        register_page()
else:
    st.sidebar.write(f"Welcome, {st.session_state.username}!")
    if st.sidebar.button("Logout"):
        logout()
        st.experimental_rerun()
        
        

@auth_required
def main_app():
    st.sidebar.header("User Context")
    age = st.sidebar.slider("Age", 18, 100, 21)
    income = st.sidebar.number_input("Annual Income (R)", min_value=0, value=50000)
    savings = st.sidebar.number_input("Current Savings (R)", min_value=0, value=10000)
    risk_tolerance = st.sidebar.select_slider("Risk Tolerance", options=["Low", "Medium", "High"])

    user_context = f"User is {age} years old, with an annual income of R{income}, current savings of R{savings}, and a {risk_tolerance.lower()} risk tolerance."

    tab1, tab2, tab3 = st.tabs(["Web Supplementation", "Private Advisory", "Stock Analysis"])
    

    with tab1: 
       # Initialize chat history if it doesn't exist
        if "web_supplementation_history" not in st.session_state:
            st.session_state.web_supplementation_history = []

        # Display a one-time welcome message before any queries
        if len(st.session_state.web_supplementation_history) == 0:
            st.header("💬 Let's talk finance!") 

        # Display chat history only after some interaction
        if len(st.session_state.web_supplementation_history) > 0:
            st.subheader("Conversation History")

            # Display all previous queries and answers
            for entry in st.session_state.web_supplementation_history:
                with st.chat_message("user"):
                    st.write(entry['query'])
                with st.chat_message("assistant"):
                    st.write(entry['answer'])

        # Create an empty placeholder for the chat input at the bottom
        placeholder = st.empty()

        # Use the placeholder to hold the chat input box
        query = placeholder.chat_input("Enter your finance-related query:")

        if query:  # Trigger when the user submits
            answer = web_supplementation(query)

            # Append the query and answer to the chat history
            st.session_state.web_supplementation_history.append({"query": query, "answer": answer})

            # Re-run the app to refresh with the new input
            st.rerun()




            

    with tab2:
        st.header("Private Advisory")
        query = st.text_area("What financial advice do you need?")
        if st.button("Get Advice"):
            advice = private_advisory(query, user_context)
            st.write("Advice:", advice)
            

    with tab3:
        st.header("Stock Analysis")
        ticker = st.text_input("Enter stock ticker (e.g., AAPL for Apple):")
        if st.button("Analyze"):
            data = get_stock_data(ticker)
            st.plotly_chart(plot_stock_data(data, ticker))
            
            analysis = private_advisory(f"Provide a brief analysis of {ticker} stock based on recent performance.")
            st.write("Analysis:", analysis)


    st.sidebar.markdown("---")
    st.sidebar.write("Disclaimer: This app provides general information and is not a substitute for professional financial advice.")


if __name__ == "__main__":
    main_app()