import streamlit as s
import pandas as p
from streamlit_folium import st_folium,folium_static
import folium
import branca.colormap as cm

##  https://discuss.streamlit.io/t/avoid-page-reload-when-interacting-with-folium-map/61957/2

def map_create(a,color):
    attr=('&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)')
    tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png'
    dd1={"CO₂ in Seawater":" FCO2","Temperature in Celsius":" SST","Salinity in Seawater":" SALINITY"}
    dd2={'Count of Observations':"COUNT_NOBS_YEAR",'Average Weighted':"AVE_WEIGHTED_YEAR",'Average Unweighted':"AVE_UNWTD_YEAR",'Minimum':"MIN_UNWTD_YEAR", 'Maximum':"MAX_UNWTD_YEAR"}
    
    
    if 'm' not in s.session_state or s.session_state.m is None or v3!=s.session_state['type'] or v2!=s.session_state['year'] or v1!=s.session_state['month'] or aa!=s.session_state['kind']:
        m=folium.Map(tiles=tiles,attr=attr,min_lat=-90,max_lat=90,min_lon=-180,max_lon=180,max_bounds=True,zoom_start=3,max_zoom = 9,min_zoom = 2,location=[0,0])
        for i in range(a.shape[0]):
            folium.CircleMarker(location=(a[' LAT'][i],a[' LON'][i]),radius=2.5, color=color(a[dd1[aa]+"_"+dd2[v3]][i]), fill_color =color(a[dd1[aa]+"_"+dd2[v3]][i]),tooltip=a[dd1[aa]+"_"+dd2[v3]][i], fill_opacity=1).add_to(m)
        color.add_to(m)
        s.session_state.m = m 

        s.session_state['type'],s.session_state['year'],s.session_state['month'],s.session_state['kind']=v3,v2,v1,aa

    return s.session_state.m    
    



def folium_map(aa,v):
    
    
    attr=('&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)')
    tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png'
    
    
    if(aa == 'CO₂ in Seawater'):
        df=p.read_csv(r"SOCATCO2_0.csv")
        
        if(v=='Count of Observations'):
            color=cm.LinearColormap(colors=['green','red'], vmin=0,vmax=500,caption='Number of Observations')
            pass 
        else:
            color = cm.LinearColormap(colors=['yellow','orange','red'], vmin=0,vmax=500,caption='CO₂ in Seawater (ppm)') 
       
        #s.write(a.shape)  tiles=tiles,attr=attr,
        
    elif(aa=='Temperature in Celsius'):
        df=p.read_csv("SOCATCO2_1.csv") 
        if(v=='Count of Observations'):
            color=cm.LinearColormap(colors=['green','red'], vmin=0,vmax=500,caption='Number of Observations')
            pass 
        else:     
            color = cm.LinearColormap(colors=['blue','red'], vmin=10,vmax=40)
        
    elif(aa=='Salinity in Seawater'):
        df=p.read_csv("SOCATCO2_2.csv") 
        if(v=='Count of Observations'):
            color=cm.LinearColormap(colors=['green','red'], vmin=0,vmax=500,caption='Number of Observations')
        else:
            color = cm.LinearColormap(colors=['purple','green','red'], vmin=20,vmax=40) 
    if(v1<10):
        a=df[df.DATE.str.startswith(str(v2)+"-"+"0"+str(v1))]
          
    else:
        a=df[df.DATE.str.startswith(str(v2)+"-"+str(v1))]
            
    a.reset_index(inplace=True,drop=True)   
    m=map_create(a,color)
    folium_static(m, width=1500, height=750)
        

def main():
    #s.set_page_config(page_title='Sea Water Dataset',layout='wide')
    s.title("  Surface Ocean CO₂ Atlas ")
    global aa
    aa=s.selectbox("Kind of data?",['CO₂ in Seawater','Temperature in Celsius','Salinity in Seawater'])
    cc=s.columns(3)
    ll=['Count of Observations','Average Weighted','Average Unweighted','Minimum', 'Maximum']
    
    if('kind' not in s.session_state or 'type' not in s.session_state or 'year' not in s.session_state or 'month' not in s.session_state):
        s.session_state['kind'],s.session_state['type'],s.session_state['year'],s.session_state['month']='CO₂ in Seawater','Average Weighted',2024,1
        pass
    
    global v1,v2,v3
    with cc[0]:
        v1=s.selectbox("Please Enter the Month",[i for i in range(1,13)])
    with cc[1]:
        v2=s.selectbox("Please Enter the Year",[i for i in range(2024,1950,-1)]) 
    with cc[2]:
        v3=s.selectbox("Please enter the type of data",ll)
    
    #if()
    folium_map(aa,v3)
    
    


if __name__=="__main__":
    main()