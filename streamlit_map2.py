import streamlit as s
import pandas as p
from streamlit_folium import st_folium,folium_static
import folium
import numpy as n
import branca.colormap as cm
import os

pK1=lambda T,s:-43.6977-0.0129037*s+1.364*10**-4*s*s+2885.378/T+7.045159*n.log(T)

pK2=lambda T,s:-452.094+13.142162*s-8.101*10**-4*s*s+21263.61/T+68.483143*n.log(T)+(-581.4428*s+0.259601*s*s)/T-1.967035*s*n.log(T)

def hco3(pK1,pK2,pH,dic):
    k1,k2,h=10**(-1*pK1) ,10**(-1*pK2) , 10**(-1*pH)
    return dic/(h/k1-1+k2/h)

def co3(pK1,pK2,pH,dic):
    k1,k2,h=10**(-1*pK1) ,10**(-1*pK2) , 10**(-1*pH)
    return dic/(h*h/k1/k2+h/k2+1)

def co2(pK1,pK2,pH,dic):
    k1,k2,h=10**(-1*pK1) ,10**(-1*pK2) , 10**(-1*pH)
    return dic/(1+k1/h+k1*k2/h/h)

def map_create(a,color,v):
    attr=('&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)')
    tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png' 

    if 'm' not in s.session_state or s.session_state.m is None or v3!=s.session_state['type'] or v2!=s.session_state['year'] or v1!=s.session_state['month'] or aa!=s.session_state['kind']:
        m=folium.Map(tiles=tiles,attr=attr,min_lat=-90,max_lat=90,min_lon=-180,max_lon=180,max_bounds=True,zoom_start=3,max_zoom = 9,min_zoom = 2,location=[0,0])
        for i in range(a.shape[0]):
            folium.CircleMarker(location=(a[' LAT'][i],a[' LON'][i]),radius=2.5, color=color(a[v][i]), fill_color =color(a[v][i]),tooltip=round(a[v][i],2), fill_opacity=1).add_to(m)
        color.add_to(m)
        s.session_state.m = m 

        s.session_state['type'],s.session_state['year'],s.session_state['month'],s.session_state['kind']=v3,v2,v1,aa

    return s.session_state.m    



def folium_map(v):
    
   
    df=s.session_state['data'] 
    df=df.round({"pK1_WEIGHTED":2, "pK1_UNWEIGHTED":2, "pK2_WEIGHTED":2, "pK2_UNWEIGHTED":2}) 
    
    if(v=='pK1_WEIGHTED' or v=='pK1_UNWEIGHTED'):
        color=cm.LinearColormap(colors=['white','blue'], vmin=5.5,vmax=6,caption='pK1 Value')
    elif(v=='pK2_WEIGHTED' or v=='pK2_UNWEIGHTED'):
        color=cm.LinearColormap(colors=['white','blue'], vmin=8.5,vmax=9.5,caption='pK2 Value')


    if(v1<10):
        a=df[df.DATE.str.startswith(str(v2)+"-"+"0"+str(v1))]
          
    else:
        a=df[df.DATE.str.startswith(str(v2)+"-"+str(v1))] 
    
    a=a[[' LAT',' LON',v]] 
    a.reset_index(inplace=True,drop=True) 
    m=map_create(a,color,v)
    folium_static(m, width=1500)

def main():
    
    s.title("  Surface Ocean CO₂ Atlas ")
    global aa
    aa=s.selectbox("Kind of data?",['pK1','pK2'])
    cc=s.columns(3)
    ll=['AVERAGE WEIGHTED','AVERAGE UNWEIGHTED']
    if('kind' not in s.session_state or 'type' not in s.session_state or 'year' not in s.session_state or 'month' not in s.session_state or 'data' not in s.session_state):
        s.session_state['kind'],s.session_state['type'],s.session_state['year'],s.session_state['month']='pK1','Average Weighted',2020,1 
        

        fol=""
        df=p.read_csv(os.path.join(fol,"SOCATCO2_0.csv"))[['DATE',' LAT',' LON',' FCO2_AVE_WEIGHTED_YEAR',' FCO2_AVE_UNWTD_YEAR']]
        df1=p.read_csv(os.path.join(fol,"SOCATCO2_1.csv"))[[' SST_AVE_WEIGHTED_YEAR',' SST_AVE_UNWTD_YEAR']]
        df2=p.read_csv(os.path.join(fol,"SOCATCO2_2.csv"))[[' SALINITY_AVE_WEIGHTED_YEAR',' SALINITY_AVE_UNWTD_YEAR']]

        df= p.concat([df, df1], axis=1)  
        df= p.concat([df, df2], axis=1) 
        df=df[df[' SALINITY_AVE_WEIGHTED_YEAR']>0]
        df=df[df[' SALINITY_AVE_UNWTD_YEAR']>0]
        df[' SST_AVE_WEIGHTED_YEAR'],df[' SST_AVE_UNWTD_YEAR']=df[' SST_AVE_WEIGHTED_YEAR']+273.15,df[' SST_AVE_UNWTD_YEAR']+273.15
        df['pK1_WEIGHTED'],df['pK1_UNWEIGHTED']=n.array(map(pK1,df[' SST_AVE_WEIGHTED_YEAR'],df[' SALINITY_AVE_WEIGHTED_YEAR'])),n.array(map(pK1,df[' SST_AVE_UNWTD_YEAR'],df[' SALINITY_AVE_UNWTD_YEAR']))
        df['pK2_WEIGHTED'],df['pK2_UNWEIGHTED']=n.array(map(pK2,df[' SST_AVE_WEIGHTED_YEAR'],df[' SALINITY_AVE_WEIGHTED_YEAR'])),n.array(map(pK2,df[' SST_AVE_UNWTD_YEAR'],df[' SALINITY_AVE_UNWTD_YEAR']))
        
        
        s.session_state['data']=df 

    global v1,v2,v3
    with cc[0]:
        v1=s.selectbox("Please Enter the Month",[i for i in range(1,13)])
        
    with cc[1]:
        v2=s.selectbox("Please Enter the Year",[i for i in range(2024,1950,-1)]) 
    with cc[2]:
        v3=s.selectbox("Please enter the type of data",ll) 
    
    
    folium_map(aa+"_"+v3.split()[-1])


if __name__=="__main__":
    main()
