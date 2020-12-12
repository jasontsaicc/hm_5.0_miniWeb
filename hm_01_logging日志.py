# 就是用來記錄程序運行時的日誌信息的
import logging

# 設置logging的配置
# level表示級別
# %(asctime)s 當前時間
# %(filename)s 表示程序文件名
# %(lineno)d 表示行號
# %(levelname)s 表示日誌級別
# %(message)s 表示日誌信息

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s-%(filename)s[lineno:%(lineno)d]-%(levelname)s-%(message)s",
                    filename="log.txt",
                    filemode="a")

logging.debug("debug等級的日誌")
logging.info("info等級的日誌")
logging.warning("warning等級的日誌")
logging.error("error等級的日誌")
logging.critical("critical等級的日誌")
# 默認是warning級別,只有大於OR等於 warning才會顯示
