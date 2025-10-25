"""便捷启动脚本"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from api.app import app

if __name__ == '__main__':
    # 支持 Render 等平台的动态端口
    PORT = int(os.getenv('PORT', 8000))
    IS_PRODUCTION = os.getenv('FLASK_ENV', 'development') == 'production'
    
    print("=" * 70)
    print("🌍 ICT Infrastructure Dashboard")
    print("=" * 70)
    print(f"\n🌐 Dashboard:  http://localhost:{PORT}")
    print(f"📡 API:        http://localhost:{PORT}/api/v1")
    print(f"❤️  Health:     http://localhost:{PORT}/health")
    print(f"\n🔧 Environment: {os.getenv('FLASK_ENV', 'development')}")
    print("\n" + "=" * 70)
    print("Press CTRL+C to stop")
    print("=" * 70 + "\n")
    
    app.run(
        debug=not IS_PRODUCTION,  # 生产环境关闭debug
        host='0.0.0.0',
        port=PORT
    )