# To be run by cron
# Please run every Friday
# for example :
# 0 2 * * 5 python3 /path/to/observium_extractor.py
# means run every Friday at 2:00 (maybe ???)

import requests,datetime,requests,csv,pickle,os#,sys
url="https://observium.domain.com/graph.php"
OBSERVIUM_USERNAME="your_observium_username"
OBSERVIUM_PASSWORD="your_observium_password"
GROUP_IDS=[
            "-100xxx3386xxx",   # Test Group Rizal
          ]
TELEGRAM_URL="https://api.telegram.org/bot50xxxxxxx4:xxxxxxxxxxs7R3wkuAo6Lvlplxxxxxxxxxx/sendDocument"

# arguments = sys.argv
# start_date = arguments[1] if len(arguments) > 1 else None
# end_date = arguments[2] if len(arguments) > 2 else None
# csv_filename = arguments[3] if len(arguments) > 3 else None

ids = []
with open('ids.pickle', 'rb') as file:
    ids = pickle.load(file)

def logger(msg: str,topic: str):
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    with open("./logs/"+topic+'log'+datetime.datetime.now().strftime("%d%m%Y")+'.txt','a+',newline='') as f:
        print(datetime.datetime.now().strftime("%d%m%Y %H:%M:%S")+" "+topic+': ['+msg+']')
        writer=csv.writer(f)
        writer.writerow([datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),msg])
    return 

def time_to_unix_epoch(time_string,format="%Y-%m-%d"): 
    return int(datetime.datetime.strptime(time_string,format).timestamp())

def convert_to_m(value_str: str):
    print("Before",value_str)
    unit=value_str[-1].upper()
    value=float(value_str[:-1])
    if unit == 'M': return_value = value
    elif unit == 'K': return_value = value * 0.001
    elif unit == 'G': return_value = value * 1000
    elif unit == 'T': return_value = value * 1000000
    else: return_value = value * 0.000001
    logger("Convert: "+value_str+" -> "+str(return_value), "convert")
    return return_value

def convert_to_g(value_str: str):
    print("before",value_str)
    unit=value_str[-1].upper()
    value=float(value_str[:-1])
    if unit == 'M': return_value = value * 0.001
    elif unit == 'K': return_value = value * 0.000001
    elif unit == 'G': return_value = value
    elif unit == 'T': return_value = value * 1000
    else: return_value = value * 0.000000001
    logger("Convert: "+value_str+" -> "+str(return_value), "convert")
    return return_value

start_date=(datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%d%m%Y") # last 7 days
end_date=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d%m%Y") # last 1 day
start_date_epoch=time_to_unix_epoch(start_date,"%d%m%Y")
end_date_epoch=time_to_unix_epoch(end_date,"%d%m%Y")

# if start_date is None or end_date is None:
#     # manual input
#     print("Enter start date (format: ddmmYYYY or enter to use last 7 days): ")
#     start_date=input()
#     if start_date != "":
#         print("Enter end date (format: ddmmYYYY): ")
#         end_date=input()
#     else:
#         start_date=(datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%d%m%Y") # last 7 days
#         end_date=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d%m%Y") # last 1 day
# start_date_epoch=time_to_unix_epoch(start_date,"%d%m%Y")
# end_date_epoch=time_to_unix_epoch(end_date,"%d%m%Y")

logger("Setting start and end dates","info")
logger("Start date: "+str(start_date)+", epoch: "+str(start_date_epoch),"info")
logger("End date: "+str(end_date)+", epoch: "+str(end_date_epoch),"info")

try:
    data=[]
    for port in ids:
        port_data=requests.get(url=url,
                               params={"timestamp_preset": "lweek",
                                       "type": "port_bits",
                                       "id": port[0],
                                       "from": start_date_epoch,
                                       "to": end_date_epoch,
                                       "format": "json"},
                               auth=(OBSERVIUM_USERNAME,OBSERVIUM_PASSWORD))
        debug_url = url + "?timestamp_preset=lweek&type=port_bits&id=" + str(port[0]) + "&from=" + str(start_date_epoch) + "&to=" + str(end_date_epoch) + "&format=json"
        logger("Accessing "+debug_url,"info")
        try:
            if port_data.status_code == 200:
                title=port[1]
                isp=port[2]
                scraps = [
                    index_this['gprint'] for index_this in port_data.json()['meta']['gprints']
                    if 'gprint' in index_this and any(substring in index_this['gprint'] for substring in ['\\n', '(In', 'Out '])
                ]
                print(scraps)
                nf_percentile_in = "{:.2f}".format(convert_to_m(str(scraps[0]).replace("\\n","").replace(" ","").replace("na","0.00")))
                nf_percentile_out = "{:.2f}".format(convert_to_m(str(scraps[1]).replace("\\n","").replace(" ","").replace("na","0.00")))
                total_in = "{:.2f}".format(convert_to_g(str(scraps[2]).replace("(In","").replace(" ","").replace("na","0.00")))
                total_out = "{:.2f}".format(convert_to_g(str(scraps[3]).replace("Out","").replace(" ","").replace(")\\l","").replace("na","0.00")))
                print(title,isp,nf_percentile_in,nf_percentile_out,total_in,total_out)
                data.append([title,isp,nf_percentile_in,nf_percentile_out,total_in,total_out])
            else: logger("Request failed with status code: "+str(port_data.status_code),"error")
        except Exception as e:
            logger("Request failed or Data does not exist on observium","error")
            logger(str(e),"debug")
    current_time=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if not os.path.exists("./outputs"): os.makedirs("./outputs")
    # if csv_filename == None:
    #     csv_filename=("outputs/"+input("Enter filename or press enter to use default: ")+".csv") or "outputs/output-"+str(current_time)+".csv"
    csv_filename=("outputs/"+"output-"+str(current_time)+".csv")
    with open(csv_filename,mode='w',newline='') as file:
        writer=csv.writer(file)
        writer.writerow(["BU","Uplink","In 95th percentile (M)","Out 95th percentile (M)","Total In (G)","Total Out (G)"])
        writer.writerows(data)
    logger("Data has been saved to "+csv_filename,"info")
    logger("Sending file to telegram group...","info")
    files={'document': open(csv_filename,'rb')}
    for group_id in GROUP_IDS:
        requests.post(TELEGRAM_URL,files=files,data={'chat_id': group_id,'caption': "cron: MRTG Export "+str(datetime.datetime.now().strftime("%Y-%m-%d"))})
        logger("File Sent to "+group_id,"info")
except Exception as e:
    logger("Error: Failed to get data","error")
    logger(str(e),"debug")
