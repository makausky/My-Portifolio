import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

def cleaner(original_series):
    
    aux = pd.Series(original_series, name='publishDate').replace('', 'null', regex=True)

    for i in range(len(aux)):
        if aux[i][-1] == 'h':
            aux[i] = "2020-03-05"
        elif aux[i][-1] == 'd':
            aux[i] = pd.to_datetime("2020-03-05") - pd.Timedelta(days=int(re.sub('[a-zA-Z]', '', aux[i])))
        elif aux[i][-1] == 'w':
            aux[i] = pd.to_datetime("2020-03-05") - pd.Timedelta(days=int(re.sub('[a-zA-Z]', '', aux[i])) * 7)
        #Jan
        elif aux[i].upper().find("JAN") != -1:
            if aux[i].split()[-1] == "'19":
                aux[i] = '2019-01-' + aux[i].split()[0]
            else:
                aux[i] = '2020-01-' + aux[i].split()[0]
        #Feb
        elif aux[i].upper().find("FEB") != -1:
            if aux[i].split()[-1] == "'19":
                aux[i] = '2019-02-' + aux[i].split()[0]
            else:
                aux[i] = '2020-02-' + aux[i].split()[0]
        #Mar
        elif aux[i].upper().find("MAR") != -1 or aux[i].upper().find("MRT") != -1:
            if aux[i].split()[-1] == "'19":
                aux[i] = '2019-03-' + aux[i].split()[0]
            else:
                aux[i] = '2020-03-' + aux[i].split()[0]
        #Apr
        elif aux[i].upper().find("APR") != -1:
            if aux[i].split()[-1] == "'19":
                aux[i] = '2019-04-' + aux[i].split()[0]
            else:
                aux[i] = '2020-04-' + aux[i].split()[0]
        #May
        elif aux[i].upper().find("MAY") != -1 or aux[i].upper().find("MEI") != -1:
            if aux[i].split()[-1] == "'19":
                aux[i] = '2019-05-' + aux[i].split()[0]
            else:
                aux[i] = '2020-05-' + aux[i].split()[0]
        #Jun
        elif aux[i].upper().find("JUN") != -1:
            if aux[i].split()[-1] == "'19":
                aux[i] = '2019-06-' + aux[i].split()[0]
            else:
                aux[i] = '2020-06-' + aux[i].split()[0]
        #Jul
        elif aux[i].upper().find("JUL") != -1:
            if aux[i].split()[-1] == "'19":
                aux[i] = '2019-07-' + aux[i].split()[0]
            else:
                aux[i] = '2020-07-' + aux[i].split()[0]
        #Aug
        elif aux[i].upper().find("AUG") != -1:
            if aux[i].split()[-1] == "'19":
                aux[i] = '2019-08-' + aux[i].split()[0]
            else:
                aux[i] = '2020-08-' + aux[i].split()[0]
        #Sep
        elif aux[i].upper().find("SEP") != -1:
            if aux[i].split()[-1] == "'19":
                aux[i] = '2019-09-' + aux[i].split()[0]
            else:
                aux[i] = '2020-09-' + aux[i].split()[0]
        #Oct
        elif aux[i].upper().find("OCT") != -1 or aux[i].upper().find("OKT") != -1:
            if aux[i].split()[-1] == "'19":
                aux[i] = '2019-10-' + aux[i].split()[0]
            else:
                aux[i] = '2020-10-' + aux[i].split()[0]
        #Nov
        elif aux[i].upper().find("NOV") != -1:
            if aux[i].split()[-1] == "'19":
                aux[i] = '2019-11-' + aux[i].split()[0]
            else:
                aux[i] = '2020-11-' + aux[i].split()[0]
        #Dec    
        elif aux[i].upper().find("DEC") != -1:
            if aux[i].split()[-1] == "'19":
                aux[i] = '2019-12-' + aux[i].split()[0]
            else:
                aux[i] = '2020-12-' + aux[i].split()[0]
        else:
            aux[i] = np.nan
    
    return aux

def splitter(original_series):
    
    aux = original_series
    dfaux = pd.DataFrame()

    # Prepare for splitting
    for i in range(len(aux)):
        if aux[i].find(' - ') != -1:
            aux[i] = aux[i].replace(' - ', '-')
        else:    
            aux[i] = aux[i].replace(' -\n                            ', '-')

    # Split in two series (minAge & maxAge)
    dfaux['matchAge'] = original_series
    dfaux['minAge'] = aux.astype(str).str.split('-').str[0]
    dfaux['maxAge'] = aux.astype(str).str.split('-').str[1]

    # Cast minAge into Integer type
    dfaux['minAge'] = dfaux['minAge'].apply(lambda x: re.sub('[a-zA-Z]', '', x))
    dfaux['minAge'] = dfaux['minAge'].str.strip()
    dfaux['minAge'] = dfaux['minAge'].replace('', 0)
    dfaux['minAge'] = dfaux['minAge'].astype({'minAge':'int'})

    # Cast maxAge into Integer type
    dfaux['maxAge'] = dfaux['maxAge'].apply(lambda x: re.sub('[a-zA-Z]', '', x))
    dfaux['maxAge'] = dfaux['maxAge'].str.strip()
    dfaux['maxAge'] = dfaux['maxAge'].replace('', 99)
    dfaux['maxAge'] = dfaux['maxAge'].astype({'maxAge':'int'})


    return dfaux

def pareto(original_df, column_name):

    colname = column_name
    df = original_df.reset_index()
    df[colname] = df[colname].astype(str)

    # Calculate the cumulative percentage
    df['cumulative_percent'] = (df['count'].cumsum() / df['count'].sum()) * 100

    # Create a bar chart of the counts
    fig, ax1 = plt.subplots(figsize=(16,5))
    ax1.bar(df[colname], df['count'])
    ax1.set_ylabel('Count')

    # Adjust spacing between x-axis labels
    plt.xticks(rotation=90, ha='right')

    # Create a line chart of the cumulative percentages
    ax2 = ax1.twinx()
    ax2.plot(df[colname], df['cumulative_percent'], color='orange', linewidth=2.5, marker='o')
    ax2.set_ylim([0, 100])
    ax2.set_ylabel('Cumulative Percentage')

    # Add a legend
    ax1.legend(['Count'], loc='upper left')
    ax2.legend(['Cumulative Percentage'], loc='upper right')

    # Set the title 
    plt.title(colname)

    # Return the chart
    ax2 = ax2.grid(visible=True, axis='y')
    
    return plt.show()