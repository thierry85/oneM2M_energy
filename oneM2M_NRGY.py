#!/usr/bin/python
##############################################################################
# Goal: oneM2M requests burst for energy test
# contributor:
# Thierry Monteil (thierry.monteil@irit.fr)
#
# Based on simple_om2m.py created by:
#   Ahmad Abbas (ahmad.abbas@eglobalmark.com)
#   Thierry Monteil (thierry.monteil@irit.fr)
#
# licence: common creative - Attribution 4.0 International (CC BY 4.0)
#############################################################################

import sys
import requests
import json
import random
import time
#ACME
CSE_URL_ACME="http://192.168.1.28:8081/~/id-in/cse-in"
#CSE_URL_ACME="http://192.168.1.28:8081/~/id-mn/cse-mn"
ORIGIN_ACME="CAdmin"

#MOBIUS
CSE_URL_MOBIUS="http://192.168.1.28:7579/Mobius"
ORIGIN_MOBIUS="Torigin"

#OM2M
CSE_URL_OM2M="http://192.168.1.28:8080/~/in-cse/in-name"
#CSE_URL_OM2M="http://192.168.1.28:8080/~/mn-cse"
ORIGIN_OM2M="admin:admin"

HTTP_SERVEUR="http://192.168.1.242:9999"
NUM_ARG=len(sys.argv)
COMMAND=sys.argv[0]
DEBUG_RESPONSE=0
DEBUG_TEST=1


def handleResponse(r):
    if DEBUG_RESPONSE ==1 :
        print (r.status_code)
        print (r.headers)
        print (r.text)

def createAE(origin,CSEurl, STACK,api_value,rn_value):
    payload = '{ \
        "m2m:ae": { \
        "api": "'+api_value+'", \
        "srv":["3"],\
        "rr": true,\
        "rn": "'+rn_value+'"\
        } \
    }'
    if (STACK == "OM2M"):
        _headers =   {'X-M2M-Origin': '','X-M2M-RI': 'req1','X-M2M-RVI': '3','Content-Type': 'application/json;ty=2','Accept': 'application/json'}

    else:
        _headers =   {'X-M2M-Origin': origin,'X-M2M-RI': 'req1','X-M2M-RVI': '3','Content-Type': 'application/json;ty=2','Accept': 'application/json'}

    json.dumps(json.loads(payload,strict=False), indent=4)
    r = requests.post(CSEurl.strip(),data=payload,headers=_headers)
    handleResponse(r)
    return r;
############################
###    Delete an <AE>    ###
############################
def deleteAE(origin, CSEurl,api_value,rn_value):
    payload = ''
    _headers =   {'X-M2M-Origin': origin ,'X-M2M-RI': 'req1', 'X-M2M-RVI': '3','Content-Type': 'application/json'}
    r = requests.delete((CSEurl+'/'+rn_value).strip(),headers=_headers)
    handleResponse(r)
    return r;

###############################
###	Create a <Container>	###
###############################
def createContainer(origin,AEurl,rn_value):
	payload = '{ \
	    "m2m:cnt": { \
            "rn": "'+rn_value+'" \
	    } \
	}'
	_headers =   {'X-M2M-Origin': origin,'X-M2M-RI': 'req1', 'X-M2M-RVI': '3','Content-Type': 'application/json;ty=3'}
	json.dumps(json.loads(payload,strict=False), indent=4)
	r = requests.post(AEurl.strip(),data=payload,headers=_headers)
	handleResponse(r)
	return r;

###################################
###    Delete an <Container>    ###
###################################
def deleteContainer(origin,CSEurl,api_value,rn_value):
    payload = ''
    _headers =   {'X-M2M-Origin': origin,'X-M2M-RI': 'req1', 'X-M2M-RVI': '3','Content-Type': 'application/json'}
    r = requests.delete((CSEurl+'/'+rn_value).strip(),headers=_headers)
    handleResponse(r)
    return r;
    
###############################################################
###	Create a <ContentInstance> with mandatory attributes	###
###############################################################
def createContentInstance(origin,CONurl,con_value):

	payload = '{ \
	    "m2m:cin": { \
	    "con": "'+str(con_value)+'" \
	    } \
	}'
	_headers =   {'X-M2M-Origin': origin,'X-M2M-RI': 'req1', 'X-M2M-RVI': '3','Content-Type': 'application/json;ty=4'}
	json.dumps(json.loads(payload,strict=False), indent=4)
	r = requests.post(CONurl.strip(),data=payload,headers=_headers)
	handleResponse(r)
	return r;

