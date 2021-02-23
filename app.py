import joblib
import streamlit as st


# input_model = open("catboost_model.pkl", "rb")
# classifier = joblib.load(input_model)
# classifier = st.cache(pd.read_csv)("football_data.csv")

def model_loader(filename):
    with open(filename, "rb") as input_model:
        classifier = joblib.load(input_model)
    return classifier


st.cache(model_loader)("catboost_model.pkl")


def time_extractor(time):
    hour = time.hour
    minute = time.minute
    return hour, minute


def departure_time_bin(time):
    hour, _ = time_extractor(time)
    if hour < 6:
        value = 'vem'
        return value
    elif hour >= 6 & hour <= 9:
        value = 'm'
        return value
    elif hour > 9 & hour <= 12:
        value = 'mm'
        return value
    elif hour > 12 & hour <= 15:
        value = 'maf'
        return value
    elif hour > 15 & hour <= 18:
        value = 'af'
        return value
    elif hour > 18 & hour <= 21:
        value = 'n'
        return value
    elif hour > 21 & hour <= 23:
        value = 'nn'
        return value


def feature_creator(time, carrier, destination, origin, month):
    hour, minute = time_extractor(time)
    hour_squared = hour ** 2
    route = origin + destination
    h_carrier = str(hour_squared) + '_' + carrier
    unique_carrier_origin = carrier + "_" + origin
    unique_carrier_destination = carrier + "_" + destination
    m_origin_carrier = str(month) + '_' + unique_carrier_origin
    m_destination_carrier = str(month) + '_' + unique_carrier_destination
    h_destination_carrier = str(hour_squared) + '_' + unique_carrier_destination
    h_origin_carrier = str(hour_squared) + '_' + unique_carrier_origin
    departure_time = departure_time_bin(time)
    departure_route = departure_time + '_' + route

    list_of_features = [minute, departure_route, hour_squared, h_destination_carrier, h_carrier,
                        h_origin_carrier, route, m_origin_carrier, m_destination_carrier]
    return list_of_features


def predict_delay(time, carrier, destination, origin, month):
    """Flight Delay Predictions
    This is using docstrings for specifications.
    ---
    parameters:
      - name: time
        in: query
        type: datetime
        required: true
      - name: carrier
        in: query
        type: str
        required: true
      - name: destination
        in: query
        type: str
        required: true
      - name: origin
        in: query
        type: str
        required: true
      - name: month
        in: query
        type: number
        required: true

    responses:
        200:
            description: The output values

    """
    classifier = model_loader("catboost_model.pkl")
    to_predict = feature_creator(time, carrier, destination, origin, month)
    prediction = float(classifier.predict_proba([to_predict])[:, 1])
    return prediction


