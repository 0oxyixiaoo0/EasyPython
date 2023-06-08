import time
def focus_timer(duration):
    start_time = time.time()
    end_time = start_time + duration * 60  # 将分钟转换为秒

    print("专注计时开始！")

    while time.time() < end_time:
        time_left = int(end_time - time.time())
        minutes = time_left // 60
        seconds = time_left % 60

        timer_display = f"{minutes:02d}:{seconds:02d}"  # 格式化时间显示为 mm:ss

        print(timer_display, end="\r")  # 使用 \r 实现动态显示，覆盖上一次输出

        time.sleep(1)  # 每秒钟更新一次显示

    print("专注时间结束！")


focus_timer(30)
