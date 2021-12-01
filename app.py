from website import createApp
import os


if __name__ == "__main__":
    app = createApp()
    app.config['APPLICATION_ROOT']="/website"
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['STATIC_FOLDER'] = os.path.join(basedir, '/website/static')
    app.run(debug=False)