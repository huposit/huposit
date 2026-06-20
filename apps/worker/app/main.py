import time


def main() -> None:
    print("Huposit worker started")

    while True:
        print("Worker heartbeat")
        time.sleep(10)


if __name__ == "__main__":
    main()