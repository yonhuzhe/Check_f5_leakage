1. 安装Python
	确保系统上已经安装了Python 
	python --version
	如果没有安装Python 3，可以从Python官网下载并安装。
2. 安装依赖库
	脚本依赖于 requests 和 urllib3 库。如果这些库还没有安装，可以使用 pip 安装：	
	pip install -r requirements.txt
3. 创建脚本文件
	将以下代码保存到一个Python脚本文件中，例如 check_f5_leakage.py：
4. 运行脚本
	扫描单个URL:
		python check_f5_leakage.py -u https://example.com
	从文件中批量扫描URL:
		python check_f5_leakage.py -f urls.txt
	将结果保存到文件:
	python check_f5_leakage.py -u https://example.com -d
	python check_f5_leakage.py -f urls.txt -d
	显示帮助信息:
	python check_f5_leakage.py -h
5. 文件准备
	确保将包含待扫描URL的文件（如 urls.txt）放在脚本所在目录，并在文件中每行写一个URL。
	按照这些步骤，你应该能够成功安装和运行该脚本。如果遇到任何问题，请检查Python环境和依赖库是否正确安装。
