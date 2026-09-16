import time
import subprocess
import sys
from datetime import datetime, timedelta

# Cấu hình thời gian: 2 phút (120 giây) bắn 1 lần
LOOP_INTERVAL = 120  
MAX_RUN_TIME = timedelta(hours=5, minutes=30)  # Tự ngắt an toàn sau 5.5 tiếng
start_time = datetime.now()

def hunt_server():
    # Thay câu lệnh OCI của anh vào đây
    cmd = [
        "oci", "compute", "instance", "launch",
        # Các tham số compartment-id, shape, image-id, subnet-id... của anh
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[{datetime.now()}] THÀNH CÔNG RỰC RỠ! Đã hốt được máy:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now()}] Chưa nhả máy (Out of host capacity), đang canh tiếp...")
        return False

if __name__ == "__main__":
    print(f"Bắt đầu vòng lặp săn OCI Ampere: Tần suất {LOOP_INTERVAL // 60} phút/lần.")
    
    while True:
        if datetime.now() - start_time > MAX_RUN_TIME:
            print("Đã đạt mốc 5.5 tiếng, script chủ động thoát an toàn.")
            sys.exit(0)
            
        success = hunt_server()
        if success:
            sys.exit(0)
            
        time.sleep(LOOP_INTERVAL)
