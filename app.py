import os
from flask import Flask, render_template
from config import Config
from database.schema import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Database Schema & Seed Data
    try:
        init_db(seed_sample_data=True)
    except Exception as e:
        print(f"[App Init] Database initialization note: {e}")

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.readers import readers_bp
    from routes.books import books_bp
    from routes.borrowing import borrowing_bp
    from routes.warehouse import warehouse_bp
    from routes.circulation import circulation_bp
    from routes.mining import mining_bp
    from routes.text_mining import text_mining_bp
    from routes.reports import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(readers_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(borrowing_bp)
    app.register_blueprint(warehouse_bp)
    app.register_blueprint(circulation_bp)
    app.register_blueprint(mining_bp)
    app.register_blueprint(text_mining_bp)
    app.register_blueprint(reports_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('base.html', error_message="Page Not Found (404)"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('base.html', error_message="Internal Server Error (500)"), 500

    return app

# Expose app at module level for Vercel / WSGI servers
app = create_app()

if __name__ == '__main__':
    print("\n" + "="*70)
    print(" >>> LIBRARY MANAGEMENT DATA WAREHOUSE & DATA MINING SYSTEM <<<")
    print(" ="*70)
    print(" Access Web Dashboard at: http://127.0.0.1:5000")
    print(" Default Login: Username: 'admin' | Password: 'admin123'")
    print("="*70 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=False)
