from app import create_app, db
from flask_migrate import Migrate

app = create_app()
app.config['UPLOAD_FOLDER'] = './uploads'  # Папка для загруженных файлов и вырезов подписей
migrate = Migrate(app, db)


if __name__ == "__main__":
    app.run(debug=True, port=5009)
