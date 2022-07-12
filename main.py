import streamlit as st
from streamlit_option_menu import option_menu
import concurrent.futures
import pandas as pd
from result import result,gpa
from css import css

#pay='''<form><script src="https://checkout.razorpay.com/v1/payment-button.js" data-payment_button_id="pl_JqtXEdNSna9bQw" async> </script> </form>'''

st.set_page_config(page_title="Loyola Academy Results", page_icon="icon.png", layout="wide", initial_sidebar_state="expanded", menu_items=None)

selection=option_menu(None, [ "Result","Ranking","CGPA Calculator","Suggestions"],menu_icon="cast",default_index=0,orientation="horizontal")

if selection=='Suggestions':
    st.header("Please provide your suggestions here:")
    st.write("https://forms.gle/5hHaFHC1zs3XHMDo9")

if selection=="Result":
        st.subheader("Enter your UID")
        txt=st.text_input("",max_chars=12)
        if st.button("Get Result"):
            if len(txt)==12 and txt.isdigit() and txt[:4]=='1117':
                try:
                    int(txt)
                    details_df,result_df=result(txt)
                    details_df.columns,result_df.columns = details_df.iloc[0],result_df.iloc[0]
                    details_df,result_df = details_df[1:],result_df[1:]
                    
                    st.markdown(css(), unsafe_allow_html=True)
                    st.table(details_df)
                    st.table(result_df)
                    #st.markdown(pay, unsafe_allow_html=True)
                    try:
                        int(txt)
                        s,g=gpa(txt,1)
                        st.subheader(f"Your SGPA is {g} in {s} semester")
                    except:
                        st.error("Couldn't calculate your GPA")
                except:
                    st.error("Enter a valid UID")
                
            else:
                st.error("Enter a valid UID")

               

        
    
if selection=="CGPA Calculator":
    st.title("CGPA Calculator")

    sem=st.slider("Select your semester for which you want to calculate your CGPA",min_value=1,max_value=6,value=1)
    first_sgpa,second_sgpa,third_sgpa,fourth_sgpa,fifth_sgpa,sixth_sgpa=0,0,0,0,0,0
    if sem>=1:
        first_sgpa=st.number_input("Enter your 1 sem SGPA:",min_value=0.0,max_value=10.0,value=0.0)
        if sem>=2:
            second_sgpa=st.number_input("Enter your 2 sem SGPA:",min_value=0.0,max_value=10.0,value=0.0)
            if sem>=3:
                third_sgpa=st.number_input("Enter your 3 sem SGPA:",min_value=0.0,max_value=10.0,value=0.0)
                if sem>=4:
                    fourth_sgpa=st.number_input("Enter your 4 sem SGPA:",min_value=0.0,max_value=10.0,value=0.0)
                    if sem>=5:
                        fifth_sgpa=st.number_input("Enter your 5 sem SGPA:",min_value=0.0,max_value=10.0,value=0.0)
                        if sem>=6:
                            sixth_sgpa=st.number_input("Enter your 6 sem SGPA:",min_value=0.0,max_value=10.0,value=0.0)

    if st.button('Calculate'):
        sum=first_sgpa+second_sgpa+third_sgpa+fourth_sgpa+fifth_sgpa+sixth_sgpa
        st.subheader(f"Your CGPA is {str(sum/sem)[:4]} (approx)")
    
    

if selection=="Ranking":
    uid=st.text_input("Enter your UID",max_chars=12)
    
    if st.button('GO'):
        if len(uid)==12 and uid.isdigit() and uid.startswith('1117'):
            try:                     
                roll=int(uid[-3:])
                zero=int(uid)-roll
                start=zero+1
                end=zero+130
            
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    res=list(executor.map(gpa,range(start,end+1)))
                res=[i for i in res if i!=None]
                final=pd.DataFrame(res,columns=['UID','NAME','GPA'])
                final['RANK']=round(final['GPA'].rank(ascending=False,method='dense'))
                final['GPA']=final['GPA'].apply(lambda x: str(x)[:4])
                final["RANK"]=final["RANK"].astype(int)
                final=final.set_index('RANK').sort_index()
                final.reset_index(inplace=True)
                index=final[final['UID']==int(uid)].index.values
                if len(index)==0:
                    index=None
                else:
                    index=index[0]+1
                st.markdown(css(index), unsafe_allow_html=True)
                st.table(final)
                #st.markdown(pay, unsafe_allow_html=True)
            except:
                st.error("Enter valid UIDs")

        else:
            st.error("Enter a valid UID")
        
