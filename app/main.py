import wolframalpha
from fastapi import FastAPI, UploadFile, File, Form
from urllib.parse import quote, quote_plus
from PIL import Image
import io
import base64
import requests

# Thay thế "YOUR_APP_ID" bằng App ID của bạn
app_id = "UYEJGU-445YE86LRU"

app = FastAPI()
# Tạo một đối tượng client WolframAlpha
client = wolframalpha.Client(app_id)

def query_wolfram_alpha(query):
    try:
        # Gửi truy vấn đến Wolfram|Alpha
        res = client.query(query)

        result = {
            'success': res['@success'],
            'error': res['@error'],
            'pods': []
        }

        # Xử lý kết quả trả về
        if res['@success'] == True:
            # Lấy ra các kết quả
            pods = res['pod']
            for pod in pods:
                pod_data = {
                    'title': pod['@title'],
                    'subpod': []
                }

                # Xử lý nội dung của pod
                if 'subpod' in pod:
                    subpod = pod['subpod']

                    # Lấy ra nội dung văn bản
                    if 'plaintext' in subpod:
                        content = subpod['plaintext']
                        pod_data['subpod'].append({'plaintext': content})

                    # Lấy ra hình ảnh
                    if 'img' in subpod:
                        img_url = subpod['img']['@src']
                        pod_data['subpod'].append({'image_url': img_url})

                result['pods'].append(pod_data)

        return result

    except Exception as e:
        return str(e)


def OCR_math(image_base64, base64 = False):
    url = "https://www.mathway.com/OCR"
    if base64:
        payload = f'imageData={quote_plus(image_base64)}&culture=en-US'
    else:
        payload = f'imageData=data%3Aimage%2Fpng%3Bbase64%2C{quote_plus(image_base64)}'
    headers = {
      'authority': 'www.mathway.com',
      'accept': '*/*',
      'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
      'content-type': 'application/x-www-form-urlencoded',
      'cookie': 'Mathway.LastSubject=Algebra; Mathway.IncomingCulture=vi-VN; Mathway.Culture=vi; Mathway.Location=VN; Mathway.GDPR=2; al_cell=main-1-control; sbm_a_b_test=1-control; sbm_country=SG; usprivacy=1YNY; OptanonConsent=isIABGlobal=false&datestamp=Wed+Jul+12+2023+09%3A19%3A15+GMT%2B0700+(Gi%E1%BB%9D+%C4%90%C3%B4ng+D%C6%B0%C6%A1ng)&version=6.13.0&hosts=&consentId=333771c0-ee63-4a29-90e8-d2ea1bb26545&interactionCount=0&landingPath=https%3A%2F%2Fwww.mathway.com%2FAlgebra&groups=snc%3A1%2Cfnc%3A1%2Cprf%3A1%2CSPD_BG%3A1%2Ctrg%3A1%2Cgoog%3A1; language=en_US; amazon-pay-connectedAuth=connectedAuth_general; Mathway.AnonUserId=1012226550; CVID=23b8a824-2394-4a53-863e-0f67e5812f0b; local_fallback_mcid=01751425693313454595680239651081208261; s_ecid=MCMID|01751425693313454595680239651081208261; mcid=01751425693313454595680239651081208261; _pbjs_userid_consent_data=3524755945110770; _pubcid=ffcbcb33-c40d-4745-bad4-a20d255fb644; CSID=1689128354502; _sdsat_mathwayAuthState=logged%20out; ab.storage.sessionId.b283d3f6-78a7-451c-8b93-d98cdb32f9f1=%7B%22g%22%3A%2293b6e9d9-ba51-864a-4ca6-d0ca52ac9f48%22%2C%22e%22%3A1689130156272%2C%22c%22%3A1689128356271%2C%22l%22%3A1689128356272%7D; ab.storage.deviceId.b283d3f6-78a7-451c-8b93-d98cdb32f9f1=%7B%22g%22%3A%2246f52eb1-d902-339a-3f65-8b41bc05905e%22%2C%22c%22%3A1689128356273%2C%22l%22%3A1689128356273%7D; apay-session-set=mqK0x2ojWHG2dKK5CvSk85I%2FzveYMWarGpkX8M2Yl6OQNFwZiePxVfdy6xljRpg%3D; _awl=2.1689128356.5-f14d02294c0b08d1eabff5d15f65f421-6763652d617369612d6561737431-0; _lr_geo_location=VN; __gads=ID=e9a8a32ce2307ad5:T=1689128357:RT=1689128357:S=ALNI_MZyzUmgMHYPXExnzmK7zUKE5tA4Rw; __gpi=UID=00000c1ff6916743:T=1689128357:RT=1689128357:S=ALNI_Mb_mcvkgwu2u4d7cGYyGXwGTk8WRQ; _cc_id=55a7febf6e0289de88eab6d4c0067b5d; panoramaId_expiry=1689214758289; cto_bundle=RCwtjF9ubXV0SW1uWFlad0h5dmpZQ25yZVBTV3NZbEk2VEhZTFNSTkZoNFd4Y0JKRTRaalpKR0tteW5mMWJBT3h2MDN5OE8lMkJEbTg4bFB1dXl1YmhNemZJMkJHV0wyN1FrdTdsOGc0b0FaMmlLclpVUm5aMWNFNXB5N1FEMyUyRnh6azZrVU01Rm1ER3dGeEMxNktFWVdMbWlCWVglMkJ0bzlFTzBoZnhtb2lqJTJGbyUyRjVHdWY3Y084RTRpQUY3dGJWdDRLb0V1OFdz; _lr_retry_request=true; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%22828923a6-0bc2-4d37-9bd9-0a9062cfa4f6%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222023-06-12T02%3A19%3A21%22%7D; _fbp=fb.1.1689128366971.1788561453; _scid=2fe4a465-e812-4d09-b38b-dc2ababdc58b; _scid_r=2fe4a465-e812-4d09-b38b-dc2ababdc58b; IR_gbd=mathway.com; IR_14422=1689128366994%7C0%7C1689128366994%7C%7C; _gcl_au=1.1.1179213552.1689128367; _sctr=1%7C1689094800000; _lr_sampling_rate=100',
      'origin': 'https://www.mathway.com',
      'referer': 'https://www.mathway.com/Algebra',
      'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
      'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        ocr_result = response.json()
        if ocr_result['AsciiMath']:
            # AsciiMath được trả về
            asciimath = ocr_result['AsciiMath']
            return {'OCRMath': asciimath}
        else:
            # Không có AsciiMath được trả về
            return {'error': 'Không tìm thấy AsciiMath trong kết quả OCR.'}
    else:
        # Lỗi trong quá trình gửi yêu cầu
        return {'error': f"Lỗi {response.status_code}: {response.text}"}


@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Math Solver API."}


@app.get("/mathSolver")
def query_api(textInput: str):
    decoded_query = quote_plus(textInput)
    result = query_wolfram_alpha(decoded_query)
    return result


@app.post("/mathSolver")
def query_api(base64input: str = Form(...)):
    OCRMath = OCR_math(base64input, True)
    result = query_wolfram_alpha(OCRMath['OCRMath'])
    return result

@app.post("/mathSolver")
def query_api(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(file.file.read()))
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    OCRMath = OCR_math(image_base64)
    result = query_wolfram_alpha(OCRMath['OCRMath'])
    return result

@app.post("/ocrmath")
def query_api(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(file.file.read()))
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    OCRMath = OCR_math(image_base64)
    return OCRMath