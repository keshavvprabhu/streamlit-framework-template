import streamlit as st
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

NS = "urn:iso:std:iso:20022:tech:xsd:acmt.007.001.05"
ET.register_namespace('', NS)

def prettify(elem: ET.Element) -> str:
    rough = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent='  ', encoding='utf-8').decode('utf-8')

st.set_page_config(page_title='ACMT XML Generator', page_icon='📤', layout='wide')

st.title('📤 ACMT 007 Account Opening Request - XML Generator')
st.write('Fill the form below to create an `acmt.007.001.05` XML message')

with st.form('acmt_form'):
    st.subheader('Message References')
    msg_id = st.text_input('Message Id', value=f'MSG{datetime.utcnow().strftime("%Y%m%d%H%M%S")}')
    msg_cre_dt = st.text_input('Message Creation DateTime (ISO)', value=datetime.utcnow().isoformat() + 'Z')
    prc_id = st.text_input('Processing Id (optional)', value='')
    prc_cre_dt = st.text_input('Processing Creation DateTime (optional)', value='')

    st.subheader('Account Information')
    use_iban = st.radio('Account identifier type', ('IBAN', 'Other'), index=0, horizontal=True)
    if use_iban == 'IBAN':
        acct_iban = st.text_input('IBAN', value='DE89370400440532013000')
        acct_other = ''
    else:
        acct_iban = ''
        acct_other = st.text_input('Other Account Id', value='')

    acct_name = st.text_input('Account Name', value='Business Operating Account')
    acct_status = st.selectbox('Account Status', ['ENAB', 'DISA', 'DELE', 'FORM'], index=0)
    acct_type = st.text_input('Account Type Code (Tp/Cd)', value='CHAR')
    currency = st.text_input('Currency (3-letter)', value='EUR')
    mnthly_pmt = st.text_input('Monthly Payment Value (optional)', value='')
    mnthly_rcvd = st.text_input('Monthly Received Value (optional)', value='')
    mnthly_tx_nb = st.text_input('Monthly Tx Number (optional)', value='')
    avrg_bal = st.text_input('Average Balance (optional)', value='')
    acct_purp = st.text_input('Account Purpose (AcctPurp)', value='Business Operations Account')

    st.subheader('Contract Details')
    go_live = st.date_input('Target Go Live Date')
    urgency = st.checkbox('Urgency Flag', value=False)

    st.subheader('Account Servicer (Bank)')
    bicfi = st.text_input('BICFI', value='DEUTDEDD')

    st.subheader('Organisation (Account owner)')
    org_anybic = st.text_input('Org AnyBIC (optional)', value='DEUTDEDD')
    org_lei = st.text_input('Org LEI (optional)', value='5493001KJTIIGC8Y1R12')
    org_name = st.text_input('Organisation Name', value='ABC Corporation Ltd')
    adr_line1 = st.text_input('Address Line 1', value='100 Business Street')
    adr_line2 = st.text_input('Address Line 2 (optional)', value='Suite 200')
    town = st.text_input('Town/City', value='New York')
    postcode = st.text_input('Postcode', value='10001')
    country = st.text_input('Country (2-letter)', value='US')
    contact_name = st.text_input('Contact Name', value='John Smith')
    contact_email = st.text_input('Contact Email', value='john.smith@abccorp.com')

    submitted = st.form_submit_button('Generate XML')

