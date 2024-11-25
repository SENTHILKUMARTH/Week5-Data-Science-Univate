class Univariate():

    def quanQual(dataset):
        quan=[]
        qual=[]
        for columnName in dataset.columns:
            #print(columnName)
            if(dataset[columnName].dtype=='O'):
                #print("qual")
                qual.append(columnName)
            else:
                #print("quan")
                quan.append(columnName)
        return quan,qual

    def freqTable(colunName,dataset,pd):
        freqTable = pd.DataFrame(columns=["Unique_Values","Frequency","Relative Frequency","Cusum"])
        freqTable["Unique_Values"]=dataset[colunName].value_counts().index
        freqTable["Frequency"]=dataset[colunName].value_counts().values
        freqTable["Relative Frequency"]=(freqTable["Frequency"]/103)
        freqTable["Cusum"]=freqTable["Relative Frequency"].cumsum()
        return freqTable

    def Outlier(dataset,pd,quant):
        univariate = pd.DataFrame(index=["Mean","Median","Mode","Q1:25","Q2:50","Q3:75","Q4:100","IQR","1.5Rule","Lesser","Greater","Min","Max"],columns =quant)
        for columnName in quant:
            univariate.loc["Mean", [columnName]] = dataset[columnName].mean()
            univariate.loc["Median", [columnName]] = dataset[columnName].median()
            univariate.loc["Mode", [columnName]] = dataset[columnName].mode()[0]
            univariate.loc["Q1:25", [columnName]] = dataset.describe()[columnName]["25%"]
            univariate.loc["Q2:50", [columnName]] = dataset.describe()[columnName]["50%"]
            univariate.loc["Q3:75", [columnName]] = dataset.describe()[columnName]["75%"]
            univariate.loc["Q4:100", [columnName]] = dataset.describe()[columnName]["max"]
            univariate.loc["IQR", [columnName]] = univariate.loc["Q3:75", [columnName]] - univariate.loc["Q1:25", [columnName]]
            univariate.loc["1.5Rule", [columnName]] = 1.5* univariate.loc["IQR", [columnName]]
            univariate.loc["Lesser", [columnName]] = univariate.loc["Q1:25", [columnName]] - univariate.loc["1.5Rule", [columnName]]
            univariate.loc["Greater", [columnName]] = univariate.loc["Q3:75", [columnName]] + univariate.loc["1.5Rule", [columnName]]
            univariate.loc["Min", [columnName]] = dataset[columnName].min()
            univariate.loc["Max", [columnName]] = dataset[columnName].max()
        return univariate
        
    def CheckOutlierExists(univariate):
        lesser=[]
        greater=[]
        for columnName in univariate:
            if(univariate[columnName]["Min"]<univariate[columnName]["Lesser"]):
                lesser.append(columnName)
            if(univariate[columnName]["Max"]>univariate[columnName]["Greater"]):
                greater.append(columnName)
        return lesser, greater
        
    def UpdateOutliers(dataset, univariate, lesser, greater):
        for column in lesser:
            dataset.loc[dataset[column] < univariate[column]["Lesser"], column] = univariate[column]["Lesser"]
        for column in greater:
            dataset.loc[dataset[column] > univariate[column]["Greater"], column] = univariate[column]["Greater"]    
        return dataset
