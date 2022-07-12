import pandas as pd
def result(uid):
    try:
        df_l=pd.read_html(f"http://202.53.11.226:8080/lastudentportal/online/report/onlineResultNewInner.jsp?registerno={uid}&iden=1")

        return df_l[1],df_l[2]
    except:
        return f"No result found for this UID {uid}"

def grade_converter(grade):
    d={'O':10,'A':9,'B':8,'C':7,'D':6,'E':5,'F':0,'-':10}
    return d[grade]

def gpa(uid,token=None):

    try:
        df_l=pd.read_html(f"http://202.53.11.226:8080/lastudentportal/online/report/onlineResultNewInner.jsp?registerno={uid}&iden=1")
        if len(df_l)!=4: return None
        df=df_l[2]
        df.columns = df.iloc[0]
        df = df.drop(0)
        sem=df['SEMESTER'].loc[1]
        df = df[df['SEMESTER']==sem]
        df[['SL.NO.', 'SEMESTER', 'CREDIT']]=df[['SL.NO.', 'SEMESTER', 'CREDIT']].astype('int64')
    except: return None
    df['grade_points']=df['GRADE'].apply(grade_converter)
    gpa=sum(df['CREDIT']*df['grade_points'])/sum(df['CREDIT'])
    if token==1:
        return sem,float(str(gpa)[:4])
    else:
        return [uid,df_l[1][1][0],float(str(gpa)[:4])]

