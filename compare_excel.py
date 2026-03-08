import pandas as pd

# Load my CSV
my_df = pd.read_csv('2025_12_Seoul_Electric.csv')
my_bids = set(my_df['공고번호'].astype(str).str.strip())

my_amt = my_df['추정가격'].sum()
my_cnt = len(my_df)

print(f"[MY DATA] Count: {my_cnt}, Amount: {my_amt:,}")

# Load User Excel
try:
    user_df = pd.read_excel('12월 전기.xlsx')
    
    # check if '공고번호' exists or '등록번호' etc.
    bid_col = None
    for col in user_df.columns:
        if '공고번호' in str(col).replace(' ', '') or col == '번호':
            bid_col = col
            break
            
    if bid_col:
        user_bids = set(user_df[bid_col].astype(str).str.strip())
        
        # let's try to find an amount column
        amt_col = None
        for col in user_df.columns:
            if '추정가격' in str(col).replace(' ', ''):
                amt_col = col
                break
        
        user_amt = user_df[amt_col].sum() if amt_col else "Unknown"
        user_cnt = len(user_df)
        print(f"[USER DATA] Count: {user_cnt}, Amount: {user_amt:,}" if amt_col else f"[USER DATA] Count: {user_cnt}")
        
        only_mine = my_bids - user_bids
        only_user = user_bids - my_bids
        
        print("\n[DIFFERENCE]")
        print(f"Items ONLY in MY CSV: {len(only_mine)}")
        if only_mine:
            print(f"Example ONLY in MY CSV: {list(only_mine)[:5]}")
            # Print details of one of these from my_df
            missing_in_user = my_df[my_df['공고번호'].astype(str).str.strip().isin(only_mine)]
            print("Why are they not in user's data? Let's trace their values:")
            for idx, row in missing_in_user.head(5).iterrows():
                print(f"  {row['공고번호']} | {row.get('지역제한','')} | {row.get('종목','')} | {row.get('추정가격',0):,}")
            
        print(f"Items ONLY in USER Excel: {len(only_user)}")
        if only_user:
            print(f"Example ONLY in USER Excel: {list(only_user)[:5]}")

    else:
        print("Could not find '공고번호' column in user's Excel. Columns:")
        print(user_df.columns.tolist())
        
except Exception as e:
    print(f"Error reading user Excel: {e}")

