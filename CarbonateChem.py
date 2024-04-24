import streamlit as s
import numpy as n

pK1=lambda T,s:-43.6977-0.0129037*s+1.364*10**-4*s*s+2885.378/T+7.045159*n.log(T)

pK2=lambda T,s:-452.094+13.142162*s-8.101*10**-4*s*s+21263.61/T+68.483143*n.log(T)+(-581.4428*s+0.259601*s*s)/T-1.967035*s*n.log(T)


def pH(a,b,c):
    rt=-b-n.sqrt(b*b-4*a*c) 
    
    rt=rt/(2*a)
    return -1*n.log10(rt)

def hco3(pK1,co2,pH):
    k1,h=10**(-1*pK1) , 10**(-1*pH)
    return co2*k1/h

def co3(pK1,pK2,co2,pH):
    k1,k2,h=10**(-1*pK1) ,10**(-1*pK2) , 10**(-1*pH)
    return co2*k1*k2/h/h


if __name__=="__main__":
    s.set_page_config(layout="wide") 
    temp=s.slider("Enter the Temperature in Degree Celcius",5,45)
    salt=s.slider("Enter the Salinity in ‰",10,45)
    fug=s.slider("Eneter the fugaciy of CO₂ in ",100,1000)
    dic=s.slider("Enter the value of Dissolved Inorganic Carbon in μM",1000,5000) 

    c=s.columns[2]
    with c[0]:
        c[0].metric("pK1",value=pK1(temp+273.15,salt))
    with c[1]:
        c[1].metric("pK2",value=pK2(temp+273.15,salt)) 

    c=s.columns[3]
    pass