#######################################
###	Get latest <ContentInstance>	###
#######################################
def getContentInstanceLatest(origin,CONurl):
    _headers =   {'X-M2M-Origin': origin,'X-M2M-RI': 'req1', 'X-M2M-RVI': '3','Accept': 'application/json'}
    r = requests.get(CONurl.strip(),headers=_headers)
    handleResponse(r)
    return r;

##########################
##    Create <ACP>     ###
##########################
def createACP(origin,url,rn_value,pv_acor_value,pv_acop_value):
    payload = '{ "m2m:acp": {\
        "rn": "'+rn_value+'",\
          "pv": {\
            "acr": [ {\
              "acor": ["'+pv_acor_value+'"],\
              "acop": "'+pv_acop_value+'"\
            }]\
          },\
          "pvs": {\
            "acr": [ {\
              "acor": ["'+pv_acor_value+'"],\
              "acop": "'+pv_acop_value+'"\
            }]\
          }\
       }\
    }'
    _headers =   {'X-M2M-Origin': origin,'X-M2M-RI': 'req1', 'X-M2M-RVI': '3','Content-Type': 'application/json;ty=1'}
    json.dumps(json.loads(payload,strict=False),indent=4)
    r = requests.post(url.strip(),data=payload,headers=_headers)
    handleResponse(r);
    return r;


###################################
###    Delete an <ACP>    ###
###################################
def deleteACP(origin,CSEurl,api_value,rn_value):
    payload = ''
    _headers =   {'X-M2M-Origin': origin,'X-M2M-RI': 'req1', 'X-M2M-RVI': '3','Content-Type': 'application/json'}
    r = requests.delete((CSEurl+'/'+rn_value).strip(),headers=_headers)
    handleResponse(r)
    return r;


        
###################################
###    Delete an <SUB>    ###
###################################
def deleteSUB(origin,CSEurl,api_value,rn_value):
    payload = ''
    _headers =   {'X-M2M-Origin': origin,'X-M2M-RI': 'req1', 'X-M2M-RVI': '3','Content-Type': 'application/json'}
    r = requests.delete((CSEurl+'/'+rn_value).strip(),headers=_headers)
    handleResponse(r)
    return r;
    
##################################
### Create a subscritpion      ###
##################################
def createSUB(origin,CONurl,rn_value,nu_value):
    payload = '{ \
        "m2m:sub": { \
            "rn": "'+rn_value+'", \
            "enc": {\
                "net": [1,3]  \
            } ,\
            "nu": ["'+nu_value+'"],\
            "su": "'+nu_value+'"\
        } \
    }'
    _headers =   {'X-M2M-Origin': origin,'X-M2M-RI': 'req1', 'X-M2M-RVI': '3','Content-Type': 'application/json;ty=23'}
    json.dumps(json.loads(payload,strict=False),indent=4)
    r = requests.post(CONurl.strip(),data=payload,headers=_headers)
    handleResponse(r)
    return r;

################################################################################
### burst of "val" creation of AE and Delete after a sleep of "dort" seconds ###
################################################################################
def Test_AE(origin,CSE_URL,STACK,val, dort):
    for i in range(val):
       createAE(origin+str(i),CSE_URL, STACK, "NEnergy.company.com", "energy_AE"+str(i))
    print("end creation")
    time.sleep(dort)
    for i in range(val):
        if (STACK == "OM2M"):
            deleteAE(origin,CSE_URL, "NEnergy.company.com", "energy_AE"+str(i))
        else:
            deleteAE(origin+str(i),CSE_URL, "NEnergy.company.com", "energy_AE"+str(i))
      
#######################################################################################
### burst of "val" creation of container and Delete after a sleep of "dort" seconds ###
#######################################################################################
def Test_CNT(origin,CSE_URL,STACK,val, dort):
    createAE(origin+"0",CSE_URL,STACK, "NEnergy.company.com", "energy_AE_testCNT")
    for i in range(val):
        createContainer(origin,CSE_URL+"/energy_AE_testCNT", "energy_CNT"+str(i))
    print("end creation")
    time.sleep(dort)
    for i in range(val):
        deleteContainer(origin,CSE_URL+"/energy_AE_testCNT", "NEnergy.company.com", "energy_CNT"+str(i))
    if (STACK == "OM2M"):
        deleteAE(origin,CSE_URL, "NEnergy.company.com", "energy_AE_testCNT")
    else:
        deleteAE(origin+"0",CSE_URL, "NEnergy.company.com", "energy_AE_testCNT")
 ################################################################################
 ### burst of "val" creation of content instance and Delete after a sleep of "dort" seconds ###
 ################################################################################
