import streamlit as st
import pandas as pd
import requests


st.set_page_config('Invoices Generation',
                    page_icon= ':factory:',
                    layout= 'wide'
                    )

st.title(':orange[Invoices] Generation :factory:')


@st.cache_data
def get_bearer_token(user,password):
    user = user
    psswrd = password

    headers = {
    'authority': 'api.nabis.com',
    'accept': '*/*',
    'accept-language': 'es-ES,es;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://app.getnabis.com',
    'referer': 'https://app.getnabis.com/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }


    json_data = {
    'operationName': 'SignIn',
    'variables': {
        'input': {
            'email': user,
            'password': psswrd,
            },
        },
        'query': 'mutation SignIn($input: LoginUserInput!) {\n  loginUser(input: $input) {\n    token\n    user {\n      ...userFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment userFragment on User {\n  id\n  email\n  firstName\n  lastName\n  address1\n  address2\n  city\n  state\n  zip\n  phone\n  profilePicture\n  isAdmin\n  isDriver\n  driversLicense\n  __typename\n}\n',
    }   

    response = requests.post('https://api.nabis.com/graphql/admin', headers=headers, json=json_data)

    bearer_token = response.json()
    token = bearer_token['data']['loginUser']['token']
    user = bearer_token['data']['loginUser']['user']['id']
    
    return token,user



@st.cache_data
def create_headers(token):

    headers = {
    'authority': 'api.nabis.com',
    'accept': '*/*',
    'accept-language': 'es-ES,es;q=0.9',
    'authorization': 'Bearer '+ token,
    'content-type': 'application/json',
    'origin': 'https://app.getnabis.com',
    'referer': 'https://app.getnabis.com/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    return headers



@st.cache_data
def load_dataframe(file):
    """
    Loads the uploaded file into a Pandas DataFrame.
    """

    file_extension = file.name.split(".")[-1]
    
    if file_extension == "csv":
        df = pd.read_csv(file)

    elif file_extension == "xlsx":
        df = pd.read_excel(file)

    return df



def all_admin_orders_accounting_page(order_number,headers):
    json_data = {
        "operationName": "AllAdminOrdersAccountingPage",
        "variables": {
            "pageInfo": {
                "numItemsPerPage": 25,
                "orderBy": [
                    {
                        "attribute": "date",
                        "order": "DESC",
                    },
                    {
                        "attribute": "createdAt",
                        "order": "DESC",
                    },
                ],
                "page": 1,
            },
            "search": order_number,
            "status": [
                "DELIVERED",
                "DELIVERED_WITH_EDITS",
                "DELAYED",
                "REJECTED",
                "ATTEMPTED",
            ],
        },
        "query": "query AllAdminOrdersAccountingPage($organizationId: ID, $search: String, $status: [OrderStatusEnum], $paymentStatus: [OrderPaymentStatusEnum], $disputeStatus: [OrderDisputeStatus!], $start: DateTime, $end: DateTime, $paymentProcessedAtStart: DateTime, $paymentProcessedAtEnd: DateTime, $paymentSentAtStart: DateTime, $paymentSentAtEnd: DateTime, $paidAtStart: DateTime, $paidAtEnd: DateTime, $irn: String, $orderFees: [String], $pageInfo: PageInfoInput, $collectionStatus: [BrandFeesCollectionCollectionStatusEnum]) {\n  viewer {\n    allAdminAccountingOrders(organizationId: $organizationId, search: $search, status: $status, irn: $irn, paymentStatus: $paymentStatus, disputeStatus: $disputeStatus, start: $start, end: $end, paymentProcessedAtStart: $paymentProcessedAtStart, paymentProcessedAtEnd: $paymentProcessedAtEnd, paymentSentAtStart: $paymentSentAtStart, paymentSentAtEnd: $paymentSentAtEnd, paidAtStart: $paidAtStart, paidAtEnd: $paidAtEnd, orderFees: $orderFees, pageInfo: $pageInfo, collectionStatus: $collectionStatus) {\n      results {\n        id\n        adminNotes\n        action\n        accountingNotes\n        ACHAmountCollectedRetailer\n        ACHAmountPaidBrand\n        internalNotes\n        createdAt\n        creditMemo\n        date\n        daysTillPaymentDue\n        distroFees\n        dueToBrand\n        discount\n        surcharge\n        edited\n        exciseTax\n        exciseTaxCollected\n        extraFees\n        gmv\n        gmvCollected\n        wholesaleGmv\n        priceDifference\n        irn\n        manifestGDriveFileId\n        apSummaryGDriveFileId\n        apSummaryS3FileLink\n        invoicesS3FileLink\n        packingListS3FileLink\n        mustPayPreviousBalance\n        nabisDiscount\n        name\n        notes\n        number\n        isSampleDemo\n        parentOrder {\n          id\n          totalGMV\n          shouldRemoveMinFee\n          __typename\n        }\n        paymentStatus\n        paymentTermsRequestStatus\n        hasSingleQBInvoice\n        hasMultiQBInvoices\n        hasMultiAQBInvoice\n        hasMultiBQBInvoice\n        hasMultiCQBInvoice\n        hasMultiC1QBInvoice\n        hasMultiC2QBInvoice\n        isAfterQuickbooksDeploy\n        lastPaymentTermOrderChange {\n          submitter {\n            id\n            firstName\n            lastName\n            isAdmin\n            __typename\n          }\n          id\n          description\n          createdAt\n          __typename\n        }\n        orderFees {\n          ...feeOrderFragment\n          __typename\n        }\n        pricingFee\n        pricingPercentage\n        basePricing {\n          pricingFee\n          pricingPercentage\n          __typename\n        }\n        status\n        creator {\n          id\n          email\n          firstName\n          lastName\n          __typename\n        }\n        licensedLocation {\n          ...licensedLocationFragment\n          __typename\n        }\n        organization {\n          id\n          doingBusinessAs\n          alias\n          name\n          owner {\n            id\n            email\n            firstName\n            lastName\n            __typename\n          }\n          __typename\n        }\n        site {\n          id\n          name\n          address1\n          address2\n          city\n          state\n          zip\n          pocName\n          pocPhoneNumber\n          pocEmail\n          licensedLocationId\n          licensedLocation {\n            id\n            __typename\n          }\n          __typename\n        }\n        paidAt\n        paymentMethod\n        remittedAt\n        factorStatus\n        calculateMoneyValues {\n          subtotal\n          orderDiscount\n          lineItemDiscounts\n          totalExciseTax\n          totalBalance\n          discountedSubtotal\n          taxRate\n          netOffTotal\n          __typename\n        }\n        nabisManifestNotes\n        referrer\n        orderFiles {\n          ...orderFileFragment\n          __typename\n        }\n        writeOffReasons\n        paymentSentAt\n        processingAt\n        ...lastAccountingOrderIssues\n        brandFeesCollection {\n          ...BrandFeesCollectionFragment\n          user {\n            id\n            firstName\n            lastName\n            email\n            __typename\n          }\n          __typename\n        }\n        willAutoRegenerateInvoices\n        __typename\n      }\n      pageInfo {\n        page\n        numItemsPerPage\n        orderBy {\n          attribute\n          order\n          __typename\n        }\n        totalNumItems\n        totalNumPages\n        __typename\n      }\n      nextOrders {\n        number\n        date\n        id\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment feeOrderFragment on OrderFee {\n  id\n  feeId\n  feeName\n  feePrice\n  feeNotes\n  createdBy {\n    firstName\n    lastName\n    email\n    __typename\n  }\n  fee {\n    ...feeFragment\n    __typename\n  }\n  __typename\n}\n\nfragment feeFragment on Fee {\n  id\n  basePrice\n  description\n  name\n  feeType\n  groupTag\n  startDate\n  endDate\n  isArchived\n  __typename\n}\n\nfragment licensedLocationFragment on LicensedLocation {\n  id\n  name\n  address1\n  address2\n  city\n  state\n  zip\n  siteCategory\n  lat\n  lng\n  billingAddress1\n  billingAddress2\n  billingAddressCity\n  billingAddressState\n  billingAddressZip\n  warehouseId\n  isArchived\n  doingBusinessAs\n  noExciseTax\n  phoneNumber\n  printCoas\n  hoursBusiness\n  hoursDelivery\n  deliveryByApptOnly\n  specialProtocol\n  schedulingSoftwareRequired\n  schedulingSoftwareLink\n  centralizedPurchasingNotes\n  payByCheck\n  collectionNotes\n  deliveryNotes\n  collect1PocFirstName\n  collect1PocLastName\n  collect1PocTitle\n  collect1PocNumber\n  collect1PocEmail\n  collect1PocAllowsText\n  collect1PreferredContactMethod\n  collect2PocFirstName\n  collect2PocLastName\n  collect2PocTitle\n  collect2PocNumber\n  collect2PocEmail\n  collect2PocAllowsText\n  collect2PreferredContactMethod\n  delivery1PocFirstName\n  delivery1PocLastName\n  delivery1PocTitle\n  delivery1PocNumber\n  delivery1PocEmail\n  delivery1PocAllowsText\n  delivery1PreferredContactMethod\n  delivery2PocFirstName\n  delivery2PocLastName\n  delivery2PocTitle\n  delivery2PocNumber\n  delivery2PocEmail\n  delivery2PocAllowsText\n  delivery2PreferredContactMethod\n  unmaskedId\n  qualitativeRating\n  creditRating\n  trustLevelNabis\n  trustLevelInEffect\n  isOnNabisTracker\n  locationNotes\n  infoplus\n  w9Link\n  taxIdentificationNumber\n  sellerPermitLink\n  nabisMaxTerms\n  __typename\n}\n\nfragment orderFileFragment on OrderFile {\n  id\n  type\n  s3Link\n  mimeType\n  notes\n  createdAt\n  updatedAt\n  orderId\n  __typename\n}\n\nfragment lastAccountingOrderIssues on AccountingOrder {\n  lastDispute {\n    id\n    reason\n    initiatedNotes\n    initiatedAt\n    issueType\n    resolvedAt\n    __typename\n  }\n  lastNonpayment {\n    id\n    reason\n    initiatedNotes\n    initiatedAt\n    issueType\n    __typename\n  }\n  __typename\n}\n\nfragment BrandFeesCollectionFragment on BrandFeesCollection {\n  id\n  createdAt\n  updatedAt\n  deletedAt\n  isArchived\n  submitterId\n  collectionStatus\n  collectionStatusUpdatedAt\n  notes\n  __typename\n}\n",
    }

    response = requests.post(
        "https://api.getnabis.com/graphql/admin", headers=headers, json=json_data
    )
    return response



def regenerate_inv_C1(qb_invoice_data,headers):
    json_data = {
    'operationName': 'GenerateQuickbooksInvoice',
    'variables': {
        'input': {
            "orderId": qb_invoice_data["orderId"],
            "pricingPercentage": qb_invoice_data["pricingPercentage"],
            "pricingFee": qb_invoice_data["pricingFee"],
            "nabisDiscount": qb_invoice_data["nabisDiscount"],
            'invoiceTypesToGenerate': [
                'C1',
            ],
        },
    },
    'query': 'mutation GenerateQuickbooksInvoice($input: GenerateQuickbooksInvoiceInput!) {\n  generateQuickbooksInvoice(input: $input) {\n    orderId\n    __typename\n  }\n}\n',
    }

    response = requests.post('https://api.getnabis.com/graphql/admin', headers=headers, json=json_data)
    return response



def delete_inv(qb_invoice_data,inv_to_delete,headers):
    json_data = {
    'operationName': 'DeleteQuickbooksInvoice',
    'variables': {
        'input': {
            'orderId': qb_invoice_data["orderId"],
            'invoiceTypesToDelete': [
                inv_to_delete,
            ],
        },
    },
    'query': 'mutation DeleteQuickbooksInvoice($input: DeleteQuickbooksInvoiceInput!) {\n  deleteQuickbooksInvoice(input: $input) {\n    orderId\n    __typename\n  }\n}\n',
    }

    response = requests.post('https://api.getnabis.com/graphql/admin', headers=headers, json=json_data)
    return response


def process_generate_or_delete(list_orders,instruction,headers):

    if instruction == 'Generate C1':

        for order in list_orders:
            order_number = order
            order_data = all_admin_orders_accounting_page(order_number,headers)
            order_data = order_data.json()
        
            qb_invoice_data = {
                "orderId": order_data['data']['viewer']['allAdminAccountingOrders']['results'][0]['id'],
                "pricingPercentage": order_data['data']['viewer']['allAdminAccountingOrders']['results'][0]['pricingPercentage'],
                "pricingFee": order_data['data']['viewer']['allAdminAccountingOrders']['results'][0]['pricingFee'],
                "nabisDiscount": order_data['data']['viewer']['allAdminAccountingOrders']['results'][0]['nabisDiscount'],
            }

            
            regenerate_inv_C1(qb_invoice_data,headers)
            st.write(f'{order} Generated')


    elif instruction == 'Delete C2':    
        for order in list_orders:
            order_number = order
            order_data = all_admin_orders_accounting_page(order_number,headers)
            order_data = order_data.json()

            qb_invoice_data = {
                "orderId": order_data['data']['viewer']['allAdminAccountingOrders']['results'][0]['id'],
                "pricingPercentage": order_data['data']['viewer']['allAdminAccountingOrders']['results'][0]['pricingPercentage'],
                "pricingFee": order_data['data']['viewer']['allAdminAccountingOrders']['results'][0]['pricingFee'],
                "nabisDiscount": order_data['data']['viewer']['allAdminAccountingOrders']['results'][0]['nabisDiscount'],
            }

        
        
        delete_inv(qb_invoice_data,"C2",headers)
        
        st.write(f'{order} Deleted')



with st.form(key='log_in',):

    email = st.text_input('email:'),
    password_st = st.text_input('Password:',type='password')

    submitted = st.form_submit_button('Log in')

try:
    if submitted:
        st.write('Credentials Saved')


        user = email[0]
        password = password_st
        token,user_id = get_bearer_token(user,password)
        headers = create_headers(token)
        st.session_state['headers'] = headers
        
except:
    st.warning('Incorrect Email or Password, Try again')



if submitted:
    st.session_state['initialize'] = 'initialize'


if "initialize" not in st.session_state:
    st.write('Enter Your Credentials')
else:

    st.subheader('Instructions')

    st.write('Upload file with the list of the invoices you want to process')
    st.write('Be sure the file contains :red[headers] called "Orders" otherwise the tool will not recognize the column')
    st.write('The invoice numbers must be :red[only] digits and do not include letters')
    st.write('Use .csv or .xlsx files only')

    invs_list = st.file_uploader('Upload list of invoices')

    if invs_list is not None:
        df = load_dataframe(invs_list)

        st.write(f'Total number of orders to process is: {df.shape[0]}')

        st.warning("🚨 Ensure invoices does not have any previous application applied")

        selection = st.selectbox('Select Transaction',options=['Generate C1', 'Delete C2'])

        if selection == "Generate C1":
            submit_button = st.button('Generate Invoice C1',key='GenerateC1')
            if submit_button:
                list_invoices = df['Orders'].astype('str').to_list()
                # list_invoices
                process_generate_or_delete(list_invoices,selection,st.session_state['headers'])

        elif selection == 'Delete C2':
            submit_button = st.button('Delete Invoice C2',key='DeleteC2')
            if submit_button:

                list_invoices = df['Orders'].astype('str').to_list()
                # list_invoices
                process_generate_or_delete(list_invoices,selection,st.session_state['headers'])