import streamlit as s
import pandas as p
from streamlit_folium import st_folium
import folium
import branca.colormap as cm

def folium_map(aa):
    ll=['Count of Observations','Average Weighted','Average Unweighted','Minimum', 'Maximum']
    dd1={"CO₂ in Seawater":" FCO2","Temperature in Celsius":" SST","Salinity in Seawater":" SALINITY"}
    dd2={'Count of Observations':"COUNT_NOBS_YEAR",'Average Weighted':"AVE_WEIGHTED_YEAR",'Average Unweighted':"AVE_UNWTD_YEAR",'Minimum':"MIN_UNWTD_YEAR", 'Maximum':"MAX_UNWTD_YEAR"}
    
    attr=('&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)')
    tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png'
    fl=False
    
    if(aa == 'CO₂ in Seawater'):
        df=p.read_csv("SOCATCO2_0.csv")
        cc=s.columns(4)
        with cc[0]:
            v1=s.selectbox("Please Enter the Month",[i for i in range(1,13)])
        with cc[1]:
            v2=s.selectbox("Please Enter the Year",[i for i in range(2024,1950,-1)]) 
        with cc[2]:
            v3=s.selectbox("Please enter the type of data",ll)
        with cc[3]:
            fl=s.button("Predict", type="primary")
        color = cm.LinearColormap(colors=['yellow','orange','red'], index=[200,350,450]) 
        if(v1<10):
            a=df[df.DATE.str.startswith(str(v2)+"-"+"0"+str(v1))]
          
        else:
            
            a=df[df.DATE.str.startswith(str(v2)+"-"+str(v1))]
            
        a.reset_index(inplace=True,drop=True)   
        
        m=folium.Map(min_lat=-90,max_lat=90,min_lon=-180,max_lon=180,max_bounds=True,zoom_start=3,max_zoom = 9,min_zoom = 2,location=[0,0])
        
        for i in range(a.shape[0]):
            folium.CircleMarker(location=(a[' LAT'][i],a[' LON'][i]),radius=2.5, color=color(a[dd1[aa]+"_"+dd2[v3]][i]), fill_color =color(a[dd1[aa]+"_"+dd2[v3]][i]),popup=a[dd1[aa]+"_"+dd2[v3]][i], fill_opacity=1).add_to(m)
        st_data = st_folium(m,width=1750)
    elif(aa=='Temperature in Celsius'):
        df=p.read_csv("SOCATCO2_1.csv") 
        cc=s.columns(4)
        with cc[0]:
            v1=s.selectbox("Please Enter the Month",[i for i in range(1,13)])
        with cc[1]:
            v2=s.selectbox("Please Enter the Year",[i for i in range(1950,2024)]) 
        with cc[2]:
            v3=s.selectbox("Please enter the type of data",ll)
        

        color = cm.LinearColormap(colors=['blue','red'], index=[10,40])
        
        m=folium.Map(tiles=tiles,attr=attr,min_lat=-90,max_lat=90,min_lon=-180,max_lon=180,max_bounds=True,zoom_start=3,max_zoom = 9,min_zoom = 2,location=[0,0])
        for i in range(df.shape[0]):
            #folium.CircleMarker(location=(a[' LAT'][i],a[' LON'][i]),radius=2.5, color=color(df[dd1[aa]+"_"+dd2[v3]][i]), fill_color =color(df[dd1[aa]+"_"+dd2[v3]][i]),popup=a[df[dd1[aa]+"_"+dd2[v3]][i], fill_opacity=1).add_to(m)
            pass
        st_data = st_folium(m,width=1750)
    elif(aa=='Salinity in Seawater'):
        df=p.read_csv("SOCATCO2_2.csv") 
        cc=s.columns(3)
        with cc[0]:
            v1=s.selectbox("Please Enter the Month",[i for i in range(1,13)])
        with cc[1]:
            v2=s.selectbox("Please Enter the Year",[i for i in range(1950,2024)]) 
        with cc[2]:
            v3=s.selectbox("Please enter the type of data",ll) 
        
        color = cm.LinearColormap(colors=['purple','green','red'], index=[20,35,45])
        
        m=folium.Map(tiles=tiles,attr=attr,min_lat=-90,max_lat=90,min_lon=-180,max_lon=180,max_bounds=True,zoom_start=3,max_zoom = 9,min_zoom = 2,location=[0,0])
        for i in range(df.shape[0]):
            folium.CircleMarker(location=(a[' LAT'][i],a[' LON'][i]),radius=2.5, color=color(df[dd1[aa]+"_"+dd2[v3]][i]), fill_color =color(df[dd1[aa]+"_"+dd2[v3]][i]),tooltip=df[dd1[aa]+"_"+dd2[v3]][i], fill_opacity=1).add_to(m)
        st_data = st_folium(m,width=1750) 
    s.write(fl)
if __name__=="__main__":
    s.set_page_config(page_title='Sea Water Dataset',layout='wide')
    s.title("  Surface Ocean CO₂ Atlas ")
    aa=s.selectbox("What kind of data you want?",['CO₂ in Seawater','Temperature in Celsius','Salinity in Seawater'])
    folium_map(aa)
    
    