def main():
    st.title("Flight Delay Prediction")
    html_temp = """
    <div style="background-color:RebeccaPurple;padding:10px">
    <h2 style="color:white;text-align:center;">Flight Delay Prediction Web App </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    time = st.time_input('Time of Departure')
    carrier = st.selectbox('Flying with', ('AA', 'US', 'XE', 'OO', 'WN', 'NW', 'DL', 'OH', 'AS', 'UA', 'MQ',
                                           'CO', 'EV', 'DH', 'YV', 'F9', 'AQ', 'TZ', 'HP', 'B6', 'FL', 'HA'))
    destination = st.selectbox('Destination Airport', ('ATL', 'PIT', 'RDU', 'DEN', 'MDW', 'MEM', 'PBI', 'MSP', 'ONT',
                                                       'BDL', 'PHX', 'LAS', 'DFW', 'DSM', 'CMH', 'ORF', 'SLC', 'CLT',
                                                       'GSO', 'IAD', 'SMF', 'FLL', 'DAL', 'ORD', 'ITO', 'SAN', 'ROA',
                                                       'LGA', 'SFO', 'GSP', 'SEA', 'DAB', 'SJC', 'LIT', 'LAX', 'OAK',
                                                       'COS', 'OKC', 'GRR', 'JFK', 'BOI', 'MCI', 'BWI', 'BHM', 'CRP',
                                                       'BOS', 'SAT', 'PHL', 'STL', 'CIC', 'AUS', 'IAH', 'COD', 'HNL',
                                                       'RNO', 'BNA', 'TPA', 'MIA', 'EVV', 'PNS', 'EWR', 'RSW', 'ANC',
                                                       'SNA', 'AMA', 'CID', 'DTW', 'DCA', 'LGB', 'MAF', 'MFE', 'BMI',
                                                       'PDX', 'IPL', 'GRB', 'FAR', 'HOU', 'MTJ', 'DRO', 'MLU', 'VPS',
                                                       'TUL', 'CVG', 'SBA', 'PWM', 'IDA', 'MCO', 'ACV', 'CHS', 'BGM',
                                                       'MSY', 'OGG', 'CLE', 'MOB', 'CAK', 'FAY', 'SHV', 'TUS', 'IND',
                                                       'CAE', 'PVD', 'ROC', 'MFR', 'VLD', 'ELP', 'RIC', 'MKE', 'SGF',
                                                       'TYS', 'CHO', 'EGE', 'BIS', 'JAN', 'JAX', 'BUF', 'MSO', 'BGR',
                                                       'CEC', 'ICT', 'MYR', 'ALB', 'LIH', 'SBP', 'AEX', 'GNV', 'SAV',
                                                       'BTM', 'BRO', 'SJU', 'XNA', 'CPR', 'SDF', 'JAC', 'AVL', 'PHF',
                                                       'GPT', 'SYR', 'PSP', 'MHT', 'MRY', 'CLD', 'FAT', 'MSN', 'ISP',
                                                       'BUR', 'PSC', 'MEI', 'LEX', 'LBB', 'GEG', 'LFT', 'OMA', 'ISO',
                                                       'MGM', 'GRK', 'AVP', 'ABQ', 'SRQ', 'BTV', 'FLG', 'BTR', 'MDT',
                                                       'ABI', 'TRI', 'ADQ', 'FSM', 'SMX', 'RST', 'RAP', 'ILM', 'SIT',
                                                       'EKO', 'DBQ', 'CHA', 'BQK', 'BZN', 'MOD', 'MOT', 'MLB', 'TVC',
                                                       'LAN', 'DAY', 'HSV', 'EUG', 'SGU', 'ACT', 'AGS', 'CLL', 'HLN',
                                                       'LNK', 'ASE', 'HRL', 'ATW', 'CMI', 'LWS', 'DHN', 'FNT', 'FLO',
                                                       'RDM', 'TYR', 'KOA', 'FAI', 'OME', 'RDD', 'MCN', 'TLH', 'MQT',
                                                       'AZO', 'FCA', 'CRW', 'TOL', 'HPN', 'FSD', 'FWA', 'SUN', 'LAW',
                                                       'YUM', 'PIA', 'GTF', 'ACY', 'PIH', 'SPS', 'MLI', 'BIL', 'TWF',
                                                       'HTS', 'SBN', 'PFN', 'GJT', 'CSG', 'JNU', 'TXK', 'LRD', 'BQN',
                                                       'CWA', 'SWF', 'GTR', 'BFL', 'OXR', 'KTN', 'PIE', 'SCE', 'PSG',
                                                       'DLH', 'SJT', 'GUC', 'SPI', 'IYK', 'ABY', 'STT', 'ABE', 'GFK',
                                                       'HDN', 'CDV', 'MBS', 'TUP', 'LCH', 'EYW', 'OTZ', 'ADK', 'GGG',
                                                       'VIS', 'GST', 'LYH', 'HVN', 'BRW', 'LSE', 'ERI', 'HKY', 'BET',
                                                       'CDC', 'OAJ', 'WRG', 'ACK', 'DLG', 'YAK', 'AKN', 'TEX', 'STX',
                                                       'SCC', 'APF', 'BPT', 'WYS', 'RFD', 'BLI', 'ILG', 'VCT', 'LWB',
                                                       'PSE'), key='destination')
    origin = st.selectbox('Destination Airport', ('ATL', 'PIT', 'RDU', 'DEN', 'MDW', 'MEM', 'PBI', 'MSP', 'ONT',
                                                  'BDL', 'PHX', 'LAS', 'DFW', 'DSM', 'CMH', 'ORF', 'SLC', 'CLT',
                                                  'GSO', 'IAD', 'SMF', 'FLL', 'DAL', 'ORD', 'ITO', 'SAN', 'ROA',
                                                  'LGA', 'SFO', 'GSP', 'SEA', 'DAB', 'SJC', 'LIT', 'LAX', 'OAK',
                                                  'COS', 'OKC', 'GRR', 'JFK', 'BOI', 'MCI', 'BWI', 'BHM', 'CRP',
                                                  'BOS', 'SAT', 'PHL', 'STL', 'CIC', 'AUS', 'IAH', 'COD', 'HNL',
                                                  'RNO', 'BNA', 'TPA', 'MIA', 'EVV', 'PNS', 'EWR', 'RSW', 'ANC',
                                                  'SNA', 'AMA', 'CID', 'DTW', 'DCA', 'LGB', 'MAF', 'MFE', 'BMI',
                                                  'PDX', 'IPL', 'GRB', 'FAR', 'HOU', 'MTJ', 'DRO', 'MLU', 'VPS',
                                                  'TUL', 'CVG', 'SBA', 'PWM', 'IDA', 'MCO', 'ACV', 'CHS', 'BGM',
                                                  'MSY', 'OGG', 'CLE', 'MOB', 'CAK', 'FAY', 'SHV', 'TUS', 'IND',
                                                  'CAE', 'PVD', 'ROC', 'MFR', 'VLD', 'ELP', 'RIC', 'MKE', 'SGF',
                                                  'TYS', 'CHO', 'EGE', 'BIS', 'JAN', 'JAX', 'BUF', 'MSO', 'BGR',
                                                  'CEC', 'ICT', 'MYR', 'ALB', 'LIH', 'SBP', 'AEX', 'GNV', 'SAV',
                                                  'BTM', 'BRO', 'SJU', 'XNA', 'CPR', 'SDF', 'JAC', 'AVL', 'PHF',
                                                  'GPT', 'SYR', 'PSP', 'MHT', 'MRY', 'CLD', 'FAT', 'MSN', 'ISP',
                                                  'BUR', 'PSC', 'MEI', 'LEX', 'LBB', 'GEG', 'LFT', 'OMA', 'ISO',
                                                  'MGM', 'GRK', 'AVP', 'ABQ', 'SRQ', 'BTV', 'FLG', 'BTR', 'MDT',
                                                  'ABI', 'TRI', 'ADQ', 'FSM', 'SMX', 'RST', 'RAP', 'ILM', 'SIT',
                                                  'EKO', 'DBQ', 'CHA', 'BQK', 'BZN', 'MOD', 'MOT', 'MLB', 'TVC',
                                                  'LAN', 'DAY', 'HSV', 'EUG', 'SGU', 'ACT', 'AGS', 'CLL', 'HLN',
                                                  'LNK', 'ASE', 'HRL', 'ATW', 'CMI', 'LWS', 'DHN', 'FNT', 'FLO',
                                                  'RDM', 'TYR', 'KOA', 'FAI', 'OME', 'RDD', 'MCN', 'TLH', 'MQT',
                                                  'AZO', 'FCA', 'CRW', 'TOL', 'HPN', 'FSD', 'FWA', 'SUN', 'LAW',
                                                  'YUM', 'PIA', 'GTF', 'ACY', 'PIH', 'SPS', 'MLI', 'BIL', 'TWF',
                                                  'HTS', 'SBN', 'PFN', 'GJT', 'CSG', 'JNU', 'TXK', 'LRD', 'BQN',
                                                  'CWA', 'SWF', 'GTR', 'BFL', 'OXR', 'KTN', 'PIE', 'SCE', 'PSG',
                                                  'DLH', 'SJT', 'GUC', 'SPI', 'IYK', 'ABY', 'STT', 'ABE', 'GFK',
                                                  'HDN', 'CDV', 'MBS', 'TUP', 'LCH', 'EYW', 'OTZ', 'ADK', 'GGG',
                                                  'VIS', 'GST', 'LYH', 'HVN', 'BRW', 'LSE', 'ERI', 'HKY', 'BET',
                                                  'CDC', 'OAJ', 'WRG', 'ACK', 'DLG', 'YAK', 'AKN', 'TEX', 'STX',
                                                  'SCC', 'APF', 'BPT', 'WYS', 'RFD', 'BLI', 'ILG', 'VCT', 'LWB',
                                                  'PSE'), key='origin')
    month = st.selectbox('Month of Departure (0: January, 1: February...)',
                         (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))

    if st.button("Predict"):
        result = predict_delay(time, carrier, destination, origin, month)
        st.success('The probability of flight delay is {:.2f}.'.format(result))


if __name__ == '__main__':
    main()
