def get_data(delta, name, exchange, interval, continuous = False, oi = False):
    to_date = datetime.datetime.now().date()
    from_date = to_date - datetime.timedelta(days = delta)
    #print(to_date, from_date)
    desired_token = kite.ltp([exchange + name])[exchange + name]['instrument_token']
    #print(token)
    data = kite.historical_data(instrument_token=desired_token, from_date=from_date, to_date=to_date, interval=interval, 
                               continuous=continuous, oi=oi)
    df_data = pd.DataFrame(data)
    return df_data

def write_log(message):
    file_name = './Log_files/10_24MA_buyside '+str(datetime.datetime.now().date())+'.txt'
    file = open(file_name, 'a+')
    file.write(str(datetime.datetime.now())+'  '+message + '\n')
    file.close()
    
def get_atm_nifty(ltp):
    nifty_step_size = 50
    mod = math.fmod(ltp, nifty_step_size)
    if mod >= 25:
        atm_value = ltp - mod + nifty_step_size
    else:
        atm_value = ltp - mod
    #print('Nifty ATM Value: ', int(atm_value))
    return int(atm_value)

def get_atm_bank_nifty(ltp):
    bnf_step_size = 100
    mod = math.fmod(ltp, bnf_step_size)
    if mod > 50:
        atm_value = int((ltp//100)*100)+100
    else:
        atm_value = int(ltp//100)*100
    print('Bnf ATM Value: ', atm_value)
    

def fetch_ltp(kite, exchange, name):
    '''
    Function takes kite object, name of exchange and name of instruments
    and returns the ltp
    '''
    instrument_name = exchange+name
    
    ltp = kite.ltp(instrument_name)[instrument_name]['last_price']
    return ltp


def send_to_telegram(message):
    apiToken = '6253697343:AAH5uSvqP_1WeM68sroSAnbbLs9csg03ek0'
    chatID = '-1001899646463'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(f"Error sending telegram messages: {e}")    


def get_atm_nf_bnf(ltp, name):
    '''
    This function returns the ATM value for both Nifty 50 and Bank nifty. 
    Along with ltp, this ask for NIFTY 50 or NIFTY BANK
    '''
    if name == 'NIFTY 50':
        nifty_step_size = 50
        mod = math.fmod(ltp, nifty_step_size)
        if mod >= 25:
            atm_value = ltp - mod + nifty_step_size
        else:
            atm_value = ltp - mod
        #print('Nifty ATM Value: ', int(atm_value))
        return int(atm_value)
    
    if name == 'NIFTY BANK':
        bnf_step_size = 100
        mod = math.fmod(ltp, bnf_step_size)
        if mod > 50:
            atm_value = int((ltp//100)*100)+100
        else:
            atm_value = int(ltp//100)*100
        #print('Bnf ATM Value: ', atm_value)
        return int(atm_value)
    
def get_monthly_itm_symbol(df_instruments, ltp, ce_pe, name, step_size = 50): 
    '''
    This function returns the monthly ITM value based on LTP. 
    Upto 2nd last expiry, this returns current monthly expiry, from last expiry date 
    on-wards, this returns next month expiry. 
    '''
    monthly_itm_symbol_name = ''
    date_format = '%Y-%m-%d'
    months_representation = {1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', :'OCT', 11:'NOV', 12:'DEC'}
    today = datetime.datetime.now().strftime(date_format)
    #today = '2023-09-21'
    #print('Today: ', today)
    all_expiry_dates = sorted(list(set(df_instruments[(df_instruments['exchange'] == 'NFO') & (df_instruments['name'] == 'NIFTY')]['expiry'].values)))
    dates = [datetime.datetime.strptime(x, date_format) for x in all_expiry_dates]
    dates = sorted(dates)
    sorted_dates = [datetime.datetime.strftime(x, date_format) for x in dates]
    #print('Sorted dates: ', sorted_dates)

    # Take first 6 dates and find this months's all expiry dates
    current_month = int(today.split('-')[1])
    #print('Current month', current_month)

    # Collect all expiry dates of this month
    this_month_expiry = []
    for x in sorted_dates[:]:
        #print(x.split('-')[1])
        if int(x.split('-')[1]) == current_month:
            this_month_expiry.append(x)
    #this_month_expiry = this_month_expiry[-2:]
    #print('This month expiry: ', this_month_expiry)
    
    next_month_expiry = 0
    if len(this_month_expiry) < 2:
        next_month_expiry = 1
    if len(this_month_expiry) == 2:
        if datetime.datetime.strptime(today, date_format).date() >= datetime.datetime.strptime(this_month_expiry[0], date_format).date():
            next_month_expiry = 1
    #print('Next month exp value: ', next_month_expiry)
    #print('Length of current expiry days: ', len(this_month_expiry))
    expiry_date = ''
    if next_month_expiry == 0:
        expiry_month = months_representation[current_month]
        expiry_date = this_month_expiry[0]
        #print('Expiry month: ', expiry_month, expiry_date)
    if next_month_expiry == 1:
        expiry_month = months_representation[int(sorted_dates[len(this_month_expiry):][0].split('-')[1])]
        expiry_date = sorted_dates[len(this_month_expiry):][0]
        #print('Expiry month: ', expiry_month, expiry_date)
    year = str(expiry_date).split('-')[0][2:]
    #print('Year: ', year)
    atm_value = get_atm_nf_bnf(ltp, name)
    if name == 'NIFTY 50':
        if ce_pe == 'CE':
            itm_value = atm_value - 1*step_size
            monthly_itm_symbol_name = 'NIFTY'+year+expiry_month+str(itm_value)+'CE'
        if ce_pe == 'PE':
            itm_value = atm_value + 1*step_size
            monthly_itm_symbol_name = 'NIFTY'+year+expiry_month+str(itm_value)+'PE'
            
    if name == 'NIFTY BANK':
        if ce_pe == 'CE':
            itm_value = atm_value - 1*step_size
            monthly_itm_symbol_name = 'BANKNIFTY'+year+expiry_month+str(itm_value)+'CE'
        if ce_pe == 'PE':
            itm_value = atm_value + 1*step_size
            monthly_itm_symbol_name = 'BANKNIFTY'+year+expiry_month+str(itm_value)+'PE'
        
    #print('Monthly itm symbol name: ', monthly_itm_symbol_name)
    #print('LTP: ', fetch_ltp(kite, 'NFO:', monthly_itm_symbol_name))
    return monthly_itm_symbol_name


def get_nifty_itm_symbol_updated(df_instruments, ltp, ce_pe, step_size = 50):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    #today = '2023-08-03'
    expiry_day = False
    expiry_date = None
    weekly_expiry, monthly_expiry = False, False
    months_representation = {1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
    
    all_expiry_dates = sorted(list(set(df_instruments[(df_instruments['exchange'] == 'NFO') & (df_instruments['name'] == 'NIFTY')]['expiry'].values)))
    dates = [datetime.datetime.strptime(x, '%Y-%m-%d') for x in all_expiry_dates]
    dates = sorted(dates)
    sorted_dates = [datetime.datetime.strftime(x, "%Y-%m-%d") for x in dates]
    #print('Sorted dates: ', sorted_dates)

    # Take first 6 dates and find this months's all expiry dates
    current_month = today.split('-')[1]
    #print('Current month', current_month)

    # Collect all expiry date for this month
    this_month_expiry = []
    for x in sorted_dates[:]:
        #print(x.split('-')[1])
        if x.split('-')[1] == current_month:
            this_month_expiry.append(x)
    #print('This month expiry: ', this_month_expiry)
    
    # Check if today is an expiry day or not
    if today == this_month_expiry[0]:
        expiry_day = True
        #print(f"Today {today} is an expiry day")
    else:
        #print(f"Today {today} is not an expiry day")
        expiry_date = this_month_expiry[0]
        if len(this_month_expiry) == 1:
            monthly_expiry = True
            #print('This is a monthly expiry')


    # this means, today is the monthly expiry date, so select next weekly expiry
    if (expiry_day) and (len(this_month_expiry) == 1):   
        expiry_date = sorted_dates[1]
        #print('Selected Expiry date: ', expiry_date)

    # if today is an expiry day and next expiry is a monthly expiry
    elif ( (expiry_day) and (len(this_month_expiry) == 2) ):
        expiry_date = this_month_expiry[-1]
        #print('Selected Expiry date: ', expiry_date, ' and its a monthly expiry')
        monthly_expiry = True

    # else today is a weekly expiry and just paas the next weekly expiry
    elif ((expiry_day) and (len(this_month_expiry) > 2)):
        expiry_date = this_month_expiry[1]
        #print('Selected Expiry date: ', expiry_date)

    # Else just paas the current expiry date    
    else:
        expiry_date = this_month_expiry[0]
        #print('Selected Expiry date: ', expiry_date)
    
    if monthly_expiry:
        month = int(this_month_expiry[0].split('-')[1])
        #print('Month: ', month)
        nifty_symbol_name = 'NIFTY'+expiry_date.split('-')[0][-2:]+months_representation[month]
        #print('Nifty symbol name: ', nifty_symbol_name)
    else:
        nifty_symbol_name = 'NIFTY'+expiry_date.split('-')[0][-2:]+str(int(expiry_date.split('-')[1]))+expiry_date.split('-')[2]
        #print('Nifty symbol name: ', nifty_symbol_name)

    atm_value = get_atm_nifty(ltp)
    if ce_pe == 'PE':
        itm_value = str(int(atm_value)+step_size)
        nifty_symbol_name = nifty_symbol_name+itm_value+'PE'
    if ce_pe == 'CE':
        itm_value = str(int(atm_value)-step_size)
        nifty_symbol_name = nifty_symbol_name+itm_value+'CE'
    #print('Nifty itm symbol: ', nifty_symbol_name)
    return nifty_symbol_name
