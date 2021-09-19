import pandas as pd
import math
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

class DoublingTimeCalculatorUS:
    def __init__(self):
        pass

    def calcDoublingTime(self):
        today=date.today()
        oneDay=date(year=2018,month=7,day=13)-date(year=2018,month=7,day=12)
        oneWeek=date(year=2018,month=7,day=19)-date(year=2018,month=7,day=12)
        start = today-oneWeek
        startFormat, todayFormat=str(start.strftime("%m-%d-%Y")), str((start+oneWeek-oneDay).strftime("%m-%d-%Y"))
        dfList=[]
        while start!=today:
            dateFormat=str(start.strftime("%m-%d-%Y"))
            filename="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/"+dateFormat+".csv"
            df=pd.read_csv(filename)
            dfList.append(df)
            start+=oneDay
        df=pd.DataFrame([], columns=["Province_State","Country_Region","Confirmed Cases on "+startFormat,"Confirmed Cases on "+todayFormat,
                                     "Change in Confirmed Cases","Doubling Time in Days"])
        df["Province_State"]=dfList[0]["Province_State"]
        df["Country_Region"] = dfList[0]["Country_Region"]
        df["Confirmed Cases on "+startFormat]= dfList[0]["Confirmed"]
        df["Confirmed Cases on " + todayFormat]=dfList[-1]["Confirmed"]
        df["Change in Confirmed Cases"]=dfList[-1]["Confirmed"]-dfList[0]["Confirmed"]

        for i in range(len(df)):
            if df.loc[i,"Change in Confirmed Cases"]<=0:
                df = df[df["Province_State"] != df.loc[i,"Province_State"]]
            else:
                num=df.loc[i,"Change in Confirmed Cases"]/df.loc[i,"Confirmed Cases on "+startFormat]
                num*=100
                numerator=math.log(2)
                denominator=math.log(1+(num/100))
                dTime=(numerator/denominator)*7
                df.loc[i,"Doubling Time in Days"]=round(dTime,2)

        dfFinal=df[["Province_State","Country_Region","Doubling Time in Days"]]
        dfFinal["Confirmed Cases on " + startFormat]=df["Confirmed Cases on "+startFormat]
        dfFinal["Confirmed Cases on " + todayFormat]= df["Confirmed Cases on " + todayFormat]
        dfFinal["Change in Confirmed Cases"] = df["Change in Confirmed Cases"]
        dfFinal["Doubling Time in Days"]=dfFinal["Doubling Time in Days"].apply(lambda x: float(x))
        dfFinal["Doubling Time Score"]=dfFinal["Doubling Time in Days"].apply(lambda x: math.log(x))
        dfFinal["Doubling Time Score"]=dfFinal["Doubling Time Score"].apply(lambda x: round(x,2))

        state_codes = {
            'District of Columbia': 'dc', 'Mississippi': 'MS', 'Oklahoma': 'OK',
            'Delaware': 'DE', 'Minnesota': 'MN', 'Illinois': 'IL', 'Arkansas': 'AR',
            'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 'Louisiana': 'LA',
            'Idaho': 'ID', 'Wyoming': 'WY', 'Tennessee': 'TN', 'Arizona': 'AZ',
            'Iowa': 'IA', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT',
            'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 'Montana': 'MT',
            'California': 'CA', 'Massachusetts': 'MA', 'West Virginia': 'WV',
            'South Carolina': 'SC', 'New Hampshire': 'NH', 'Wisconsin': 'WI',
            'Vermont': 'VT', 'Georgia': 'GA', 'North Dakota': 'ND',
            'Pennsylvania': 'PA', 'Florida': 'FL', 'Alaska': 'AK', 'Kentucky': 'KY',
            'Hawaii': 'HI', 'Nebraska': 'NE', 'Missouri': 'MO', 'Ohio': 'OH',
            'Alabama': 'AL', 'Rhode Island': 'RI', 'South Dakota': 'SD',
            'Colorado': 'CO', 'New Jersey': 'NJ', 'Washington': 'WA',
            'North Carolina': 'NC', 'New York': 'NY', 'Texas': 'TX',
            'Nevada': 'NV', 'Maine': 'ME'}

        dfFinal['state_code'] = dfFinal['Province_State'].apply(lambda x: state_codes[x] if x in state_codes else None)
        dfFinal = dfFinal[dfFinal["Province_State"] != "Virgin Islands"]
        # fig = px.choropleth(dfFinal,locations="state_code",color="Doubling Time Score",hover_name="Province_State",
        #                     hover_data=["Doubling Time in Days","Confirmed Cases on "+startFormat,"Confirmed Cases on "+todayFormat],
        #                     color_continuous_scale=px.colors.diverging.RdYlGn,
        #                     locationmode='USA-states',scope="usa")
        #

        fig = px.scatter_geo(dfFinal,locations="state_code",color="Doubling Time Score",hover_name="Province_State",
                             hover_data=["Doubling Time in Days","Confirmed Cases on "+startFormat,"Confirmed Cases on "+todayFormat],
                             size="Change in Confirmed Cases",size_max=90,
                             color_continuous_scale=px.colors.diverging.RdYlGn,locationmode='USA-states',scope="usa")
        fig.update_layout(geo=dict(bgcolor='rgba(78,133,253,1)'))
        #fig.update_layout(title_text="https://drive.google.com/drive/u/0/my-drive")
        fig.show()

test=DoublingTimeCalculatorUS()
test.calcDoublingTime()

# df=test.calcDoublingTime()
# s=df["Change in Confirmed Cases"]
#
# print(type(s))