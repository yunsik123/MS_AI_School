import gradio as gr
import requests

cookies = list()
csrf_token = None


def request_history():
    response = requests.get("http://127.0.0.1:8000/v1/openai/messages/",
                            headers={
                                "Cookie": "; ".join(cookies),
                                "X-CSRFToken": csrf_token
                            })

    response_json = response.json()

    return response_json['datas']


def request_sign_in(username, password):
    global cookies
    global csrf_token
    response = requests.post("http://127.0.0.1:8000/v1/users/signin/",
                             json=dict(
                                 username=username,
                                 password=password
                             ))
    status_code = response.status_code

    for key, value in response.cookies.items():
        # "csrftoken=NfuQAGia2zpmbyAhcghEAsJ3iHJASIJf"
        if key == 'csrftoken':
            csrf_token = value
        cookies.append(f"{key}={value}")

    response_json = response.json()
    if status_code == 200:
        return True
    else:
        return False


def request_chatgpt(input_text, pre_message_count):
    global cookies
    global csrf_token
    response = requests.post("http://127.0.0.1:8000/v1/openai/messages/",
                             headers={
                                 "Cookie": "; ".join(cookies),
                                 "X-CSRFToken": csrf_token
                             },
                             json=dict(
                                 message=input_text,
                                 pre_message_count=pre_message_count
                             ))

    if response.status_code == 200:
        response_json = response.json()
        response_text = response_json["data"]
        return response_text
    else:
        return None


def click_sign_in(username, password):
    is_succeed = request_sign_in(username, password)
    if is_succeed:
        datas = request_history()
        return ("로그인에 성공하였습니다.", gr.Textbox(visible=False), gr.Textbox(visible=False), gr.Button(visible=False),
                gr.Button(visible=True), datas)
    else:
        return ("로그인에 실패하였습니다.", gr.Textbox(visible=True), gr.Textbox(visible=True), gr.Button(visible=True),
                gr.Button(visible=False), [])


def click_me():
    global cookies
    response = requests.get("http://127.0.0.1:8000/v1/users/me/", headers={
        "Cookie": "; ".join(cookies)
    })
    response_json = response.json()
    user = response_json.get('user')
    response_text = f"""
        결과 : {response_json.get('message')}
        ### 이메일 : {user.get('username')}\n
        최근 로그인 : {user.get('last_login')}
    """
    return response_text


def click_sign_out():
    global cookies
    response = requests.get("http://127.0.0.1:8000/v1/users/signout/", headers={
        "Cookie": "; ".join(cookies)
    })
    status_code = response.status_code
    response_json = response.json()
    if status_code == 200:
        cookies.clear()
        return "로그아웃 하였습니다.", gr.Textbox(visible=True), gr.Textbox(visible=True), gr.Button(visible=True), gr.Button(visible=False)
    else:
        return "로그아웃 실패", gr.Textbox(visible=False), gr.Textbox(visible=False), gr.Button(visible=False), gr.Button(visible=True)


def click_send(input_text, histories, pre_message_count):
    response_text = request_chatgpt(input_text, pre_message_count)
    if response_text:
        histories.append((input_text, response_text))
    return "", histories


# request_sign_in("fimtrus@gmail.com", "1234")
# request_chatgpt("남해여행지 알려줘 ")

with gr.Blocks() as demo:

    # 전체 컨테이너
    with gr.Row():
        # GPT 관련
        with gr.Column(scale=5):
            chatbot = gr.Chatbot(label="GPT")

            with gr.Row():
                input_textbox = gr.Textbox(label="메시지 입력", placeholder="질문을 입력하세요.", scale=5)
                pre_message_count_textbox = gr.Textbox(label="이전 메시지 수", value="10", placeholder="포함시킬 메시지 수")
                send_button = gr.Button("전송", scale=1)

        # 로그인 관련
        with gr.Column(scale=1):
            username_textbox = gr.Textbox(label="아이디", placeholder="아이디를 입력하세요.", value='fimtrus@gmail.com')
            password_textbox = gr.Textbox(label="패스워드", placeholder="패스워드를 입력하세요.", value='1234', type='password')
            sign_in_button = gr.Button("로그인")
            sign_out_button = gr.Button("로그아웃", visible=False)
            me_button = gr.Button("내 정보 가져오기")
            result_text = gr.Markdown(label="결과")

    sign_in_button.click(fn=click_sign_in, inputs=[username_textbox, password_textbox],
                         outputs=[result_text, username_textbox, password_textbox, sign_in_button, sign_out_button, chatbot])
    sign_out_button.click(fn=click_sign_out, inputs=[],
                          outputs=[result_text, username_textbox, password_textbox, sign_in_button, sign_out_button])
    me_button.click(fn=click_me, inputs=[], outputs=[result_text])
    send_button.click(fn=click_send, inputs=[input_textbox, chatbot, pre_message_count_textbox], outputs=[input_textbox, chatbot])

demo.launch(server_name="0.0.0.0", server_port=7860)
