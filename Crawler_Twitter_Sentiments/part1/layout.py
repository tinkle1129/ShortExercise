import plotly.plotly as py
import pandas as pd

df = pd.read_csv('data/attitude.csv')

data = [ dict(
        type = 'choropleth',
        locations = df['CODE'],
        z = df['ATTITUDE'],
        text = df['COUNTRY'],
        colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
            [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            title = 'ATTITUDE<br>POSITIVE'), #tickprefix = '$',
      ) ]

layout = dict(
    title = 'THAAD ATTITUDE',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.plot( fig, validate=False, filename='d3-world-map' )