# ESPP simulator
A simple script to compare [ESPP](https://www.investopedia.com/terms/e/espp.asp#:~:text=What%20Is%20an%20Employee%20Stock,date%20and%20the%20purchase%20date.) vs. an alternative investment (e.g. a stock market index) projected value over time

The values shown are the projected total holdings over time and the ratio between them, derived from the parameters.

Provides both a plot and tabular data


Personally, I used it to get a sense of the cost of diversifying my portfolio vs. "putting all the eggs in one basket".

## How to run
[Run online in a notebook](https://datalore.jetbrains.com/notebook/L5aLk8hKwv2yIZSG9YzZRV/kHifqtHaqFr1wYtTncq8Lw/)

Created with [Jetbrains Datalore](https://datalore.jetbrains.com/notebooks). You can sign in with Google and click "clone to home folder" to edit the parameters.

## Notes:
__The following far-fetched assumptions have been made to simplify the analysis:__
* Both the stock and index have a fixed, evenly-distributed average monthly return. For example, if the average annual return is set to 8%, the monthly return needs to be 0.643% to compound to 8% annually.
* The tax otherwise deducted in the ESPP option is used as an addition to the alternative investment in the index.
* Quick sells (if enabled) are immediate and reinvested directly in the alternative index

# Disclaimer:
I am not a financial advisor. Do not take anything in this script as financial advice.

## Example
![image](https://user-images.githubusercontent.com/20489303/172060353-7cff0d04-4040-45b8-9ad5-09625428d241.png)

#### Example values in PyCharm debugger:
![image](https://user-images.githubusercontent.com/20489303/172056516-0a904a0b-e492-4529-8757-5df597762511.png)
