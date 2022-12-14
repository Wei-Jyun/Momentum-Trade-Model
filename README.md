# Momentum-Trade-Model
以下使用我部署的<a href="http://silenceblog.ml/MomentumDemo/">個人網站</a>作為功能介紹 
<br>
![image](https://user-images.githubusercontent.com/62560900/207608281-704e561f-ba84-4103-b093-4f5cbc4a110a.png)
<br>
這是一個基於動能交易策略所寫成的一個網頁應用，有關動能交易可以參考以下資訊：<a href="https://www.ig.com/us/trading-strategies/momentum-trading-strategies--a-beginners-guide-190905">動能策略簡介</a>

透過這個應用，您可以輸入多個市場標的及時間參數給模型進行運算，

模型會根據歷史的收盤價格及時間參數計算動能強弱值，

並且在比較之後提供最高動能強弱值之標的作為買進訊號，

針對在每個星期五的收盤價進行模擬交易(有關為何以週五作為交易日，後面我會提供我的一些看法)，

程式會從交易起始的10,000美元開始交易直到最新一周的收盤價格，

並且在最後運用前端數據視覺化框架提供回測結果。

# 設定回測模型標的
![image](https://user-images.githubusercontent.com/62560900/207610490-aaefc919-29c3-4b35-9cc3-37571d827b52.png)
<br>
首先，在這邊您可以設定要投入回測運算的股市標的(後端是以抓取yahoo Finance的數據為主， 所以請參考該網站的代號規則)，只要點擊綠色的add more即可新增標的欄位。

以下提供一些股票代號的示例，

您也可以前往Yahoo Finance查詢股票代號：

<ul>
    <li>納斯達克100指數：^NDX</li>
    <li>道瓊工業指數：^DJI</li>
    <li>S&P500指數：^GSPC</li>
    <li>蘋果：AAPL</li>
    <li>特斯拉：TSLA</li>
</ul>

註：由於不同市場的交易日及報價數據上會有差異，建議輸入時以同個市場區域為主。
#設定時間參數
![image](https://user-images.githubusercontent.com/62560900/207612213-0e29625b-c882-4e3f-95d5-059a8aca09d8.png)
<br>
設定時間參數
確定標的後，接下來需要設定回測的起始日期以及時間參數，

由於需要時間參數的運算決定動能數據，才可以進行交易回測，

因此起始日期建議可以設定為過去五年以上，

這個項目預設可以輸入3個時間參數，

但若您認為不需要這麼多參數，您可以將其他參數設定為0，不會影響回測結果。

註：由於時間參數亦會影響運算交易之起始日，建議設定一個不會過大的數值。

(一般來說只要起始日設定夠長，360內的參數都是可以提供運算的)
# 開始回測
講到這邊，如果上述的前置設定都有做了，那麼就可以開始來回測啦!
<br>
![image](https://user-images.githubusercontent.com/62560900/207612895-eb1c2cd5-a5bf-4b6e-9aee-af35f96855bb.png)

點選完開始回測後，等待頁面更新即可在前端看到視覺化的結果囉!
![image](https://user-images.githubusercontent.com/62560900/207613595-2bec1570-4b85-4adc-99c4-c0d620e3f9ba.png)

