"""
最小测试版本 - 用于诊断Render部署问题
"""
from flask import Flask, jsonify
import sys
import os

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "ok",
        "message": "服务运行正常",
        "python_version": sys.version,
        "files": os.listdir('.')
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("=" * 60)
    print("测试服务启动")
    print("Python版本:", sys.version)
    print("当前目录:", os.getcwd())
    print("文件列表:", os.listdir('.'))
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
