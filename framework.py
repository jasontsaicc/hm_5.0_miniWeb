"""web框架的職責專門負責處理動態資源請求"""
import time
import pymysql

# 路由列表
route_list = [
    #("/index.html",index)]
]

# 定義帶有參數的裝飾器
def route(path):
    # 裝飾器
    def decorator(fluc):
        # 當執行裝飾器時就需要把路由添加到路由列表中
        # 當裝飾函數時只需要添加一次路由即可
        route_list.append((path, fluc))
        def inner():
            result = fluc()
            return result
        return inner
    return decorator

# 獲取首頁數據
@route("/index.html")
def index():
    # 狀態信息
    status = "200 OK"
    #響應頭信息
    response_header = [("server", "PWS/1.1")]

    #1.打開指定模板文件,讀取模板文件中的數據
    with open("template/index.html", "r") as file:
        file_data = file.read()

    # 2.查詢數據庫,模板裡面的模板變量({%content%}) ,替換成以後從數據庫裡面查詢的數據
    conn = pymysql.connect(host="10.211.55.16",
                           port=3306,
                           user="root",
                           password="00065638",
                           database="stock_db",
                           charset="utf8")
    # 3.獲取游標，目的就是要執行sql語句
    cursor = conn.cursor()
    # 準備sql 之前在mysql客戶端如何編寫sql，在python程序裡面還怎麼編寫
    sql = "select * from info;"
    # 4.執行sql語句
    cursor.execute(sql)
    # 獲取查詢的結果
    result = cursor.fetchall()
    print(result)

    # 5.關閉游標
    cursor.close()
    # 6.關閉連接
    conn.close()
    #web處理後的數據
    data = ""
    for row in result:
        data += """<tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="000007"></td>
               </tr>""" % row

    response_body = file_data.replace("{%content%}", data)
    # 這裡返回的是元組
    return status, response_header, response_body

def center_data():
    conn = pymysql.connect(host="10.211.55.16",
                    port=3306,
                    user="root",
                    password="00065638",
                    database="stock_db",
                    charset="utf8")
    cursor = conn.cursor()
    sql = '''select i.code, i.short, i.chg, i.turnover, i.price, i.highs, i.time, c.note_info 
             from info i inner join focus c 
             on i.id = c.info_id;
          '''
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    conn.close()


@route("/center.html")
def center():
    # 狀態信息
    status = "200 OK"
    # 響應頭信息
    response_header = [("server", "PWS/1.1")]

    # 1.打開指定模板文件,讀取模板文件中的數據
    with open("template/center.html", "r") as file:
        file_data = file.read()

    # 2.查詢數據庫,模板裡面的模板變量({%content%}) ,替換成以後從數據庫裡面查詢的數據
    # web處理後的數據
    data = time.ctime()

    response_body = file_data.replace("{%content%}", data)
    # 這裡返回的是元組
    return status, response_header, response_body

# 處理沒找到的動態資源
def not_found():
    # 狀態信息
    status = "404 Not Found"
    # 響應頭信息
    response_header = [("server", "PWS/1.1")]
    # web處理後的數據
    data = "Not Found"

    # 這裡返回的是元組
    return status, response_header, data


# 處理動態資源請求
def handle_request(env):
    #獲取動態的請求資源路徑
    request_path = env["request_path"]
    print("動態資源請求的地址:", request_path)
    # 判斷請求的資源路徑，選擇指定的函數處理對應的動態資源請求

    for path, func in route_list:
        if request_path == path:
            result = func()
            return result

    #
    # if request_path =="/index.html":
    #     # 獲取首頁數據
    #     result = index()
    #     # 把處理好的結果返回給web服務器使用，讓web服務器拼接響應報文時使用
    #     return result
    #
    # elif request_path == "/center.html":
    #     result = center()
    #     return result

    else:
        #沒有動態資源數據，返回404信息
        result = not_found()
        return result
''
if __name__ == '__main__':
    center_data()
