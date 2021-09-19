import pandas as pd
import math
import plotly.express as px
from datetime import date

class DoublingTimeCalculatorGlobal:
    def __init__(self):
        pass

    def __getCountryCodes(self):
        filename = "https://gist.githubusercontent.com/tadast/8827699/raw/3cd639fa34eec5067080a61c69e3ae25e3076abb/countries_codes_and_coordinates.csv"
        dfCountryCodes = pd.read_csv(filename)
        dfCountryCodes = dfCountryCodes[["Country", "Alpha-3 code"]]
        dfCountryCodes["Alpha-3 code"] = dfCountryCodes["Alpha-3 code"].apply(lambda x: x[2:5])
        countryCodes = {}
        for i in range(len(dfCountryCodes)):
            countryName = dfCountryCodes.loc[i, "Country"]
            code = dfCountryCodes.loc[i, "Alpha-3 code"]
            countryCodes[countryName] = code
        return countryCodes

    def calcDoublingTime(self):
        today = date.today()
        oneDay = date(year=2018, month=7, day=13) - date(year=2018, month=7, day=12)
        oneWeek = date(year=2018, month=7, day=19) - date(year=2018, month=7, day=12)
        start = today - oneWeek
        startFormat, todayFormat = str(start.strftime("%m-%d-%Y")), str((start + oneWeek - oneDay).strftime("%m-%d-%Y"))
        dfList=[]
        while start!=today:
            dateFormat = str(start.strftime("%m-%d-%Y"))
            filename = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+dateFormat+".csv"
            df = pd.read_csv(filename)
            dfList.append(df)
            start += oneDay
        countries,countriesDataframe=[],pd.DataFrame([], columns=["Country_Region"])
        countriesDataframe["Country_Region"]=dfList[-1]["Country_Region"]
        for i in range(len(countriesDataframe)):
            countryName=countriesDataframe.loc[i,"Country_Region"]
            if not countryName in countries:
                countries.append(countryName)
        dfListStart,dfListEnd,dfStart,dfEnd=[],[],dfList[0],dfList[-1]
        for i in countries:
            countStart=countEnd=0
            dfStartTemp=pd.DataFrame([], columns=["Country_Region","Confirmed Cases on "+startFormat])
            dfEndTemp=pd.DataFrame([], columns=["Country_Region","Confirmed Cases on "+todayFormat])
            for j in range(len(dfStart)):
                if dfStart.loc[j,"Country_Region"]==i:
                    dfStartTemp.loc[countStart,"Country_Region"]=i
                    dfStartTemp.loc[countStart,"Confirmed Cases on "+startFormat]=dfStart.loc[j,"Confirmed"]
                    countStart+=1
            for j in range(len(dfEnd)):
                if dfEnd.loc[j,"Country_Region"]==i:
                    dfEndTemp.loc[countEnd,"Country_Region"]=i
                    dfEndTemp.loc[countEnd,"Confirmed Cases on "+todayFormat]=dfEnd.loc[j,"Confirmed"]
                    countEnd+=1
            dfListStart.append(dfStartTemp)
            dfListEnd.append(dfEndTemp)
        dfStartFinal=pd.DataFrame([], columns=["Country_Region","Confirmed Cases on "+startFormat])
        dfEndFinal=pd.DataFrame([], columns=["Country_Region","Confirmed Cases on "+todayFormat])
        countStart=countEnd=0
        for i in dfListStart:
            countryName=i.loc[0,"Country_Region"]
            i["Confirmed Cases on "+startFormat]=i["Confirmed Cases on "+startFormat].apply(lambda x: float(x))
            totalConfirmed=i["Confirmed Cases on "+startFormat].sum()
            dfStartFinal.loc[countStart,"Country_Region"]=countryName
            dfStartFinal.loc[countStart,"Confirmed Cases on "+startFormat]=totalConfirmed
            countStart+=1
        for i in dfListEnd:
            countryName = i.loc[0, "Country_Region"]
            i["Confirmed Cases on " + todayFormat] = i["Confirmed Cases on " + todayFormat].apply(lambda x: float(x))
            totalConfirmed = i["Confirmed Cases on " + todayFormat].sum()
            dfEndFinal.loc[countEnd, "Country_Region"] = countryName
            dfEndFinal.loc[countEnd, "Confirmed Cases on " + todayFormat] = totalConfirmed
            countEnd += 1
        dfFinal=pd.DataFrame([], columns=["Country_Region","Confirmed Cases on "+startFormat,
                                          "Confirmed Cases on "+todayFormat,"Change in Confirmed Cases","Doubling Time in Days"])
        dfFinal["Country_Region"]=dfStartFinal["Country_Region"]
        dfFinal["Confirmed Cases on "+startFormat]=dfStartFinal["Confirmed Cases on "+startFormat]
        dfFinal["Confirmed Cases on "+todayFormat]=dfEndFinal["Confirmed Cases on "+todayFormat]
        dfFinal["Change in Confirmed Cases"]=dfFinal["Confirmed Cases on "+todayFormat]-dfFinal["Confirmed Cases on "+startFormat]

        puertoRico={"Country_Region":"Puerto Rico"}
        for i in range(2):
            if i==0:
                filename = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/"+startFormat+".csv"
                df = pd.read_csv(filename)
                df=df[df["Province_State"]=="Puerto Rico"]
                puertoRico["Confirmed Cases on "+startFormat]=float(df["Confirmed"])
            elif i==1:
                filename = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/"+todayFormat+".csv"
                df = pd.read_csv(filename)
                df = df[df["Province_State"] == "Puerto Rico"]
                puertoRico["Confirmed Cases on "+todayFormat] = float(df["Confirmed"])
        puertoRico["Change in Confirmed Cases"]=puertoRico["Confirmed Cases on "+todayFormat]-puertoRico["Confirmed Cases on "+startFormat]
        index=len(dfFinal)
        dfFinal.loc[index,"Country_Region"]="Puerto Rico"
        dfFinal.loc[index,"Confirmed Cases on "+startFormat]=puertoRico["Confirmed Cases on "+startFormat]
        dfFinal.loc[index,"Confirmed Cases on "+todayFormat]=puertoRico["Confirmed Cases on "+todayFormat]
        dfFinal.loc[index,"Change in Confirmed Cases"]=puertoRico["Change in Confirmed Cases"]

        for i in range(len(dfFinal)):
            if dfFinal.loc[i,"Change in Confirmed Cases"]<=0:
                dfFinal = dfFinal[dfFinal["Country_Region"] != dfFinal.loc[i,"Country_Region"]]
            else:
                num=dfFinal.loc[i,"Change in Confirmed Cases"]/dfFinal.loc[i,"Confirmed Cases on "+startFormat]
                numerator=math.log(2)
                denominator=math.log(1+num)
                dTime=(numerator/denominator)*7
                dfFinal.loc[i,"Doubling Time in Days"]=round(dTime,2)
        dfFinal.loc[0,"Country_Region"]="United States"
        countryCodes=self.__getCountryCodes()
        dfFinal['countryCode'] = dfFinal['Country_Region'].apply(lambda x: countryCodes[x] if x in countryCodes else None)
        dfFinal["Doubling Time in Days"]=dfFinal["Doubling Time in Days"].apply(lambda x: float(x))
        dfFinal["Doubling Time Score"]=dfFinal["Doubling Time in Days"].apply(lambda x: (math.log(x)**1.9))
        dfFinal["Change in Confirmed Cases"] = dfFinal["Change in Confirmed Cases"].apply(lambda x: float(x))
        dfFinal["Size Score"]=dfFinal["Change in Confirmed Cases"].apply(lambda x: x**0.5)

        dfFinal.loc[55,"Country_Region"]="Republic of the Congo"
        dfFinal.loc[56, "Country_Region"] = "Democratic Republic of the Congo"
        dfFinal.loc[58, "Country_Region"] = "Côte d'Ivoire"
        dfFinal.loc[62, "Country_Region"] = "Czech Republic"
        dfFinal.loc[73, "Country_Region"] = "Swaziland/Eswatini"
        dfFinal.loc[101, "Country_Region"] = "South Korea"
        dfFinal.loc[168, "Country_Region"] = "Taiwan"

        dfFinal.loc[55, "countryCode"] = "COG"
        dfFinal.loc[56, "countryCode"] = "COD"
        dfFinal.loc[58, "countryCode"] = "CIV"
        dfFinal.loc[62, "countryCode"] = "CZE"
        dfFinal.loc[73, "countryCode"] = "SWZ"
        dfFinal.loc[93, "countryCode"] = "IRN"
        dfFinal.loc[101, "countryCode"] = "KOR"
        dfFinal.loc[102, "countryCode"] = "RKS"
        dfFinal.loc[135, "countryCode"]= "MKD"
        dfFinal.loc[167, "countryCode"] = "SYR"
        dfFinal.loc[168, "countryCode"] = "TWN"

        # fig = px.choropleth(dfFinal, locations="countryCode", color="Doubling Time Score", hover_name="Country_Region",
        #                     hover_data=["Doubling Time in Days", "Confirmed Cases on " + startFormat,
        #                                 "Confirmed Cases on " + todayFormat],
        #                     color_continuous_scale=px.colors.diverging.RdYlGn,
        #                     locationmode='ISO-3', scope="world")

        fig = px.scatter_geo(dfFinal, locations="countryCode", color="Doubling Time Score", hover_name="Country_Region",
                             hover_data=["Doubling Time in Days", "Confirmed Cases on " + startFormat,
                                         "Confirmed Cases on " + todayFormat,"Change in Confirmed Cases"],
                             size="Size Score", size_max=40,
                             color_continuous_scale=px.colors.diverging.RdYlGn, locationmode='ISO-3', scope="world")
        fig.update_layout(geo=dict(bgcolor='rgba(78,133,253,1)'))
        fig.show()

test=DoublingTimeCalculatorGlobal()
test.calcDoublingTime()

# df=test.calcDoublingTime()
# print(df.loc[102])