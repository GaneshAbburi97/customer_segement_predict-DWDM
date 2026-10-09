import os
import tempfile

class Config:
    # Flask Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'library-dwdm-secret-key-2026-academic-secure')
    
    # Check if running in Vercel / Serverless environment
    IS_VERCEL = bool(os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))
    
    # Primary MySQL Database Configuration
    DB_TYPE = os.environ.get('DB_TYPE', 'mysql')  # 'mysql' or 'sqlite'
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'library_dw_dm')
    
    # SQLite Database Configuration:
    # On Vercel, the project filesystem is read-only, so use /tmp directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    if IS_VERCEL:
        SQLITE_PATH = os.path.join(tempfile.gettempdir(), 'library_dw_dm.sqlite')
    else:
        SQLITE_PATH = os.path.join(BASE_DIR, 'data', 'library_dw_dm.sqlite')
    
    # Default Admin Credentials
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    # ETL & Mining Settings
    DEFAULT_MIN_SUPPORT = 0.08
    DEFAULT_MIN_CONFIDENCE = 0.40
    DEFAULT_K_CLUSTERS = 3

# Configure headless matplotlib environment for serverless
os.environ.setdefault('MPLCONFIGDIR', tempfile.gettempdir())