def Test_CIN(origin,CSE_URL,STACK,val, dort):
    createAE(origin+"0",CSE_URL,STACK, "NEnergy.company.com", "energy_AE_testCIN")
    createContainer(origin,CSE_URL+"/energy_AE_testCIN", "energy_CNT")
    for i in range(val):
        createContentInstance(origin,CSE_URL+"/energy_AE_testCIN/energy_CNT", i)
    print("end creation")
    time.sleep(dort)
    deleteContainer(origin,CSE_URL+"/energy_AE_testCIN", "NEnergy.company.com", "energy_CNT")
    if (STACK == "OM2M"):
        deleteAE(origin,CSE_URL, "NEnergy.company.com", "energy_AE_testCIN")
    else:
        deleteAE(origin+"0",CSE_URL, "NEnergy.company.com", "energy_AE_testCIN")
        
################################################################################
### burst of "val" creation of content instance, get last value and Delete after a sleep of "dort" seconds ###
################################################################################
def Test_LAST(origin,CSE_URL,STACK,val, dort):
    createAE(origin+"0",CSE_URL,STACK, "NEnergy.company.com", "energy_AE_testCIN")
    createContainer(origin,CSE_URL+"/energy_AE_testCIN", "energy_CNT")
    createContentInstance(origin,CSE_URL+"/energy_AE_testCIN/energy_CNT", 0)
    for i in range(val):
        getContentInstanceLatest(origin,CSE_URL+"/energy_AE_testCIN/energy_CNT")
    print("end last")
    time.sleep(dort)
    deleteContainer(origin,CSE_URL+"/energy_AE_testCIN", "NEnergy.company.com", "energy_CNT")
    if (STACK == "OM2M"):
        deleteAE(origin,CSE_URL, "NEnergy.company.com", "energy_AE_testCIN")
    else:
        deleteAE(origin+"0",CSE_URL, "NEnergy.company.com", "energy_AE_testCIN")

################################################################################
### burst of "val" creation of content instance, get last value and Delete after a sleep of "dort" seconds ###
################################################################################
def Test_CIN_LAST(origin,CSE_URL,STACK,val, dort):
    createAE(origin+"0",CSE_URL,STACK, "NEnergy.company.com", "energy_AE_testCIN")
    createContainer(origin,CSE_URL+"/energy_AE_testCIN", "energy_CNT")
    for i in range(val):
        createContentInstance(origin,CSE_URL+"/energy_AE_testCIN/energy_CNT", i)
        getContentInstanceLatest(origin,CSE_URL+"/energy_AE_testCIN/energy_CNT")
    print("end creation")
    time.sleep(dort)
    deleteContainer(origin,CSE_URL+"/energy_AE_testCIN", "NEnergy.company.com", "energy_CNT")
    if (STACK == "OM2M"):
        deleteAE(origin,CSE_URL, "NEnergy.company.com", "energy_AE_testCIN")
    else:
        deleteAE(origin+"0",CSE_URL, "NEnergy.company.com", "energy_AE_testCIN")


################################################################################
### burst of "val" creation of ACP Delete after a sleep of "dort" seconds ###
################################################################################
def Test_ACP(origin,CSE_URL,STACK, val, dort):
    for i in range(val):
        createACP(origin,CSE_URL,"TestACP"+str(i), origin, "63")
    print("end creation")
    time.sleep(dort)
    for i in range(val):
       deleteACP(origin,CSE_URL, "NEnergy.company.com", "TestACP"+str(i))
        
        
        
################################################################################
### burst of "val" creation of subscription after a sleep of "dort" seconds ###
################################################################################
def Test_SUB(origin,CSE_URL,STACK,val, dort):
    createAE(origin+"0",CSE_URL,STACK, "NEnergy.company.com", "energy_AE_testSUB")
    createContainer(origin,CSE_URL+"/energy_AE_testSUB", "energy_CNT")
    for i in range(val):
        createSUB(origin,CSE_URL+"/energy_AE_testSUB"+"/energy_CNT","energy_SUB"+str(i),HTTP_SERVEUR)
    print("end creation")
    time.sleep(dort)
    for i in range(val):
        deleteSUB(origin,CSE_URL+"/energy_AE_testSUB"+"/energy_CNT", "NEnergy.company.com", "energy_SUB"+str(i))
    deleteContainer(origin,CSE_URL+"/energy_AE_testSUB", "NEnergy.company.com", "energy_CNT")
    if (STACK == "OM2M"):
        deleteAE(origin,CSE_URL, "NEnergy.company.com", "energy_AE_testSUB")
    else:
        deleteAE(origin+"0",CSE_URL, "NEnergy.company.com", "energy_AE_testSUB")

