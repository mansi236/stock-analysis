import yfinance as yf
import pandas as pd


df=pd.read_csv('Stocks.csv')
stock_df=pd.DataFrame(df.iloc[:,[0,1]])

stockName_list=list(stock_df.iloc[:,0])


start_date = "2023-12-06"
end_date = "2023-12-08"  

#creat function for fetching api for daily candle data
def closing_price():
    closing_lst=[]


    for symbol in stockName_list:
        ticker = f"{symbol}.NS"  # Append '.NS' for NSE stocks
        
        data = yf.download(ticker, start=start_date, end=end_date, interval="1d")
        
        # Extract only the Close column
        close_prices = data['Close']
        
        # print(close_prices)  # Print the Close column for verification
        closing_lst.append(close_prices)  # Append Close column to list

    # Optional: Combine all close prices into a single DataFrame for further analysis
    closing_data = pd.concat(closing_lst, axis=1)
    closing_data.columns = stockName_list  # Set column names to stock symbols
    
    return closing_data.T
close_price=closing_price()

#input of total amount you want to invest
total_amount=int(input("enter the total amount you want to invest: "))

amount_list=[]
weightage=df.iloc[:,1]
#calculating total amount to be invested in each stock
for weight in weightage :
    invst_each_stk=weight*total_amount
    amount_list.append(invst_each_stk)

#calculating number of shares that can bought with that amount 
share_list=[]
cp=close_price.iloc[:,1]
for amount in amount_list:
    for price in cp:
        num_of_share=price/amount
        share_list.append(num_of_share)
        break

#adding amount of each stock and number of share in dataframe
stock_df['amount of each stock']=amount_list
stock_df['number of share']=share_list

print(stock_df)

stock_df.to_excel('output.xlsx', index=False)

