import multiprocessing
import time

def worker(num, return_dict):
    print(f"Worker {num} started")
    time.sleep(2)
    result = f"Result from worker {num}"
    return_dict[num] = result
    print(f"Worker {num} finished")

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    processes = []

    # 프로세스 생성
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i, return_dict))
        processes.append(p)
        p.start()

    # 프로세스 종료 대기
    for p in processes:
        p.join()

    print("All processes finished")
    print("Results:", dict(return_dict))