if submitted:
    # Build XML
    doc = ET.Element(ET.QName(NS, 'Document'))
    acct_req = ET.SubElement(doc, ET.QName(NS, 'AcctOpngReq'))

    # Refs
    refs = ET.SubElement(acct_req, ET.QName(NS, 'Refs'))
    msg = ET.SubElement(refs, ET.QName(NS, 'MsgId'))
    ET.SubElement(msg, ET.QName(NS, 'Id')).text = msg_id
    ET.SubElement(msg, ET.QName(NS, 'CreDtTm')).text = msg_cre_dt
    if prc_id or prc_cre_dt:
        prc = ET.SubElement(refs, ET.QName(NS, 'PrcId'))
        if prc_id:
            ET.SubElement(prc, ET.QName(NS, 'Id')).text = prc_id
        if prc_cre_dt:
            ET.SubElement(prc, ET.QName(NS, 'CreDtTm')).text = prc_cre_dt

    # Account
    acct = ET.SubElement(acct_req, ET.QName(NS, 'Acct'))
    id_el = ET.SubElement(acct, ET.QName(NS, 'Id'))
    if acct_iban:
        ET.SubElement(id_el, ET.QName(NS, 'IBAN')).text = acct_iban
    else:
        ET.SubElement(id_el, ET.QName(NS, 'Othr')).text = acct_other

    if acct_name:
        ET.SubElement(acct, ET.QName(NS, 'Nm')).text = acct_name
    if acct_status:
        ET.SubElement(acct, ET.QName(NS, 'Sts')).text = acct_status
    if acct_type:
        tp = ET.SubElement(acct, ET.QName(NS, 'Tp'))
        ET.SubElement(tp, ET.QName(NS, 'Cd')).text = acct_type
    if currency:
        ET.SubElement(acct, ET.QName(NS, 'Ccy')).text = currency
    if mnthly_pmt:
        ET.SubElement(acct, ET.QName(NS, 'MnthlyPmtVal')).text = mnthly_pmt
    if mnthly_rcvd:
        ET.SubElement(acct, ET.QName(NS, 'MnthlyRcvdVal')).text = mnthly_rcvd
    if mnthly_tx_nb:
        ET.SubElement(acct, ET.QName(NS, 'MnthlyTxNb')).text = mnthly_tx_nb
    if avrg_bal:
        ET.SubElement(acct, ET.QName(NS, 'AvrgBal')).text = avrg_bal
    if acct_purp:
        ET.SubElement(acct, ET.QName(NS, 'AcctPurp')).text = acct_purp

    # Contract Dts
    ctr = ET.SubElement(acct_req, ET.QName(NS, 'CtrctDts'))
    ET.SubElement(ctr, ET.QName(NS, 'TrgtGoLiveDt')).text = go_live.isoformat()
    ET.SubElement(ctr, ET.QName(NS, 'UrgcyFlg')).text = 'true' if urgency else 'false'

    # Account Servicer
    acctsvcr = ET.SubElement(acct_req, ET.QName(NS, 'AcctSvcrId'))
    fin = ET.SubElement(acctsvcr, ET.QName(NS, 'FinInstnId'))
    if bicfi:
        ET.SubElement(fin, ET.QName(NS, 'BICFI')).text = bicfi

    # Org
    org = ET.SubElement(acct_req, ET.QName(NS, 'Org'))
    orgid = ET.SubElement(org, ET.QName(NS, 'OrgnStnId'))
    if org_anybic:
        ET.SubElement(orgid, ET.QName(NS, 'AnyBIC')).text = org_anybic
    if org_lei:
        ET.SubElement(orgid, ET.QName(NS, 'LEI')).text = org_lei
    if org_name:
        ET.SubElement(org, ET.QName(NS, 'Nm')).text = org_name

    adr = ET.SubElement(org, ET.QName(NS, 'Adr'))
    tp = ET.SubElement(adr, ET.QName(NS, 'Tp'))
    ET.SubElement(tp, ET.QName(NS, 'Cd')).text = 'ADDR'
    if adr_line1:
        ET.SubElement(adr, ET.QName(NS, 'AdrLine')).text = adr_line1
    if adr_line2:
        ET.SubElement(adr, ET.QName(NS, 'AdrLine')).text = adr_line2
    if postcode:
        ET.SubElement(adr, ET.QName(NS, 'PstCd')).text = postcode
    if town:
        ET.SubElement(adr, ET.QName(NS, 'TwnNm')).text = town
    if country:
        ET.SubElement(adr, ET.QName(NS, 'Ctry')).text = country

    ctc = ET.SubElement(org, ET.QName(NS, 'CtctDtls'))
    if contact_name:
        ET.SubElement(ctc, ET.QName(NS, 'Nm')).text = contact_name
    if contact_email:
        ET.SubElement(ctc, ET.QName(NS, 'EmailAdr')).text = contact_email

    xml_str = prettify(doc)

    st.subheader('Generated XML Preview')
    st.code(xml_str, language='xml')

    # Download
    st.download_button('Download XML', data=xml_str, file_name='acmt_acct_opening_req_v05.xml', mime='application/xml')

    # Optionally save to workspace
    if st.button('Save to workspace file'):
        path = 'sample_generated_acmt007_v05.xml'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        st.success(f'Saved to {path}')
