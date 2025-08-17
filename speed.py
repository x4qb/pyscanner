import sys
import speedtest

def main():
    print("Testing network speed..")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = st.results.ping

        print(f"Download speed: {download:.2f} mbps")
        print(f"Upload speed: {upload:.2f} mbps")
        print(f"Latency: {ping:.2f} ms")

    except Exception as e:
        print(f"Error running speedtest: {e}")

if __name__ == "__main__":
    main()
