import requests
import re
import struct
import sys
import urllib3

# 禁用 InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_f5_cookie(cookie):
    """解析 F5 Big-IP 格式的 cookie，并返回内部 IP 和端口"""
    f5_pattern = re.compile(r'BIGipServer[^=]+=(\d+)\.(\d+)\.0000')
    matches = f5_pattern.findall(cookie)
    
    if matches:
        for match in matches:
            host, port = match
            a, b, c, d = [int(x) for x in struct.unpack("<BBBB", struct.pack("<I", int(host)))]
            port = int(port)
            return f"{a}.{b}.{c}.{d}:{port}"
    return None

def check_f5_leakage(url):
    """检查 URL 是否存在 F5 内网 IP 泄露"""
    try:
        session = requests.Session()
        response = session.get(url, verify=False)
        
        detected_ip = None
        if 'Cookie' in response.request.headers:
            cookies = response.request.headers['Cookie']
            detected_ip = parse_f5_cookie(cookies)
        
        if 'Set-Cookie' in response.request.headers:
            set_cookie = response.request.headers['Set-Cookie']
            ip_from_set_cookie = parse_f5_cookie(set_cookie)
            if ip_from_set_cookie:
                detected_ip = ip_from_set_cookie
        
        if 'Set-Cookie' in response.headers:
            set_cookie = response.headers['Set-Cookie']
            ip_from_set_cookie = parse_f5_cookie(set_cookie)
            if ip_from_set_cookie:
                detected_ip = ip_from_set_cookie
        
        if 'Cookie' in response.headers:
            cookies = response.headers['Cookie']
            ip_from_cookie = parse_f5_cookie(cookies)
            if ip_from_cookie:
                detected_ip = ip_from_cookie
        
        if detected_ip:
            return f"[+]存在F5内网ip泄漏 IP：{detected_ip}"
        else:
            return "[-]不存在F5内网ip泄漏"
    
    except requests.RequestException as e:
        return f"Error occurred: {e}"

def process_urls(urls, save_to_file):
    results = []
    for url in urls:
        result = check_f5_leakage(url)
        results.append(result)
        print(result)
    
    if save_to_file:
        with open("result_success.txt", "w") as file:
            for result in results:
                if "[+]" in result:
                    file.write(result + "\n")

def print_help():
    """显示帮助信息"""
    help_text = """
Usage:
  script.py -u <url> [-d]
    -u <url>       : Scan a single URL for F5 Big-IP leakage.
    -d             : Save results with leakage information to result_success.txt.

  script.py -f <file_path> [-d]
    -f <file_path> : Scan URLs listed in the specified file for F5 Big-IP leakage.
    -d             : Save results with leakage information to result_success.txt.

  script.py -h
    -h             : Display this help message.
"""
    print(help_text)

def main():
    if len(sys.argv) < 2:
        print("Usage: script.py [-h | -u <url> | -f <file_path>] [-d]")
        sys.exit(1)
    
    option = sys.argv[1]
    save_to_file = '-d' in sys.argv
    
    if option == "-h":
        print_help()
        sys.exit(0)
    
    urls = []
    
    if option == "-u":
        if len(sys.argv) != 3 and not save_to_file:
            print("Usage: script.py -u <url> [-d]")
            sys.exit(1)
        url = sys.argv[2]
        urls.append(url)
    
    elif option == "-f":
        if len(sys.argv) != 3 and not save_to_file:
            print("Usage: script.py -f <file_path> [-d]")
            sys.exit(1)
        file_path = sys.argv[2]
        try:
            with open(file_path, "r") as file:
                urls = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            sys.exit(1)
    
    else:
        print(f"Invalid option: {option}")
        print("Usage: script.py [-h | -u <url> | -f <file_path>] [-d]")
        sys.exit(1)
    
    process_urls(urls, save_to_file)

if __name__ == "__main__":
    main()
