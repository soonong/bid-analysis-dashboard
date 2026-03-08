import json
from datetime import datetime

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

dec_data = [r for r in data if '2025-12-01' <= r.get('입력일', '')[:10] <= '2025-12-31']
pure_seoul = [r for r in dec_data if ('서울' in r.get('지역제한', '') or '서울특별시' in r.get('지역제한', '')) and '전국' not in r.get('지역제한', '') and '전기' in r.get('종목', '')]

print("All elements with their price and jongmok:")
cnt_172 = 0
amt_172 = 0

for r in pure_seoul:
    reg = r.get('지역제한', '').strip()
    jong = r.get('종목', '').strip()
    amt = r.get('추정가격', 0)
    
    # Let's try to find exactly what makes 172 by looking at exclusions
    # from pure_seoul (which has 189)
    # the user said 172 and 75,418,481,366
    
    if jong == '전기':
        # what if only '전기' and only '서울'?
        if reg == '서울':
            cnt_172 += 1
            amt_172 += amt

print(f"If EXACTLY '서울' and EXACTLY '전기': Count={cnt_172}, Amount={amt_172:,}")

# Let's see if there is any subset of pure_seoul that sums to 75418481366
# pure_seoul amount is 45,181,747,086 ? Wait! My earlier script showed 45.1B!
# The user says "넌 451억에 189 라고 나와있어. 왜그런거?" => "You say 189 and 45.1B."
# "내가 본건 172개에 75,418,481,366인데?" (I see 172 and 75.4B?)

# Let's look for how user might get 172 and 75.4B.
# Could the user be INCLUDING nationwide, but filtering manually?
# Nationwide + Seoul + Electric = 202.
import itertools
target_amt = 75418481366
target_cnt = 172

print("User amount:", target_amt)

# What if user's data does NOT filter out 전국? 
# Maybe they filter out something else?