################################################################################
### burst of "val" creation of subscription and post CIN after a sleep of "dort" seconds ###
################################################################################
def Test_SUB_CIN(origin,CSE_URL,STACK,val, dort):
    createAE(origin+"0",CSE_URL,STACK, "NEnergy.company.com", "energy_AE_testSUB")
    createContainer(origin,CSE_URL+"/energy_AE_testSUB", "energy_CNT")
    for i in range(val):
        createSUB(origin,CSE_URL+"/energy_AE_testSUB"+"/energy_CNT","energy_SUB"+str(i),HTTP_SERVEUR)
    print("end creation sub")
    time.sleep(dort)
    for i in range(val):
        createContentInstance(origin,CSE_URL+"/energy_AE_testSUB/energy_CNT", i)
    print("end creation cin")
    time.sleep(dort)
    for i in range(val):
        deleteSUB(origin,CSE_URL+"/energy_AE_testSUB"+"/energy_CNT", "NEnergy.company.com", "energy_SUB"+str(i))
    deleteContainer(origin,CSE_URL+"/energy_AE_testSUB", "NEnergy.company.com", "energy_CNT")
    if (STACK == "OM2M"):
        deleteAE(origin,CSE_URL, "NEnergy.company.com", "energy_AE_testSUB")
    else:
        deleteAE(origin+"0",CSE_URL, "NEnergy.company.com", "energy_AE_testSUB")


#########################################
### run a test on a specific resource ###
#########################################
def main():

    if NUM_ARG==7:
        step=int(sys.argv[2])
        maxburst=int(sys.argv[3])
        dodo=int(sys.argv[4])
        DODO=int(sys.argv[5])
        STACK=sys.argv[6]
        if STACK== "OM2M":
            CSE_URL=CSE_URL_OM2M
            ORIGIN=ORIGIN_OM2M
        elif STACK== "ACME":
            CSE_URL=CSE_URL_ACME
            ORIGIN=ORIGIN_ACME
        elif STACK== "MOBIUS":
            CSE_URL=CSE_URL_MOBIUS
            ORIGIN=ORIGIN_MOBIUS
        else :
            print(" unknow stack")
            exit(0)
        for i in range(maxburst):
            if DEBUG_TEST==1:
                print("burst of "+sys.argv[1]+" creation: "+str(step*(i+1)))
            if sys.argv[1]=="AE":
                Test_AE(ORIGIN,CSE_URL,STACK,(i+1)*step,dodo)
            elif sys.argv[1]=="CNT":
                Test_CNT(ORIGIN,CSE_URL,STACK,(i+1)*step,dodo)
            elif sys.argv[1]=="CIN":
                Test_CIN(ORIGIN,CSE_URL,STACK,(i+1)*step,dodo)
            elif sys.argv[1]=="LAST":
                Test_LAST(ORIGIN,CSE_URL,STACK,(i+1)*step,dodo)
            elif sys.argv[1]=="ACP":
                Test_ACP(ORIGIN,CSE_URL,STACK,(i+1)*step,dodo)
            elif sys.argv[1]=="SUB":
                Test_SUB(ORIGIN,CSE_URL,STACK,(i+1)*100,dodo)
            elif sys.argv[1]=="SUBCIN":
                Test_SUB_CIN(ORIGIN,CSE_URL,STACK,(i+1)*100,dodo)
            else :
                print("unknown command")
                print ('Usage: '+COMMAND+' AE/CNT/CIN/LAST/ACP/SUB/SUBCIN [call per burst][X number of burst] [sleep between two requests in a burst] [sleep between two bursts] [OM2M/ACME/MOBIUS]')
                exit(0)
            if DEBUG_TEST==1:
                print("fin du burst of "+sys.argv[1]+" creation: ")
            time.sleep(DODO)
    else:
        print ('Usage: '+COMMAND+' AE/CNT/CIN/LAST/ACP/SUB/SUBCIN [call per burst][X number of burst] [sleep between create and delete in a burst] [sleep between two bursts] [OM2M/ACME/MOBIUS] ')
 
        		
if __name__ == "__main__":
    main()
