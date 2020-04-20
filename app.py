import os
from flask import Flask
from flask import request, redirect
# $env:FLASK_ENV="development"

#Site 사용 가능 회원 목록
members = [
    {"id": "ksi", "pw": "1004"},
    {"id": "guest", "pw": "1111"},
]

app = Flask(__name__, static_folder="static")

#공통페이지 출력
def get_template(filename):
    with open('views/' + filename, 'r', encoding="utf-8") as f:
        template = f.read()
        
    return template


#매매일지 출력
def get_list():
    log_temp = "<li style='text-align: center'><a href='/{0}'>{0}</a></li>"
    log = [e for e in os.listdir('content') if e[0] != '.']
    return "\n".join([log_temp.format(m) for m in log])

@app.route("/relax")
def relax():
    title = 'Relax room'
    template = get_template('relax.html')
    content = "휴식 공간 :D"
    logs = get_list()

    return template.format(title, content, logs)

    

#메인페이지 출력
@app.route("/main")
def index():
    #querystring을 사용한 GET
    id = request.args.get('id', '')
    template = get_template('main.html')
    title = 'Trading Dairy -' + id
    content = "Daily Trading Logs"
    logs = get_list()
    return template.format(title, content, logs)
    
'''    
얼렛 띄우기
    javascript = """
       alert("Hello \\nHow are you?");
    """
    return template.format(title, content, logs, javascript)


#인덱스 출력
@app.route("/")
def index():
    id = request.args.get('id', '')
    template = get_template('main.html')
    title = 'Trading Dairy -' + id
    content = "Daily Trading Logs"
    logs = get_list()
    
    return template.format(title, content, logs)

'''


#매매일지 세부출력
@app.route("/<title>")
def html(title):
    template = get_template('template.html')
    logs = get_list()
    
    with open(f'content/{title}', 'r') as f:
        content = f.read()
    
    return template.format(title, content, logs)

#로그인 페이지 출력
@app.route("/", methods = ['GET', 'POST'])
def login():
    template = get_template('login.html')
    logs = get_list()

#    print("*" * 100)
 #   print(request.method)

    if request.method == 'GET':
        return template.format("", logs)
    
    elif request.method == 'POST':
        m = [e for e in members if e['id'] == request.form['id']]
        if len(m) == 0:
            return template.format("<p>회원이 아닙니다.</p>", logs)
        
        if request.form['pw'] != m[0]['pw']:
            return template.format("<p>패스워드를 확인해 주세요</p>", logs)
        #querystring을 사용한 GET
        return redirect("/main?id=" + m[0]['id'])
    
#매매일지 생성 페이지 출력
@app.route("/create", methods = ['GET', 'POST'])
def create():
    template = get_template('create.html')
    logs = get_list()
    
    if request.method == 'GET':
        return template.format('', logs)
    #유저에게 받은 값을 file로 저장
    elif request.method == 'POST':
        with open(f'content/{request.form["title"]}', 'w') as f:
            f.write(request.form['desc'])
            
    return redirect('/main')

'''
Update 구현은 실패 ㅠㅠ
@app.route('/update/<path>', methods=['get', 'post'])
def update(path):
    title, message = "Update", ""
    logs = get_list()
    with open('update.html', 'r') as f:
        update = f.read()
    
    if request.method == 'GET':
        with open(f"content/{path}", 'r') as f:
            content = f.read()
        return update.format(title, message, menu, path, content)
    else:
        with open(f"content/{request.form['title']}", 'w') as f:
            f.write(request.form['description'])
        return redirect(f"/{request.form['title']}")
    
'''

#매매일지 삭제
@app.route("/delete/<title>")
def delete(title):

    log = [e for e in os.listdir('content') if e[0] != '.']
    #if log.count(title) > 0: // string으로 들어오면 다른 type으로? 예상치 못한 data? visual code???
    #지울 file이 있는지 조회
    if title in log: 
        os.remove(f"content/{title}")
        return redirect("/main")
    else:
        return redirect("/main")