#steam market comparison for booster packs vs steam cards
#make UI w/ OpenCV
from bs4 import BeautifulSoup, SoupStrainer
import requests
from math import fsum

#details about cards
def trading_cards(game_title, foil):
    allPrice = []
    
    if foil.lower() == 'y':
        addend = '&category_753_cardborder%5B%5D=tag_cardborder_1'
    else:
        addend = '&category_753_cardborder%5B%5D=tag_cardborder_0'
        
    getTitle = SoupStrainer(class_="market_listing_row market_recent_listing_row market_listing_searchresult")
    req = requests.get('https://steamcommunity.com/market/search?q=&category_753_Game%5B%5D=any&category_753_item_class%5B%5D=tag_item_class_2&appid=753&q=' + game_title.replace(" ", "+") + addend)
    soup = BeautifulSoup(req.content, 'lxml', parse_only=getTitle)
    
    for x in soup.find_all(class_='market_listing_row market_recent_listing_row market_listing_searchresult'):
        #print(x.find(class_='normal_price'))
        for y in x.find_all(class_='normal_price'):
            if y.string != None:
                print(x.find(class_='market_listing_item_name').string + ': ' + x.find(class_='market_listing_game_name').string + ' | ' + y.string)
                allPrice.append(float(y.string[1:]))
    #print(allPrice)   
    Min = sorted(allPrice[0:3])
    Max = sorted(allPrice[len(allPrice) - 4:len(allPrice) - 1])
    nuMin = []
    nuMax = []
    
    for x in Min:
        
        if x * .15 <= 0.02:
            x -= 0.02
        else:
            x *= .85
            
        nuMin.append(x)
    for y in Max:        
        if y * .15 <= 0.02:
            y -= 0.02
        else:
            y *= .85
            
        nuMax.append(x)
        
    Min = nuMin
    Max = nuMax
    
    print("Min gain: " + '$' + str(round(fsum(Min), 2)), "Max: " + '$' + str(round(fsum(Max), 2)))
    booster(game_title, round(fsum(Min), 2))

#details about booster packs                         
def booster(game_title, unpackPrice):
    req = requests.get('https://steamcommunity.com/market/search?q=&category_753_Game%5B%5D=any&category_753_item_class%5B%5D=tag_item_class_5&appid=753&q=' + game_title.replace(" ", "+"))
    getTitle = SoupStrainer(class_="market_listing_row market_recent_listing_row market_listing_searchresult")
    soup = BeautifulSoup(req.content, 'lxml', parse_only=getTitle)
    
    for x in soup.find_all(class_='market_listing_row market_recent_listing_row market_listing_searchresult'):
        #print(x.find(class_='normal_price'))
        for y in x.find_all(class_='normal_price'):
            if y.string != None:
                price = float(y.string[1:])
                
                if price * .15 <= 0.02:
                    price -= 0.02
                    
                else:
                    price *= .85
                   
                print(x.find(class_='market_listing_item_name').string + ' | ' + '$' + str(round(price, 2)))
                print("Minimum net gain from unpacking: " + str(round(unpackPrice - price, 2)))
    
trading_cards(input('Name of game? '), input('Foil cards included? (Y/N) '))