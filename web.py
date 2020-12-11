import socket
import os
import threading
import sys
import framework

class HttpWebSever(object):
    def __init__(self, port):
        # 創建tcp服務端套接字
        tcp_sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        tcp_sever_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        # 綁定端口號
        tcp_sever_socket.bind(("", port))

        # 設置監聽
        tcp_sever_socket.listen(128)

        self.tcp_sever_socket = tcp_sever_socket

    @staticmethod
    def handle_client_request(new_socket):
        # 代碼執行到此 建立成功
        # 接收客戶端的請求信息 可以設置接收4KB資料
        recv_data = new_socket.recv(4096)

        # 判斷接收的數據長度是否為0
        if len(recv_data) == 0:
            new_socket.close()
            return

        # 對二進制數據進行解碼
        recv_content = recv_data.decode("utf-8")
        print(recv_content)

        # 對數據按照空格進行分割
        request_list = recv_content.split(" ", maxsplit=2)
        # 獲取請求的資源路徑
        request_path = request_list[1]

        print(request_path)

        # 判斷請求的是否是根目錄，如果是根目錄設置返回的信息
        if request_path == "/":
            request_path = "/index.html"

        if request_path.endswith(".html"):
            """動態資源請求"""
            #動態資源請求找web框架進行處理,需要把請求參數給web框架
            # 準備給web框架的參數信息,都要放到字典裡
            env = {
                "request_path" : request_path,
                # 傳入請求頭信息,額外的參數可以在字典中添加
            }
            # 使用框架處理動態資源請求
            # 1.web框架需要把處理結果返回給web服務器，
            # 2.web服務區負責把返回的結果封裝成響應報文發給瀏覽器
            status, headers, response_body = framework.handle_request(env)
            print(status, headers, response_body)
            # 響應行
            response_line = "HTTP/1.1 %s\r\n" % status
            # 響應頭
            response_header = ""
            for header in headers:
                response_header += "%s: %s\r\n" % header
            #響應報文
            response_data = (response_line +
                             response_header +
                             "\r\n" +
                             response_body).encode("utf-8")
            #發送響應報文給瀏覽器
            new_socket.send(response_data)
            # 關閉連結
            new_socket.close
        else:
            """靜態資源請求"""
            # 判斷是否是動態資源請求，以後把後綴是.html的請求任務是動態資源請求


            # 1. os.path.exists 如果路径 path 存在，返回 True；如果路径 path 不存在，返回 False。
            # os.path.exists("static/" + request_path)

            # 2.try-except

            # print(recv_data)

            # 打開文件讀取文件中的數據
            # 原本寫法
            # file = open("static/index.html")
            # file.close()

            # 新的寫法
            # 提示， with open關閉文件這 步操作不用程序員來完成，系統幫我們來完成|
            # 打開文件讀取文件中的數據，提示:這裡使用rb模式，兼容打開圖片文件

            # 代碼執行到此，說明沒有請求的該文件，返回404狀態信息
            try:
                with open("static/" + request_path, "rb") as file:  # 這裡的file表示打開文件的對象.

                    file_data = file.read()

            except Exception as e:

                # 響應行
                response_line = "HTTP/1.1 404 Not Fount\r\n"
                # 響應頭
                response_header = "Server: PWS/1.0\r\n"

                with open("static/error.html", "rb") as file:
                    file_data = file.read()

                    response_body = file_data

                    # 把數據封裝成http響應報文格式的數據
                    response = (response_line + response_header + "\r\n").encode("utf-8") + response_body

                    # 發送給瀏覽器的響應報文數據
                    new_socket.send(response)


            # 代碼執行到此，說明文件存在，返回200狀態信息|
            else:

                # 把數據封裝成http響應報文格式的數據 不能直接發給瀏覽器
                # 響應行
                response_line = "HTTP/1.1 200 OK\r\n"

                # 響應頭
                response_header = "Server: PWS/1.0\r\n"
                # 空行
                # 響應體
                response_body = file_data

                # 把數據封裝成http響應報文格式的數據
                response = (response_line + response_header + "\r\n").encode("utf-8") + response_body

                # 發送給瀏覽器的響應報文數據
                new_socket.send(response)

            finally:
                # 關閉服務於客戶端的套接字
                new_socket.close()

    def start(self):
        # 循環等待接受客戶端的連接請求
        while True:
            # 等待接受客戶端的連接請求
            new_socket, ip_post = self.tcp_sever_socket.accept()

            sub_thread = threading.Thread(target=self.handle_client_request, args=(new_socket,))
            sub_thread.setDaemon(True)
            sub_thread.start()



def main():

    # params = sys.argv
    
    # if len(params) != 2:

    #     print("輸入的端口好格式如下ＸＸＸＸ 必須數字")
    #     return

    # if not params[1].isdigit():

    #     print("輸入的端口好格式如下ＸＸＸＸ 必須數字")
    #     return
    
    # port = int(params[1])


    webserver = HttpWebSever(8002)
    webserver.start()





if __name__ == '__main__':
    main()

